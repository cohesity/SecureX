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
 - [Getting Started](#getting-started)
 - Supported [Atomic Actions](#atomic-actions) you can take
 - Supported [Workflows](#workflows) you can perform
 - [Minimum Permission for Helios User to generate Helios API KEY](#minimum-permission)
 - [Suggestions and Feedback](#suggest)
 - [Supported Objects](#supported)


## <a name="get-started"></a> What is SecureX :question:
[top](#Cisco-SecureX-Integration)

SecureX is a cloud-native, built-in platform that connects Cisco Secure portfolio and your infrastructure. It allows you to radically reduce dwell time and human-powered tasks. Refer to [Cisco SecureX page](https://www.cisco.com/c/en/us/products/security/securex/index.html) to know more about it.

## <a name="import"></a> Getting Started :bookmark_tabs:
[top](#Cisco-SecureX-Integration)

In order to start using the Cohesity SecureX Integration, you need to do the following.

1. [Register this Git Repo on SecureX](./docs/misc/registerGitRepo.md)

2. [Import the Atomics and Workflow using this Git Repo in SecureX](https://ciscosecurity.github.io/sxo-05-security-workflows/importing). While importing Workflows, it will automatically create a global variable for Helios API Key. Enter the Helios API Key there and you can then start using the Workflows

3. Once you have imported all the Workflows and Atomics. Next step is to run the workflows. Check the [Workflow](#workflows) section to find all *required* pre-reqs to run these workflow. 

> *Note that you will need to import Atomics and then Workflows since the Workflows depend on the Atomics.* 

To know more about importing and exporting your Workflows and Atomic Actions refer to [this video](https://www.youtube.com/watch?v=qmJk994qLOg&ab_channel=Cisco).

## <a name="atomic-actions"></a> Atomic Actions :large_blue_circle:
[top](#Cisco-SecureX-Integration)

Atomic actions are self-contained workflows that are similar to a function in traditional programming. They can consume input, perform various actions, and then return output. They’re designed to be portable, re-usable, and make building workflows more efficient. Refer to the [Atomic Actions](https://ciscosecurity.github.io/sxo-05-security-workflows/atomics/) documentation to find more. 

Lets go over the list of Atomic Actions that this integration supports. 

- [Cohesity Helios - Get Anomalous Objects](./docs/atomics/CohesityGetAnomalousObjects.md)
- [Cohesity Helios - Ignore Anomaly](./docs/atomics/CohesityIgnoreAnomaly.md)
- [Cohesity Helios - Resolve Anomalous VM](./docs/atomics/CohesityResolveAnomaly.md)
- [Cohesity Helios - Restore Anomalous VM](./docs/atomics/CohesityRestoreAnomalousVM.md)
- [Cohesity Threat Response - Create SecureX Incidents](./docs/atomics/CohesityCreateSecureXIncident.md)
- [Cohesity Threat Response - Create SecureX Sightings](./docs/atomics/CohesityCreateSecureXSighting.md)
- [Cohesity Threat Response - Create SecureX Relationship](./docs/atomics/CohesityCreateSecureXRelationship.md)
- [Cohesity Threat Response - Resolve SecureX Incident/Sighting](./docs/atomics/CohesityResolveSecureXConstruct.md)
- [Cohesity Threat Response - Delete SecureX Incident/Sighting/Relationship](./docs/atomics/CohesityDeleteSecureXConstruct.md)
- [Cohesity Threat Response - Get SecureX Incident/Sighting/Relationship](./docs/atomics/CohesityGetSecureXConstruct.md)

## <a name="workflows"></a> Workflows :hourglass_flowing_sand:
[top](#Cisco-SecureX-Integration)

Workflows are the larger component of orchestration and are similar to a script in traditional programming. A workflow can be simple and only have a few actions or be complex and string together many different actions for different products. Refer to the [Workflows](https://ciscosecurity.github.io/sxo-05-security-workflows/workflows/) documentation to find more. 

Lets go over the list of Workflows that this integration supports. 

- [Helios Ransomware Alerts to Threat Response and ServiceNow](./docs/workflows/HeliosRansomwareAlertsToThreatResponse.md)
- [Ignore Anomaly on Cohesity Helios](./docs/workflows/IgnoreAnomalyOnCohesity.md)
- [Cohesity Restore Anomalous Object](./docs/workflows/CohesityRestoreAnomalousObject.md)

## <a name="import"></a> Import Atomic Actions and Workflows :bookmark_tabs:
[top](#Cisco-SecureX-Integration)

To explore the various options available in SecureX orchestration for importing and exporting your Workflows and Atomic Actions refer to [this video](https://www.youtube.com/watch?v=qmJk994qLOg&ab_channel=Cisco).

## <a name="minimum-permission"></a> Minimum Permission for Helios API user to generate APIKey :cop:
[top](#Cisco-SecureX-Integration)

In order to run the workflow on SecureX, you need to pass Helios APIKey. The user that creates this APIKey must have the following privileges. 

* *Viewer Role*: This role is needed for the user to be able to login to Cohesity Helios and [create the APIKey.](https://developer.cohesity.com/docs/helios-getting-started)

* *Manage Protection Groups and Manage Recovery*: This role is needed to get a clean snapshot and recover the VM to the latest known safe state.

To know more about Cohesity Roles, please visit [Cohesity Product Documentation](https://docs.cohesity.com/6_5_1/Web/UserGuide/Content/Dashboard/Admin/RoleManage.htm?tocpath=Administration%7CAccess%20Management%7CRoles%7C_____0#ManageRoles). 

## <a name="suggest"></a> Supported Objects :green_book:
[top](#Cisco-SecureX-Integration)

For this release of the Integration, only Anomalous VMs are supported as Objects. More Objects from Cohesity Helios will be supported in the future. Please reach out to use for more info. 


## <a name="suggest"></a> Suggestions and Feedback :handshake:
[top](#Cisco-SecureX-Integration)

We would love to hear from you. Please send your suggestions and feedback to: [cohesity-api-sdks@cohesity.com](mailto:cohesity-api-sdks@cohesity.com)

## License

Apache 2.0
