## <a name="create-securex-incident"></a> Cohesity Threat Response - Create SecureX Incidents
[home](../../README.md)

This atomic action creates a Cisco Threat Response Incident object. This is used in the [Cohesity Helios: Get Anomalous Objects v1.2 workflow](../workflows/HeliosRansomwareAlertsToThreatResponse.md). Refer [Cisco Github](https://github.com/threatgrid/ctim/tree/master/doc) to find more about it. 

### Input

When you run this Atomic action, it will ask for the following input. 

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Access Token | Secure String | An access token for the Threat Response API. This is often obtained using the "Threat Response - Generate Access Token" atomic | Yes | 
| External ID | String | External ID can be used to uniquely identify the SecureX Incident   | Yes | 
| Incident Confidence | String | Must be one of the following: Medium, Info, Unknown, None, High, or Low | Yes | 
| Incident Description | String | This can be a string of plain text or can be formatted with Markdown | No | 
| Incident Source | String | Source from where this incident was created. Default is `Cohesity Helios` in this case | No | 
| Incident Status | String | Must be one of the following: New, Closed, Rejected, Open, Restoration Achieved, Incident Reported, Stalled, or Containment Achieved | Yes | 
| Incident Title | String | A short title for the incident | Yes | 
| TLP Value | String | The traffic light protocol value to give this incident. Valid values include: red, amber, green, and white. See: https://www.cisa.gov/tlp | Yes | 

### Output

This Atomic actions gives out the following output that you can use to perform operations like resolving or deleting the Incident.

| **Argument Name** | **Type** | **Description** |
| --- | --- | --- |
| Incident ID | String  | The ID of the new incident. This can be used when creating relationships to other objects or providing a user a link to view the incident | 

