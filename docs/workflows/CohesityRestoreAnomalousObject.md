### <a name="restore-anomaly"></a> Cohesity Restore Anomalous Object
[top](#Cisco-SecureX-Integration)

This workflow restores the specified anomalous object to the latest clean snapshot. It also resolves the alert on helios once the restore task is triggered. The restored VM name will in the format Recover-{original VM name}-VM-{epoch timestamp when the vm is restored} and the restore task name on the cluster will be in format Cisco_SecureX_triggered_restore_task_{object name}. This workflows also Resolves the SecureX Incident and Sighting or deletes them, based on the `Cohesity Delete Sighting and Incident` variable. 

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