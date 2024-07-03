with

source as (

    select * from {{ source('public', 'starlink') }}

),

renamed as (
    select
        id as satellite_id,
        launch as satellite_launch_id
    from source
)

select * from renamed
