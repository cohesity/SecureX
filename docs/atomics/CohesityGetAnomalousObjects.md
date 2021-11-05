## <a name="get-anomalous-objects"></a> Cohesity Helios - Get Anomalous Objects 
[home](../../README.md)

This atomic perform a fetch operation which gets the list of anomalous objects from Cohesity Helios. This Atomic action gets all the alerts and creates an array of alerts that can be used to create other workflows. This is used in the [Cohesity Helios: Get Anomalous Objects v1.2 workflow](). 

### Input

When you run this Atomic action, it will ask for the following input. 

| **Argument Name** | **Type** | **Description** | **Required** |
| --- | --- |--- | --- |
| HeliosAPIKey | Secure String | API Key to access Cohesity Helios | Yes | 
| Start Time | String | Anomalous Object Alerts created after this time will be fetched. This time is an EPOCH timestamp in microseconds   | No | 
| End Time | String | Anomalous Object Alerts created before this time will be fetched. This time is an EPOCH timestamp in microseconds | No | 

### Output

This Atomic actions gives out the following output that you can use to perform operations like resolving these objects, restoring the anomalous objects etc. 

| **Argument Name** | **Type** | **Description** |
| --- | --- | --- |
| HeliosAlertsArray | String  | The Array of json object (a JSON string) with holds the anomalous objects fetched from Cohesity Helios | 

Below is the sample array that is presented by this output variable. 

```
[{
    "shortDescription": "",
    "description": "",
    "alert_id": "",
    "entity_id": "",
    "job_id": "",
    "parent_id": "",
    "job_instance_id": "",
    "cluster_incarnation_id": "",
    "object_id": "",
    "job_start_time_usecs": "",
    "cluster_id": "",
    "external_id": "",
    "title": "",
    "object": "",
    "start_time": "",
    "end_time": "",
    "incident_description": "",
    "source_name": "",
    "sighting_description": "",
    "observables": [
      {
        "type": "hostname",
        "value": "VALUE"
      }
    ]
  }]
```

