### <a name="get-alerts-to-securex"></a> Helios Ransomware Alerts to Threat Response and ServiceNow 
[top](#Cisco-SecureX-Integration)

This workflow pushes Cohesity Helios ransomware alerts to Threat Response Private Intelligence data store, creates SecureX Incidents, Sightings and a Relationship between them. It also creates incidents on ServiceNow at regular intervals based on the schedule you define. 

This workflow has to be triggered on a schedule and user has to create `Cohesity Helios Ransomware Data Push Schedule` for this to work which is a schedule to trigger orchestration workflow to push Helios ransomware data to private intelligence.

> Note: This workflow also needs creation of 'ServiceNow_Credentials' under Account Keys and 'Cohesity_ServiceNow_Target' under Targets. These are needed for creating incidents on service now.

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Threat Response API Client Id | Secure String | Threat Response API Client ID | Yes | 
| Threat Response API Client Password | Secure String | Threat Response API Client Password | Yes | 
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Cohesity Helios Ransomware Alerts Filter  | String | Number of hours, used to get anomalous objects detected in the last `N` hours| Yes | 
| Create ServiceNow Incidents | String | Set this variable to `yes` or `no` based on which ServiceNow incidents will be created | Yes | 

##### Output

N/A