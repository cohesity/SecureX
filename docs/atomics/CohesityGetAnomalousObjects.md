### <a name="get-anomalous-objects"></a> Cohesity Helios - Get Anomalous Objects 
[top](#Cisco-SecureX-Integration)

This atomic perform a fetch operation which gets the list of anomalous objects from Cohesity Helios. 

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Start Time | String | Anomalous Object Alerts created after this time will be fetched. This time is an EPOCH timestamp in microseconds   | No | 
| End Time | String | Anomalous Object Alerts created before this time will be fetched. This time is an EPOCH timestamp in microseconds | No | 

##### Output

| **Argument Name** | **Type** | **Description** |
| --- | --- | --- |
| Anomalous Objects Json | String  | The json object (a JSON string) with holds the anomalous objects fetched from Cohesity Helios | 