## <a name="create-securex-relationship"></a> Cohesity Threat Response - Create SecureX Relationship
[home](../../README.md)

This atomic action creates a Cisco Threat Response Relationship object. This is used in the [Cohesity Helios: Get Anomalous Objects v1.2 workflow](../workflows/HeliosRansomwareAlertsToThreatResponse.md). Refer [Cisco Github](https://github.com/threatgrid/ctim/tree/master/doc) to find more about it. 

### Input

When you run this Atomic action, it will ask for the following input. 

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Access Token | Secure String | An access token for the Threat Response API. This is often obtained using the "Threat Response - Generate Access Token" atomic | Yes | 
| External ID | String | External ID can be used to uniquely identify the SecureX Relationship   | Yes | 
| Incident ID | String | Incident ID that needs to be linked in this relationship   | Yes | 
| Sighting ID | String | Sighting ID that needs to be linked in this relationship   | Yes | 


### Output

N/A