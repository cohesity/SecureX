## Table of contents :scroll:

 - [Intro](#intro)
 - [Pre-requisites](#pre-req)
    * [Create SecureX API Client](#securex-client)
    * [Create Cohesity Helios API Key](#helios-client)
    * [Set Variables](#set-variables)
    * [Create Schedule](#create-schedule)
    * [Create ServiceNow Credentials](#create-snow-cred)
    * [Create ServiceNow Target](#create-snow-target)
 - [How to Run](#run)
 - [Input to this workflow](#input)
 - [Output for workflow](#output)
 - [What's Next!](#next)

### <a name="intro"></a> Helios Ransomware Alerts to Threat Response and ServiceNow (Optional)
[home](../../README.md)

This workflow pushes Cohesity Helios ransomware alerts to Threat Response Private Intelligence data store, creates SecureX Incidents, Sightings and a Relationship between them. It optionally also creates incidents on ServiceNow.

This workflow can be triggered on a schedule and user can create `Cohesity Helios Ransomware Data Push Schedule` for this to work which is a schedule to trigger orchestration workflow to push Helios ransomware data to private intelligence.

> Note: If you choose to create ServiceNow Incidents, then this workflow also needs creation of 'ServiceNow_Credentials' under Account Keys and 'Cohesity_ServiceNow_Target' under Targets. These are needed for creating incidents on service now.

### <a name="pre-req"></a> Pre-requisites
[home](../../README.md)

Before you can run this workflow, there are a certain pre-req that you need to configure. Lets go over all of them and make sure they are set to get started. Most of the steps are common between all the workflows, so once you set configure these, you will be able to easily configure and run other workflows :)

#### <a name="helios-client"></a> Create Cohesity Helios API Key

In order to run the workflow on SecureX, you need to pass Helios APIKey. To create it, login to Cohesity Helios and [create the APIKey.](https://developer.cohesity.com/docs/helios-getting-started)

#### <a name="set-variables"></a> Create Global Helios API Key Variable

Create a [Global variable to set Cohesity Helios API Key](../misc/CreateHeliosAPIKey.md). 

This workflow also use some local variables. These variables should be set to default but can be changed before you try and run this workflow. Below is the list of variables that you can edit.  

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| Helios API Key | Secure String | API Key to access Helios. This is set globally | Yes | 
| HeliosRansomwareAlertsFilter  | String | Number of hours, used to get anomalous objects detected in the last `N` hours| No. Default is `250` | 
| Create ServiceNow Ticket | String | Set this variable to `yes` or `no` based on which ServiceNow incidents will be created | No. Default is `no` | 

In order to set this variables, check the [Set Variables document](../misc/SetVariables.md). Now let's move the next pre-req.

#### <a name="create-schedule"></a> Create Schedule

Once the variables are set, you need to create a Schedule on SecureX. This schedule will define the cadence of this workflow. For example you would want to run this workflow everyday at 9 PM PST. In that case, you can create a Schedule for that and that will run periodically and get the list of Anomalous objects everyday so that you can take action on it. 

This workflow looks for a Schedule named `Cohesity Helios Ransomware Data Push Schedule`. Please check the [Create Schedule Document](../misc/CreateSchedule.md) to see how to create this Schedule. 

#### <a name="create-snow-cred"></a> Create ServiceNow Credentials 

If you set the `Create ServiceNow Ticket` variable to `Yes`, then one more pre-req for this workflow is to Create ServiceNow credentials. This is needed if you want to create ServiceNow ticket for any anomalous object that is reported by Cohesity. 

Check the Create [ServiceNow Credentials document](../misc/CreateServiceNowCredentials.md) to know how to do that. 

#### <a name="create-snow-target"></a> Create ServiceNow Target

The last pre-req to run this workflow is to Create ServiceNow Target. Here is where you define your ServiceNow instance details where the ServiceNow tickets will be created. 

Check the Create [ServiceNow Target document](../misc/CreateServiceNowTarget.md) to know how to do that. 

### <a name="run"></a> How to Run
[home](../../README.md)

Once you have performed all the [pre-req](#pre-req) for this workflow, you can now go ahead run this workflow. Now as mentioned before, this workflow will run using the [Schedule](#create-schedule) that we created earlier. But if you want to run this workflow ad-hoc and not wait for the schedule, you can directly run this workflow as shown below. Please make sure that all the [pre-req](#pre-req) are taken care of. 

1. Login to your SecureX account and go to Orchestration

    ![Go to Orchestration](../assets/orchestration.png)

2. Select Workflow from the left Nav bar

     ![Select Workflow](../assets/runWorkflow01.png)

3. Run the workflow as shown below. 

    ![Run Workflow](../assets/runWorkflow02.png)

###  <a name="input"></a> Input

Input to these workflows can be referred to under [Set Variables](#set-variables) section

###  <a name="output"></a> Output

N/A

### <a name="next"></a> What's Next!
[home](../../README.md)

After you have executed this workflow, the anomalous objects reported by Cohesity Helios will be pushed into SecureX Threat Response as Incidents and you can perform 2 operations on these Incidents. They are,

1. [Ignore Anomaly](./IgnoreAnomalyOnCohesity.md)
2. [Restore to Object to latest known safe snapshot](./CohesityRestoreAnomalousObject.md)
