### <a name="resolve-anomaly"></a> Cohesity Helios - Resolve Anomaly
[home](../../README.md)

This Atomic Action resolves the anomaly which removes the anomalous object from the list of anomalous object. This removes the anomalous object alert on Cohesity Helios. This atomic action can be used when an action as been taken on the Anomalous Object and now this alert can be resolved. In order to use this Atomic, you will need to get the Alert ID of the Alert. That can be done by running the [Cohesity Helios: Get Anomalous Objects v1.2 atomic](./CohesityGetAnomalousObjects.md). 

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Alert ID | String | The Anomalous Object Alert ID that needs to be Resolved   | Yes | 

##### Output

N/A