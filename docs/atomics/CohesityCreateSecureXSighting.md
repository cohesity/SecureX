## <a name="create-securex-sighting"></a> Cohesity Threat Response - Create SecureX Sighting
[home](../../README.md)

This atomic action creates a Cisco Threat Response Sighting object. This is used in the [Cohesity Helios: Get Anomalous Objects v1.2 workflow](). Refer [Cisco Github](https://github.com/threatgrid/ctim/tree/master/doc) to find more about it. 

### Input

When you run this Atomic action, it will ask for the following input. 

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Access Token | Secure String | An access token for the Threat Response API. This is often obtained using the "Threat Response - Generate Access Token" atomic | Yes | 
| External ID | String | External ID can be used to uniquely identify the SecureX Sighting   | Yes | 
| Observables | String | A JSON-formatted list of observables. Example: `[ { "type": "ip", "value": "192.168.1.1" }, { "type": "domain", "value": "cisco.com" }]` | Yes | 
| Sighting Description | String | This can be a string of plain text or can be formatted with Markdown | No | 
| Severity | String | Must be one of the following: Medium, Info, Unknown, None, High, Low | Yes | 
| Sighting Confidence | String | Must be one of the following: Medium, Info, Unknown, None, High, or Low | Yes | 
| Sighting Title | String | A short title for the Sighting | Yes | 
| Sighting Source | String | Source from where this incident was created. Default is `Cohesity Helios` | No | 

### Output

This Atomic actions gives out the following output that you can use to perform operations like resolving these objects, restoring the anomalous objects etc. 

| **Argument Name** | **Type** | **Description** |
| --- | --- | --- |
| Sighting ID | String  | The ID of the new Sighting. This can be used when creating relationships to other objects or providing a user a link to view the Sighting | 

