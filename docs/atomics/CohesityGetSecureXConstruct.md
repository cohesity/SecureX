## <a name="get-securex-objects"></a> Cohesity Threat Response - Get SecureX Incident Sighting and Relationship
[home](../../README.md)

This atomic action gets the Cisco Threat Response Incident, Sighting and Relationship object so that action can be taken on them, like Deleting or Resolving it.  This is used in the [Cohesity Helios: Ignore Anomaly v1.2]() and [Cohesity Helios: Restore Anomaly v1.2](). Refer [Cisco Github](https://github.com/threatgrid/ctim/tree/master/doc) to find more about it. 

### Input

When you run this Atomic action, it will ask for the following input. 

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Access Token | Secure String | An access token for the Threat Response API. This is often obtained using the "Threat Response - Generate Access Token" atomic | Yes | 
| External ID | String | External ID can be used to uniquely identify the SecureX Incident, Sighting and Relationship object   | Yes | 



### Output

| Relationship ID | String | Relationship ID of the Relation object   | Yes | 
| Incident ID | String | Incident ID for Incident that is created   | Yes | 
| Sighting ID | String | Sighting ID for Sighting that is created   | Yes | 
