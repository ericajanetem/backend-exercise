-- Need the payloads data but it was too big so write a sample query here first
WITH success_launch AS (
    SELECT
        launch_id,
        launch_name,
        launch_rocket,
        launch_success,
        payloads,
        date_unix,
        launch_upcoming
    FROM    
        {{ ref('stg_launches') }}
    WHERE
        launch_success = true
        AND launch_upcoming = false
),

starlink_info AS (
    SELECT
        satellite_id,
        satellite_launch_id
    FROM
        {{ ref('stg_starlink')}}
),

launch_w_starlink AS (
    SELECT
        launch_id,
        launch_name,
        launch_rocket,
        launch_success,
        payloads,
        date_unix,
        launch_upcoming,
        satellite_id
    FROM
        success_launch launch_info
    JOIN
        starlink_info satellite_info
    ON
        launch_info.launch_id = satellite_info.satellite_launch_id
)

SELECT * FROM launch_w_starlink