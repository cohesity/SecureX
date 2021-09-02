# Cisco SecureX Integration

<!--
  Title: Cisco SecureX Integration
  Description: This project is to integrate Cohesity Helios with Cisco SecureX and manage Cohesity Ransomware alerts on SecureX and take appropriate actions using Threat Response.
  -->

![](docs/assets/images/cohesity_ansible.png)

## Overview

This project is to integrate Cohesity Helios with Cisco SecureX and manage Cohesity Ransomware alerts on SecureX and take appropriate actions using Threat Response.

This integration leverages Cohesity REST API to interact and fetch information from the Cohesity Helios and perform actions based on alerts raised.

## Table of contents :scroll:

 - What is [Cisco SecureX](#get-started)
 - Supported [Atomic Actions](#atomic-actions) you can take
 - Supported [Workflows](#workflows) you can perform
 - How to [Import Workflows and Atomic Actions](#import)
 - [Minimum Permission for Helios User to generate APIKEY](#minimum-permission)
 - [Suggestions and Feedback](#suggest)


## <a name="get-started"></a> What is SecureX :question:
[top](#Cisco-SecureX-Integration)

* SecureX is a cloud-native, built-in platform that connects Cisco Secure portfolio and your infrastructure. It allows you to radically reduce dwell time and human-powered tasks. Refer to [Cisco SecureX page](https://www.cisco.com/c/en/us/products/security/securex/index.html) to know more about it.

## <a name="atomic-actions"></a> Atomic Actions :large_blue_circle:
[top](#Cisco-SecureX-Integration)

Atomic actions are self-contained workflows that are similar to a function in traditional programming. They can consume input, perform various actions, and then return output. They’re designed to be portable, re-usable, and make building workflows more efficient. Refer to the [Atomic Actions](https://ciscosecurity.github.io/sxo-05-security-workflows/atomics/) documentation to find more. 

Lets go over the list of Atomic Actions that this integration supports. 

- [Cohesity Helios - Get Anomalous Objects](#get-anomalous-objects)
- [Cohesity Helios - Restore Anomalous VM](#restore-anomalous-objects)
- [Cohesity Helios - Ignore Anomaly](#ignore-anomaly)

### <a name="get-anomalous-objects"></a> Cohesity Helios - Get Anomalous Objects 
[top](#Cisco-SecureX-Integration)

This atomic perform a fetch operation which gets the list of anomalous objects from Cohesity Helios. 

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Start Time | String | Anomalous Object Alerts created after this time will be fetched. This time is an EPOCH timestamp in microseconds   | No | 
| End Time | String | Anomalous Object Alerts created before this time will be fetched. This time is an EPOCH timestamp in microseconds | No | 

##### Output

| **Argument Name** | **Type** | **Description** |
| --- | --- | --- |
| Anomalous Objects Json | String  | The json object (a JSON string) with holds the anomalous objects fetched from Cohesity Helios | 

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


### <a name="ignore-anomaly"></a> Cohesity Helios - Ignore Anomaly
[top](#Cisco-SecureX-Integration)

This Atomic Action ignores the anomaly which removes the anomalous object from the list of anomalous object. This suppresses the anomalous object alert on Cohesity Helios.

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Object | String | The VM Object name that needs to be Ignored   | Yes | 

##### Output

N/A

## <a name="workflows"></a> Workflows :hourglass_flowing_sand:
[top](#Cisco-SecureX-Integration)

Workflows are the larger component of orchestration and are similar to a script in traditional programming. A workflow can be simple and only have a few actions or be complex and string together many different actions for different products. Refer to the [Workflows](https://ciscosecurity.github.io/sxo-05-security-workflows/workflows/) documentation to find more. 

> All the input to the workflows are passed as Global Variables.

Lets go over the list of Workflows that this integration supports. 

- [Helios Ransomware Alerts to Threat Response and ServiceNow](#get-alerts-to-securex)
- [Ignore Anomaly on Cohesity Helios](#ignore-anomaly-workflow)
- [Cohesity Restore Anomalous Object](#restore-anomaly)

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

## <a name="import"></a> Import Atomic Actions and Workflows :bookmark_tabs:
[top](#Cisco-SecureX-Integration)

To explore the various options available in SecureX orchestration for importing and exporting your Workflows and Atomic Actions refer to [this video](https://www.youtube.com/watch?v=qmJk994qLOg&ab_channel=Cisco).

## <a name="minimum-permission"></a> Minimum Permission for Helios API user to generate APIKey :cop:
[top](#Cisco-SecureX-Integration)

In order to run the workflow on SecureX, you need to pass Helios APIKey. The user that creates this APIKey must have the following privileges. 

* *Viewer Role*: This role is needed for the user to be able to login to Cohesty Helios and [create the APIKey.](https://developer.cohesity.com/docs/helios-getting-started)

* *Manage Protection Groups and Manage Recovery*: This role is needed to get a clean snapshot and recoever the VM to latest know safe state. 

To know more about Cohesity Roles, please visit [Cohesity Product Documentation](https://docs.cohesity.com/6_5_1/Web/UserGuide/Content/Dashboard/Admin/RoleManage.htm?tocpath=Administration%7CAccess%20Management%7CRoles%7C_____0#ManageRoles). 

## <a name="suggest"></a> Suggestions and Feedback :handshake:
[top](#Cisco-SecureX-Integration)

We would love to hear from you. Please send your suggestions and feedback to: [cohesity-api-sdks@cohesity.com](mailto:cohesity-api-sdks@cohesity.com)

## License

Apache 2.0
