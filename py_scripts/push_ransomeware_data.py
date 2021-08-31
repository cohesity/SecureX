'''
SecureX orchestration workflow python script used to get anomalous objects detected
in the last n hours from Cohesity Helios and push to SecureX private intelligence
Script usage:
python push_ransonware_data.py <client_id> <client_password> <helios_api_key> <n>
client_id: Threat Response API client id
client_password: Threat Response API client password
helios_api_key: Cohesity Helios API key
n: number of hours, used to get anomalous objects detected in the last n hours
'''
import argparse
import datetime
import json
import requests
import sys
import datetime

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

def _get_sightings_from_external_id(external_id, tr_access_token):
    try:
        url = 'https://private.intel.amp.cisco.com/ctia/sighting/external_id/' + external_id
        headers = {
            'Authorization': 'Bearer ' + tr_access_token,
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            raise Exception('Failed to get sightings from external id, ' + str(response.json()))
        return response.json()
    except Exception as e:
        raise Exception(str(e))

def _get_incidents_from_external_id(external_id, tr_access_token):
    try:
        url = 'https://private.intel.amp.cisco.com/ctia/incident/external_id/' + external_id
        headers = {
            'Authorization': 'Bearer ' + tr_access_token,
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            raise Exception('Failed to get incidents from external id, ' + str(response.json()))
        return response.json()
    except Exception as e:
        raise Exception(str(e))


def create_sightings(tr_access_token, alert):
    try:
        service_now_description = {}
        headers = {
            'Authorization': 'Bearer ' + tr_access_token,
            'Content-Type': 'application/json'
        }

        property_dict = _get_property_dict(alert['propertyList'])
        external_id = property_dict.get('object', '') + '___' +\
                        property_dict.get('entityId', '') + '___' +\
                        property_dict.get('source', '') + '___' +\
                        property_dict.get('cluster', '') + '___' +\
                        property_dict.get('cid', '')
        service_now_description = {
            "shortDescription": "[CiscoSecureX]Anomalous object \'" + property_dict.get("object", "") +
                                "\' from Cohesity. Source: \'" +
                                property_dict.get("source", "") + "\' Cluster: \'" +
                                property_dict.get("cluster", "") + "\'",
            "description": alert.get('alertDocument')['alertName'] + ". \n" +
                            alert.get('alertDocument')['alertDescription'] + ". \n" +
                            alert.get('alertDocument')['alertCause'] + ". \n" +
                            alert.get('alertDocument')['alertHelpText']
        }
        sightings = _get_sightings_from_external_id(external_id, tr_access_token)
        if sightings:
            sighting = sightings[0]
            url = 'https://private.intel.amp.cisco.com/ctia/sighting/' + sighting['id'].split('/')[-1]
            sighting['resolution'] = ''
            sighting['observed_time']['start_time'] = datetime.datetime.utcfromtimestamp(
                    float(alert['firstTimestampUsecs']) / 1000000).isoformat()
            sighting['observed_time']['end_time'] = datetime.datetime.utcfromtimestamp(
                    float(alert['latestTimestampUsecs']) / 1000000).isoformat()
            response = requests.put(url, headers=headers,
                                        verify=False, json=sighting)
            if response.status_code != 200:
                raise Exception('Failed to update the sighting, ' + str(response.json()))
            else:
                return json.loads(response.content), service_now_description
        else:
            url = 'https://private.intel.amp.cisco.com/ctia/sighting'
            sighting = {
                "description": "Anomalous object from Cohesity"
                                " Helios. The object is under source \'" +
                                property_dict.get("source", "") +
                                "\' on cluster \'" + property_dict.get("cluster", "") + "\'",
                "observables": [
                    {
                        "type": "hostname",
                        "value": property_dict.get("object", "")
                    }
                ],
                "source": "Cohesity Helios",
                "severity": "High",
                "confidence": "High",
                "internal": True,
                "observed_time": {
                    "start_time": datetime.datetime.utcfromtimestamp(
                        float(alert['firstTimestampUsecs']) / 1000000).isoformat(),
                    "end_time": datetime.datetime.utcfromtimestamp(
                        float(alert['latestTimestampUsecs']) / 1000000).isoformat()
                },
                "external_ids": [external_id],
                "external_references": [
                    {
                        "source_name": property_dict.get('source', ''),
                        "description": "The source in which the anomalous object is present"
                    }
                ]
            }
            response = requests.post(url, headers=headers,
                                        verify=False, json=sighting)
            if response.status_code != 201:
                raise Exception('Failed to create sighting, ' + str(response.json()))
            else:
                return json.loads(response.content), service_now_description
    except Exception as e:
        raise Exception(str(e))


def create_incidents(tr_access_token, alert):
    try:
        headers = {
            'Authorization': 'Bearer ' + tr_access_token,
            'Content-Type': 'application/json'
        }

        property_dict = _get_property_dict(alert['propertyList'])
        external_id = property_dict.get('object', '') + '___' +\
                        property_dict.get('entityId', '') + '___' +\
                        property_dict.get('source', '') + '___' +\
                        property_dict.get('cluster', '') + '___' +\
                        property_dict.get('cid', '')
        incidents = _get_incidents_from_external_id(external_id, tr_access_token)
        if incidents:
            incident = incidents[0]
            url = 'https://private.intel.amp.cisco.com/ctia/incident/' + incident['id'].split('/')[-1]

            incident['incident_time']['opened'] = datetime.datetime.utcfromtimestamp(
                    float(alert['firstTimestampUsecs']) / 1000000).isoformat()
            incident['incident_time']['discovered'] = datetime.datetime.utcfromtimestamp(
                    float(alert['firstTimestampUsecs']) / 1000000).isoformat()
            incident['incident_time']['reported'] = datetime.datetime.utcfromtimestamp(
                    float(alert['firstTimestampUsecs']) / 1000000).isoformat()
            response = requests.put(url, headers=headers,
                                        verify=False, json=incident)
            if response.status_code != 200:
                raise Exception('Failed to update the incident, ' + str(response.json()))
            else:
                return json.loads(response.content)
        else:
            url = 'https://private.intel.amp.cisco.com/ctia/incident'
            incident = {
                "description": "Anomalous object from Cohesity"
                                " Helios. The object is under source \'" +
                                property_dict.get("source", "") +
                                "\' on cluster \'" + property_dict.get("cluster", "") + "\'" + "\n" +
                                "# Alert Info \n\n" + 
                                "*Alert Name* : " + alert['alertDocument']['alertName'] + "\n\n" + 
                                "*Alert Description* : " + alert['alertDocument']['alertDescription'] + "\n\n" + 
                                "*Alert Cause* : " + alert['alertDocument']['alertCause']+ "\n\n" + 
                                "*Alert Help Text* : " + alert['alertDocument']['alertHelpText'] ,
                "confidence": "High",
                "incident_time": {
                    "opened": datetime.datetime.utcfromtimestamp(float(alert['firstTimestampUsecs']) / 1000000).isoformat(),
                    "discovered": datetime.datetime.utcfromtimestamp(float(alert['firstTimestampUsecs']) / 1000000).isoformat(),
                    "reported": datetime.datetime.utcfromtimestamp(float(alert['firstTimestampUsecs']) / 1000000).isoformat()
                },
                "schema_version": "1.1.3", 
                "status": "New",
                "type": "incident",
                "source": "Cohesity Helios",
                "external_ids": [external_id],
                "title": "Cohesity Helios: " + property_dict.get("object", ""),
                "external_references": [
                    {
                        "source_name": property_dict.get('source', ''),
                        "description": "The source in which the anomalous object is present"
                    }
                ]

            }
            response = requests.post(url, headers=headers,
                                        verify=False, json=incident)
            if response.status_code != 201:
                raise Exception('Failed to create Incident, ' + str(response.json()))
            else:
                return json.loads(response.content)
    except Exception as e:
        raise Exception(str(e))


def create_relationship(tr_access_token, source, destination):
    try:
        headers = {
            'Authorization': 'Bearer ' + tr_access_token,
            'Content-Type': 'application/json'
        }
        url = 'https://private.intel.amp.cisco.com/ctia/relationship'
        relation = {
            "description": "Cohesity Anomalous Object Sighting to Incident Relation",
            "title": "Cohesity Anomalous Object Sighting to Incident Relation",
            "relationship_type": "related-to",
            "schema_version": "1.1.3",
            "type": "relationship",
            "source_ref": source,
            "target_ref": destination

        }
        response = requests.post(url, headers=headers,
                                    verify=False, json=relation)
        if response.status_code != 201:
            raise Exception('Failed to create relation, ' + str(response.json()))
    except Exception as e:
        raise Exception(str(e))


###### Cohesity Functions ###### 

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


def get_ransomware_alerts(args):
    '''
    get ransomware alerts from Cohesity Helios
    :param args:
    :return:
    '''
    try:
        ransomware_alerts = []
        url = 'https://helios.cohesity.com/mcm/alerts?' \
              'alertCategoryList=kSecurity&alertStateList=kOpen'
        params = {
            "maxAlerts": 1000,
            "alertCategoryList": "kSecurity",
            "alertStateList": "kOpen",
            "_includeTenantInfo": True,
            "startDateUsecs": int((time.time() - int(args.n) * 60 * 60) * 1000000)
        }
        headers = {'Content-Type': 'application/json',
                   'apiKey': args.helios_api_key}
        response = requests.get(url, headers=headers, params=params, verify=False)
        if response.status_code != 200:
            raise Exception(str(response.json()))
        for alert in response.json():
            if alert['alertCode'] == 'CE01516011':
                ransomware_alerts.append(alert)
        return ransomware_alerts
    except Exception as e:
        raise Exception("Failed to get ransomware alerts from Helios, " + str(e))


def main(args):
    service_now_descriptions = []
    try:
        tr_access_token = _get_access_token(args)
        ransomware_alerts = get_ransomware_alerts(args)
        for alert in ransomware_alerts:
            sighting, service_now_description = create_sightings(tr_access_token, alert)
            incident = create_incidents(tr_access_token, alert)
            service_now_description['description'] = service_now_description['description'] + "\n" + incident['id']
            create_relationship(tr_access_token, sighting['id'], incident['id'])
            service_now_descriptions.append(service_now_description)
        print(json.dumps(service_now_descriptions))
    except Exception as e:
        sys.exit(str(e))
parser = argparse.ArgumentParser(
    description="Arguments to get anomalous objects from Helios"
                " and push to private intelligence")
parser.add_argument("client_id", help="Threat Response API client id")
parser.add_argument("client_password", help="Threat Response API client password")
parser.add_argument("helios_api_key", help="Cohesity Helios API key")
parser.add_argument("n", help="Number of hours, filter anomalous objects detected"
                              " in the last n hours")
args = parser.parse_args()
main(args)
