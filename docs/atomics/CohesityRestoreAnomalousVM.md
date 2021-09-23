
### <a name="restore-anomalous-objects"></a> Cohesity Helios - Restore Anomalous VM
[top](#Cisco-SecureX-Integration)

This Atomic Action performs a restore operation for the specified anomalous VM to latest clean snapshot. Currently only VMware VMs are supported. This atomic action also resolves the corresponding alert on Helios after restore task for that vm is triggered.

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Object | String | The name of the VM that needs to be restored   | Yes | 

##### Output

| **Argument Name** | **Type** | **Description** |
| --- | --- | --- |
| Restored Object  | String  | The name of the VM that was restored to the latest snapshot | 