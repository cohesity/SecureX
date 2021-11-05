### <a name="ignore-anomaly"></a> Cohesity Helios - Ignore Anomaly
[home](../../README.md)

This Atomic Action ignores the anomaly which removes the anomalous object from the list of anomalous object. This suppresses the anomalous object alert on Cohesity Helios. This atomic action can be used when the Anomalous Object is identified to be harmless and now this alert can be ignored. In order to use this Atomic, you will need to get the Alert ID of the Alert. That can be done by running the [Cohesity Helios: Get Anomalous Objects v1.2 atomic](./CohesityGetAnomalousObjects.md). 

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Alert ID | String | The Anomalous Object Alert ID that needs to be Ignored   | Yes | 

##### Output

N/A