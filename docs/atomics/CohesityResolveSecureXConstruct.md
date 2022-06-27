## <a name="resolve-securex-objects"></a> Cohesity Threat Response - Resolve SecureX Incident Sighting and Relationship
[home](../../README.md)

This atomic action Resolves the Cisco Threat Response Incident, Sighting and Relationship object. This is used in the [Cohesity Helios: Restore Anomalous Objects v1.2 workflow](../workflows/CohesityRestoreAnomalousObject.md) and [Cohesity Helios: Ignore Anomalous Objects v1.2 workflow](../workflows/IgnoreAnomalyOnCohesity.md). Refer [Cisco Github](https://github.com/threatgrid/ctim/tree/master/doc) to find more about it. 

### Input

When you run this Atomic action, it will ask for the following input. 

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Access Token | Secure String | An access token for the Threat Response API. This is often obtained using the "Threat Response - Generate Access Token" atomic | Yes | 
| Incident ID | String | Incident ID that needs to be Resolved   | Yes | 
| Sighting ID | String | Sighting ID that needs to be Resolved   | Yes | 


### Output

N/A