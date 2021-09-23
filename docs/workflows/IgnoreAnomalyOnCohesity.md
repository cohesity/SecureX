### <a name="ignore-anomaly-workflow"></a> Ignore Anomaly on Cohesity Helios
[top](#Cisco-SecureX-Integration)

This workflow ignores anomaly for the specified object on Helios which removes this object from the list of anomalous objects. This workflow also suppresses anomalous object alert on helios of the given object. This workflows also Resolves the SecureX Incident and Sighting or deletes them, based on the `Cohesity Delete Sighting and Incident` variable. 
 
> This is an Response workflow. 

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Threat Response API Client Id | Secure String | Threat Response API Client ID | Yes | 
| Threat Response API Client Password | Secure String | Threat Response API Client Password | Yes | 
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Cohesity Delete Sighting and Incident | String | Specifies where to delete or not the sighting once the anomaly is ignored. Can be `yes` or `no`. | Yes | 

##### Output

N/A