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

- [Cohesity Helios - Get Anomalous Objects](./docs/atomics/CohesityGetAnomalousObjects.md)
- [Cohesity Helios - Restore Anomalous VM](./docs/atomics/CohesityRestoreAnomalousVM.md)
- [Cohesity Helios - Ignore Anomaly](./docs/atomics/CohesityIgnoreAnomaly.md)


## <a name="workflows"></a> Workflows :hourglass_flowing_sand:
[top](#Cisco-SecureX-Integration)

Workflows are the larger component of orchestration and are similar to a script in traditional programming. A workflow can be simple and only have a few actions or be complex and string together many different actions for different products. Refer to the [Workflows](https://ciscosecurity.github.io/sxo-05-security-workflows/workflows/) documentation to find more. 

Lets go over the list of Workflows that this integration supports. 

- [Helios Ransomware Alerts to Threat Response and ServiceNow](./docs/workflows/HeliosRansomwareAlertsToThreatResponseAndServiceNow.md)
- [Ignore Anomaly on Cohesity Helios](./docs/workflows/IgnoreAnomalyOnCohesity.md)
- [Cohesity Restore Anomalous Object](./docs/workflows/CohesityRestoreAnomalousObject.md)


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
