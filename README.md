# Cisco SecureX Integration

<!--
  Title: Cisco SecureX Integration
  Description: This project is to integrate Cohesity Helios with Cisco SecureX and manage Cohesity Ransomware alerts on SecureX and take appropriate actions using SecureX dashboard.
  -->

![](docs/assets/images/cohesity_ansible.png)

## Overview

This project is to integrate Cohesity Helios with Cisco SecureX and manage Cohesity Ransomware alerts on SecureX and take appropriate actions using SecureX dashboard.

This integration leverages Cohesity REST API to interact and fetch information from the Cohesity Helios and perform actions based on alerts raised.

## Table of contents :scroll:

 - What is [Cisco SecureX](#get-started)
 - Supported [Atomic Actions](#atomic-actions) you can take
 - Supported [Workflows](#workflows) you can perform
 - How to [Import Workflows and Atomic Actions](#import)
 - [Suggestions and Feedback](#suggest)


## <a name="get-started"></a> What is SecureX :question:
[top](#Cisco-SecureX-Integration)

* SecureX is a cloud-native, built-in platform that connects our Cisco Secure portfolio and your infrastructure. It allows you to radically reduce dwell time and human-powered tasks. Refer to [Cisco SecureX page](https://www.cisco.com/c/en/us/products/security/securex/index.html) to know more about it.

## <a name="atomic-actions"></a> Atomic Actions :large_blue_circle:
[top](#Cisco-SecureX-Integration)

Atomic actions are self-contained workflows that are similar to a function in traditional programming. They can consume input, perform various actions, and then return output. They’re designed to be portable, re-usable, and make building workflows more efficient. Refer to the [Atomic Actions](https://ciscosecurity.github.io/sxo-05-security-workflows/atomics/) documentation to find more. 

Lets go over the list of Atomic Actions that this integration supports. 

- [Cohesity Helios - Get Anomalous Objects](#get-anomalous-objects)
- [Cohesity Helios - Restore Anomalous VM](#restore-anomalous-objects)
- [Cohesity Helios - Ignore Anomaly](#ignore-anomaly)

### <a name="get-anomalous-objects"></a> Cohesity Helios - Get Anomalous Objects 
[top](#Cisco-SecureX-Integration)

This atomic action executes a python script to fetch the list of anomalous objects from Cohesity Helios. 

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Start Time | String | Objects created after this time will be fetched   | Yes | 
| End Time | String | Objects created before this time will be fetched | Yes | 

##### Output

| **Argument Name** | **Type** | **Description** |
| --- | --- | --- |
| Anomalous Objects Json | json  | The json object with holds the anomalous objects fetched from Cohesity Helios | 

### <a name="restore-anomalous-objects"></a> Cohesity Helios - Restore Anomalous VM
[top](#Cisco-SecureX-Integration)

This Atomic Action performs a restore operation for the specified anomalous VM to latest clean snapshot. Currently only VMware VMs are supported

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| VM Object | JSON | The VM object that needs to be restored   | Yes | 

##### Output

| **Argument Name** | **Type** | **Description** |
| --- | --- | --- |
| Restored VM Object  | JSON  | The restored VM object that was restored to the latest snapshot | 


### <a name="ignore-anomaly"></a> Cohesity Helios - Ignore Anomaly
[top](#Cisco-SecureX-Integration)

This Atomic Action ignores the anomaly which removes the anomalous object from the list of anomalous object. 

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| VM Object | JSON| The VM object that needs to be Ignored   | Yes | 

##### Output

N/A

## <a name="workflows"></a> Workflows :hourglass_flowing_sand:
[top](#Cisco-SecureX-Integration)

Workflows are the larger component of orchestration and are similar to a script in traditional programming. A workflow can be simple and only have a few actions or be complex and string together many different actions for different products. Refer to the [Workflows](https://ciscosecurity.github.io/sxo-05-security-workflows/workflows/) documentation to find more. 

> All the input to the workflows are passed as Global Variables.

Lets go over the list of Workflows that this integration supports. 

- [Helios Ransomware Alerts to SecureX and ServiceNow](#get-alerts-to-securex)
- [Push Helios Ransomware Alerts to Private Intelligence](#push-alerts-to-pi)
- [Ignore Anomaly on Cohesity Helios](#ignore-anomaly-workflow)
- [Cohesity Restore Anomalous Object](#restore-anomaly)
- [Push All Helios Ransomware Alerts to Private Intelligence](#push-all-anomaly)

### <a name="get-alerts-to-securex"></a> Helios Ransomware Alerts to SecureX and ServiceNow 
[top](#Cisco-SecureX-Integration)

This workflow pushes Cohesity Helios ransomware alerts to Threat Response Private Intelligence data store and also creates incidents on ServiceNow at regular intervals based on the schedule you define. 

This workflow can also be triggered based on a schedule. The schedule that is used here is `Cohesity Helios Ransomware Data Push Schedule` which is a schedule to trigger orchestration workflow to push Helios ransomware data to private intelligence.

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Threat Response API Client Id | Secure String | Threat Response API Client ID | Yes | 
| Threat Response API Client Password | Secure String | Threat Response API Client Password | Yes | 
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Cohesity Helios Ransomware Alerts Filter  | String | Number of hours, used to get anomalous objects detected in the last `N` hours| Yes | 
| Create ServiceNow Incidents | String | Set this variable to `yes` or `no` based on which ServiceNow incidents will be created | No | 

##### Output

N/A

### <a name="push-alerts-to-pi"></a> Push Helios Ransomware Alerts to Private Intelligence
[top](#Cisco-SecureX-Integration)

This workflow pushes Cohesity Helios ransomware alerts detected in the last `N` hours to Threat Response private intelligence data store. 


This workflow can also be triggered based on a schedule. The schedule that is used here is `Cohesity Helios Ransomware Data Push Schedule` which is a schedule to trigger orchestration workflow to push Helios ransomware data to private intelligence.

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Threat Response API Client Id | Secure String | Threat Response API Client ID | Yes | 
| Threat Response API Client Password | Secure String | Threat Response API Client Password | Yes | 
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Cohesity Helios Ransomware Alerts Filter  | String | Number of hours, used to get anomalous objects detected in the last `N` hours| Yes | 

##### Output

N/A


### <a name="ignore-anomaly-workflow"></a> Ignore Anomaly on Cohesity Helios
[top](#Cisco-SecureX-Integration)

This workflow ignores anomaly on for the specified object on Helios which removes this object from the list of anomalous objects. 

> This is an Response workflows. 

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Threat Response API Client Id | Secure String | Threat Response API Client ID | Yes | 
| Threat Response API Client Password | Secure String | Threat Response API Client Password | Yes | 
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Cohesity Delete Sighting | String | Specifies where to delete or not the sighting once the anomaly is ignored. Can be `yes` or `no`. | Yes | 

##### Output

N/A

### <a name="restore-anomaly"></a> Cohesity Restore Anomalous Object
[top](#Cisco-SecureX-Integration)

This workflow restores the specified anomalous object to the latest clean snapshot

> This is an Response workflows. 

##### Input 

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Threat Response API Client Id | Secure String | Threat Response API Client ID | Yes | 
| Threat Response API Client Password | Secure String | Threat Response API Client Password | Yes | 
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 
| Delete | String | Specifies where to delete or not the sighting once the anomaly is ignored. Can be `yes` or `no`. | Yes | 

##### Output

N/A

### <a name="push-all-anomaly"></a> Push All Helios Ransomware Alerts to Private Intelligence
[top](#Cisco-SecureX-Integration)

This Workflow pushes all helios ransomware alerts to Threat Response private intelligence data store. This does not create ServiceNow incidents for the alerts in Cohesity Helios. 

##### Input

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Threat Response API Client Id | Secure String | Threat Response API Client ID | Yes | 
| Threat Response API Client Password | Secure String | Threat Response API Client Password | Yes | 
| Cohesity Helios API Key | Secure String | API Key to access Helios | Yes | 

##### Output

N/A

## <a name="import"></a> Import Atomic Actions and Workflows :bookmark_tabs:
[top](#Cisco-SecureX-Integration)

To explore the various options available in SecureX orchestration for importing and exporting your Workflows and Atomic Actions refer to [this video](https://www.youtube.com/watch?v=qmJk994qLOg&ab_channel=Cisco).

## <a name="suggest"></a> Suggestions and Feedback :handshake:
[top](#Cisco-SecureX-Integration)

We would love to hear from you. Please send your suggestions and feedback to: [cohesity-api-sdks@cohesity.com](mailto:cohesity-api-sdks@cohesity.com)

## License

Apache 2.0
