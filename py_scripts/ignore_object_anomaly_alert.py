'''
SecureX orchestration workflow python script used to ignore anomalous object on Helios
and delete or update the sighting once ignore operation is successful
Script usage:
python ignore_object_anomaly_alert.py <client_id> <client_password> <helios_api_key> <object> <delete>
client_id: Threat Response API client id
client_password: Threat Response API client password
helios_api_key: Cohesity Helios API key
object: Anomalous object name
delete: Specifies where to delete or not the sighting once the anomaly is ignored.
        Can be 'yes' or 'no'.
'''

import argparse
import requests
import sys

##### Cohesity Functions #######

def _get_property_dict(property_list):
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


def get_ransomware_alert_id(args):
    '''
    get ransomware alert id from Helios for the given
    anomalous object
    :param args:
    :return:
    '''
    try:
        alert_id = ''
        url = 'https://helios.cohesity.com/mcm/alerts'
        params = {
            "maxAlerts": 1000,
            "alertCategoryList": "kSecurity",
            "alertStateList": "kOpen",
            "_includeTenantInfo": True
        }
        headers = {'Content-Type': 'application/json',
                   'apiKey': args.helios_api_key}
        response = requests.get(url, headers=headers, params=params, verify=False)
        if response.status_code != 200:
            raise Exception(str(response.json()))
        for alert in response.json():
            if alert['alertCode'] == 'CE01516011':
                property_dict = _get_property_dict(alert['propertyList'])
                if property_dict.get('object', "") == args.object:
                    alert_id = alert['id']
        return alert_id
    except Exception as e:
        raise Exception("Failed to get ransomware alert id from Helios, " + str(e))


##### CISCO Functions #######

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
    update or delete sighting once the anomaly is ignored
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
            sighting['resolution'] = 'Anomaly is ignored'
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


def main(args):
    try:
        alert_id = get_ransomware_alert_id(args)
        if not alert_id:
            raise Exception("Failed to find the anomalous object "
                            + args.object + " on Helios")
        url = 'https://helios.cohesity.com/mcm/alerts/' + alert_id
        headers = {'Content-Type': 'application/json', 'apiKey': args.helios_api_key}
        request_payload = {
            "status": "kSuppressed"
        }
        response = requests.patch(url, headers=headers, json=request_payload, verify=False)
        if response.status_code != 200:
            raise Exception('Failed to ignore anomaly on Helios ' + str(response.json()))
        tr_access_token = _get_access_token(args)
        update_or_delete_sighting(tr_access_token, args)
        print("Workflow succeeded")
    except Exception as e:
        sys.exit(str(e))
parser = argparse.ArgumentParser(
    description="Arguments to ignore anomaly on Helios")
parser.add_argument("client_id", help="Threat Response API client id")
parser.add_argument("client_password", help="Threat Response API client password")
parser.add_argument("helios_api_key", help="Cohesity Helios API key")
parser.add_argument("object", help="Anomalous object name")
parser.add_argument("delete", choices=['yes', 'no'],
                    help="Specify if sighting has to be removed from"
                         " private intelligence once anomaly is ignored")
args = parser.parse_args()
main(args)
