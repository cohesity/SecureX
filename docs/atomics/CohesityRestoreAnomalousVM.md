
### <a name="restore-anomalous-objects"></a> Cohesity Helios - Restore Anomalous VM
[home](../../README.md)

This Atomic Action performs a restore operation for the specified anomalous VM to latest clean snapshot. Currently only VMware VMs are supported. This atomic action can be used to create your own custom workflow and the output from this Atomic action can be used to perform some action. Currently this atomic is being used by [Cohesity Helios: Restore Anomalous Object v1.2](../workflows/CohesityRestoreAnomalousObject.md) workflow

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Cluster ID | String | Cohesity Cluster ID where the anomalous object is sitting | Yes | 
| Restore Request Body | String | The Restore Request body for the VM that needs to be restored. Refer https://helios.cohesity.com/docs/restApiDocs/browse/ for the documentation on Restore API Object   | Yes | 

A sample Restore Request body is shown as below.

```
{
  "name": "",
  "type": "kRecoverVMs",
  "vmwareParameters": {
    "poweredOn": true,
    "prefix": "Recover-",
    "suffix": ""
  },
  "objects": [
    {
      "jobId": 1234,
      "jobRunId": 1234,
      "startedTimeUsecs": 1635972955123123,
      "sourceName": "VM_NAME",
      "protectionSourceId": 1234
    }
  ]
}
```

##### Output

N/A

