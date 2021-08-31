'''
SecureX orchestration workflow python script used to restore an anomalous object on Helios
to the latest clean snapshot.
Supported environments: VMware
Script usage:
python restore_to_latest_clean_snapshot.py <client_id> <client_password> <helios_api_key> <object> <delete>
client_id: Threat Response API client id
client_password: Threat Response API client password
helios_api_key: Cohesity Helios API key
object: Anomalous object name
delete: Specifies where to delete or not the sighting once the anomalous object is
        restored to the latest clean snapshot. Can be 'yes' or 'no'.
'''
import argparse
import requests
import sys
import time

##### Cisco Functions ##### 

def _get_access_token(args):
    '''
    Get Threat Response access token
    :param args:
    :return:
    '''
    try:
        url = "https://visibility.amp.cisco.com/iroh/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        response = requests.post(url, headers=headers, auth=(args.client_id, args.client_password),
                                 verify=False, data={'grant_type': 'client_credentials'})
        if response.status_code != 200:
            raise Exception(str(response.json()))
        return response.json()['access_token']
    except Exception as e:
        raise Exception("Failed to get threat response access token, " + str(e))


def update_or_delete_sighting(tr_access_token, args):
    '''
    update or delete sighting once anomalous object is restored
    :param tr_access_token:
    :param args:
    :return:
    '''
    try:
        headers = {
            'Authorization': 'Bearer ' + tr_access_token,
            'Content-Type': 'application/json'
        }
        url = 'https://private.intel.amp.cisco.com/ctia/sighting/search'
        params = {
            "observables.value": args.object,
            "observables.type": "hostname",
            "source": "Cohesity Helios"
        }
        response = requests.get(url, params=params, headers=headers, verify=False)
        if response.status_code != 200 or not response.json():
            raise Exception("Failed to find the sighting, " + str(response.json()))
        sighting = response.json()[0]
        sightingId = sighting['id']
        url = 'https://private.intel.amp.cisco.com/ctia/sighting/' + sighting['id'].split('/')[-1]
        if args.delete == 'yes':
            response = requests.delete(url, headers=headers, verify=False)
            if response.status_code != 204:
                raise Exception("Failed to delete sighting, " + str(response.json()))
            else:
                incident_id, relationship_id = get_incident_and_relationship_id(tr_access_token, sightingId)
                update_or_delete_incident(tr_access_token, incident_id)
                update_or_delete_relationship(tr_access_token, relationship_id)
        else:
            sighting['resolution'] = 'Anomalous object is restored to latest clean snapshot'
            response = requests.put(url, headers=headers,
                                    verify=False, json=sighting)
            if response.status_code != 200:
                raise Exception('Failed to update the sighting, ' + str(response.json()))
            else:
                incident_id, relationship_id = get_incident_and_relationship_id(tr_access_token, sightingId)
                update_or_delete_incident(tr_access_token, incident_id)
                update_or_delete_relationship(tr_access_token, relationship_id)
    except Exception as e:
        raise Exception(str(e))


def get_restore_properties(args):
    '''
    Get the alert id and the properties needed for
    restore operation
    :param args:
    :return:
    '''
    try:
        alert_id = ''
        url = 'https://helios.cohesity.com/mcm/alerts?alertCategoryList=kSecurity&alertStateList=kOpen'
        params = {
            "maxAlerts": 1000,
            "alertCategoryList": "kSecurity",
            "alertStateList": "kOpen",
            "_includeTenantInfo": True
        }
        headers = {'Content-Type': 'application/json', 'apiKey': args.helios_api_key}
        # get security alerts
        response = requests.get(url, headers=headers, params=params, verify=False)
        if response.status_code != 200:
            raise Exception("Failed to get security alerts from helios, " + str(response.json()))
        restore_properties = {}
        for alert in response.json():
            if alert['severity'] == 'kCritical' and alert['alertState'] == 'kOpen' and \
                    alert['alertCode'] == 'CE01516011':
                property_dict = get_property_dict(alert['propertyList'])
                if property_dict.get('object', "") == args.object:
                    restore_properties = property_dict
                    alert_id = alert['id']
                    break
        return restore_properties, alert_id
    except Exception as e:
        raise Exception(str(e))

def get_incident_and_relationship_id(tr_access_token, sightingId):
    incident_id = ""
    headers = {
        'Authorization': 'Bearer ' + tr_access_token,
        'Content-Type': 'application/json'
    }
    try:
        url = 'https://private.intel.amp.cisco.com/ctia/relationship/search'
        params = {"source_ref": str(sightingId)}
        response = requests.get(url, params=params, headers=headers, verify=False)
        if response.status_code != 200:
            raise Exception('Failed to get relation, ' + str(response.json()))
        else:
            incident_id = response.json()[0]['target_ref']
            relationship_id = response.json()[0]['id']
            return incident_id, relationship_id
    except Exception as e:
        raise Exception(str(e))


def update_or_delete_incident(tr_access_token, incident_id):
    try:
        headers = {
            'Authorization': 'Bearer ' + tr_access_token,
            'Content-Type': 'application/json'
        }
        url = 'https://private.intel.amp.cisco.com/ctia/incident/search'
        params = {
            "id": str(incident_id.split('/')[-1])
        }
        response = requests.get(url, headers=headers, params=params, verify=False)
        if response.status_code != 200 or not response.json():
            raise Exception("Failed to find the incident, " + str(response.json()))
        incident = response.json()[0]
        url = 'https://private.intel.amp.cisco.com/ctia/incident/' + str(incident_id.split('/')[-1])
        if args.delete == 'yes':
            response = requests.delete(url, headers=headers, verify=False)
            if response.status_code != 204:
                raise Exception("Failed to delete incident, " + str(response))
        else:
            incident['status'] = 'Closed'
            response = requests.put(url, headers=headers,
                                    verify=False, json=incident)
            if response.status_code != 200:
                raise Exception("Failed to delete incident, " + str(response))
    except Exception as e:
        raise Exception(str(e))


def update_or_delete_relationship(tr_access_token, relationship_id):
    if args.delete == 'yes':
        try:
            headers = {
                'Authorization': 'Bearer ' + tr_access_token,
                'Content-Type': 'application/json'
            }
            url = 'https://private.intel.amp.cisco.com/ctia/relationship/' + str(relationship_id.split('/')[-1])
            response = requests.delete(url, headers=headers, verify=False)
            if response.status_code != 204:
                raise Exception("Failed to delete relationship, " + str(response))
        except Exception as e:
            raise Exception(str(e))

##### Cohesity Functions #####

def get_property_dict(property_list):
    '''
    get property dictionary from list of property dicts
    with keys, values
    :param property_list:
    :return:
    '''
    property_dict = {}
    for property in property_list:
        property_dict[property['key']] = property['value']
    return property_dict

def restore_vmware_object(restore_properties, args):
    '''
    restore anomalous object to the latest clean snapshot
    :param restore_properties:
    :param args:
    :return:
    '''
    try:
        headers = {'Content-Type': 'application/json', 'apiKey': args.helios_api_key}
        request_payload = {
            "objects": [{"entity": {"id": int(restore_properties["entityId"]),
                                    "parentId": int(restore_properties["parentId"])},
                         "jobId": int(restore_properties["jobId"]),
                         "jobInstanceId": int(restore_properties["jobInstanceId"]),
                         "jobUid": {
                             "clusterId": int(restore_properties['cid']),
                             "clusterIncarnationId": int(restore_properties['clusterIncarnationId']),
                             "objectId": int(restore_properties['jobId'])
                         },
                         "startTimeUsecs": int(restore_properties["jobStartTimeUsecs"]),
                         }],
            "name": "Cisco_SecureX_triggered_restore_task_" + restore_properties["object"],
            "powerStateConfig": {"powerOn": True},
            "restoredObjectsNetworkConfig": {"disableNetwork": False},
            "renameRestoredObjectParam": {"prefix": "Recover-", "suffix": "-VM-" + str(int(time.time()))},
            "continueRestoreOnError": False}
        url = 'https://helios.cohesity.com/irisservices/api/v1/restore'
        headers['clusterid'] = restore_properties['cid']
        response = requests.post(url, headers=headers, json=request_payload, verify=False)
        if response.status_code != 200:
            raise Exception("Failed to restore " + restore_properties['object'] +
                            ' to latest clean snapshot. ' + str(response.json()))
    except Exception as e:
        raise Exception(str(e))

def resolve_alert(alert_id, args):
    '''
    resolve ransomware alert on helios
    :param alert_id:
    :param args:
    :return:
    '''
    try:
        headers = {'Content-Type': 'application/json', 'apiKey': args.helios_api_key}
        request_payload = {
            "status": "kResolved"
        }
        url = 'https://helios.cohesity.com/mcm/alerts/' + alert_id
        response = requests.patch(url, headers=headers, json=request_payload, verify=False)
        if response.status_code != 200:
            raise Exception("Successful in restoring the anomalous object"
                            " but failed to resolve the alert on Helios")
    except Exception as e:
        raise Exception(str(e))


def main(args):
    '''
    :param args: commandline arguments
    :return:
    '''
    try:
        restore_properties, alert_id = get_restore_properties(args)
        if not restore_properties:
            raise Exception("Failed to find the anomalous object on Helios")
        elif restore_properties.get('environment', "") != 'kVMware':
            raise Exception("Workflow supports only VMware environment")
        # restore VMware anomalous object
        elif restore_properties and restore_properties.get('environment') == 'kVMware':
            restore_vmware_object(restore_properties, args)
            resolve_alert(alert_id, args)
            tr_access_token = get_access_token(args)
            update_or_delete_sighting(tr_access_token, args)
        print("Workflow succeeded")
    except Exception as e:
        sys.exit("Workflow failed: " + str(e))


parser = argparse.ArgumentParser(
    description="Arguments to restore anomalous object to latest clean snapshot")
parser.add_argument("client_id", help="Threat Response API client id")
parser.add_argument("client_password", help="Threat Response API client password")
parser.add_argument("helios_api_key", help="Cohesity Helios API key")
parser.add_argument("object", help="Anomalous object name")
parser.add_argument("delete", choices=['yes', 'no'],
                    help="Specify if sighting has to be removed from"
                         " private intelligence once anomalous object is"
                         " restored to the latest clean snapshot")
args = parser.parse_args()
main(args)
