## Knoetic Backend Exercise

### Key Guiding Question:

> 👨🏼‍🦳 When will there be 42,000 Starlink satellites in orbit, and how many more launches will it take to get there?
> 

**Exploring the API:** https://github.com/r-spacex/SpaceX-API/blob/master/docs/README.md

> [**Starlink](https://github.com/r-spacex/SpaceX-API/blob/master/docs/starlink) - Detailed info about Starlink satellites and orbits**
> 
> 
> Includes raw orbit data from [Space Track](https://www.space-track.org/auth/login), updated hourly.
> 
> Space Track data adheres to the standard for [Orbit Data Messages](https://public.ccsds.org/Pubs/502x0b2c1e2.pdf)
> 

<br>
<br>

#### **Data Analysis & Modelling**

- Data Analysis: Understanding the data from SpaceX:
    - Found this data analysis that gives insight into the data from the various endpoints: https://www.kaggle.com/code/dilarabr/insights-into-spacex-using-api-v4
    
    In particular, there are three that stands out: 
    
    1. Payloads: Identifies the payload or purpose of each launch rocket mission. In this case, since we are need to analyze the number of launches till a certain x number of satellites are in orbit, we need to use payload to identify the launches that contains satellites and how many satellites it contains.
    2. Starlink: The operational status of the Starlink satellite, including information of its launch.
    3. Launches: The historical launch data, including information of the payload of each launch, the launch status.
    
    Connecting the data together:
    
    - Launch ID ↔ [Payload.launch.ID](http://Payload.launch.ID) ↔ Starlink.launch.id

<br>

#### **Utilising the Custom Connector:**

In Airbyte, set up the custom connector through Docker connection:

Dockerhub Link: https://hub.docker.com/layers/olices/spacex-explorer/dev/images/sha256:a0a59bea2d76a323b61f896ec3475660fb2aa33952816679a69b2f0d849dbcbf?tab=vulnerabilities

```
Docker repository name: olices/spacex-explorer
Docker image tag: dev
```



#### **Future considerations:**

As the data size is still very small for the endpoints, I only implemented full refresh sync at the moment. As the data size grows, there are some additional considerations: 

1. Incremental Stream: Save resources reading only new data, querying using a start and endpoint also allows for historical data backfilling. Also consider, append + deduped to prevent primary key duplications.
2. Pagination: Instead of retrieving ‘all’ data, use the ‘query’ endpoint and utilises pagination to prevent from querying too large a data size.
3. Column Selection: only select fields of interest to be sync to the database instead of all the fields

<br>

**Postgres Database:**

[Supabase](https://supabase.com/) was selected as the postgres database for this project.

<br>

Supabase Postgres Database:

![image](https://github.com/ericajanetem/backend-exercise/assets/48477045/18a34fde-4500-4856-88c5-e49616587cc5)

<br>
Airbytes Connection:

![image](https://github.com/ericajanetem/backend-exercise/assets/48477045/24ba008b-b829-4ebf-8130-7e7dac444051)

<br>

#### **DBT**

DBT is used for the Transformation step, and orchestrated using Airflow [WIP].

#### **Future considerations:**
1. Quality Testing using DBT: Using DBT for [Quality Testing](https://www.getdbt.com/blog/data-quality-testing) to ensure that the extracted data is validated and the transformed data meets quality development standards (no duplication of primary keys, no empty strings or null values, row count number is normal).


<br>

#### **Airflow**

Airflow will work as the orchestrator for the entire project’s ELT pipeline and ensure that the transformation step using DBT is triggered per schedule upon completion of each sync. Airbytes and Airflow can be integrated together using this guide (https://airbyte.com/tutorials/how-to-use-airflow-and-airbyte-together#airbyte-and-apache-airflow-together). 

Using Airflow as the orchestrator allows for the entire pipeline flow to be tracked at a glance for both the Airbytes Extract & Load processes and DBT transformation models.

<br>
<br>

#### **Answering the key question:**

> 👨🏼‍🦳 When will there be 42,000 Starlink satellites in orbit, and how many more launches will it take to get there?
> 

1. Using the data from launches and starlink, form a final data set with the launch id, starlink id and other relevant fields by doing a join of the launch.d with starlink.launch_id. 
2. Filter the data based on the launch status (success/failure, upcoming/completed launch) and the satellite's operational status.
3. Using this data, use time series modelling to forecast the rate of future launches (frequency of launch) and the number of Starlink satellites per launch.
4. Display the results of the data using a data visualisation tool such as Tableau.
