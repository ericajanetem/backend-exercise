with

source as (

    select * from {{ source('public', 'launches') }}

),

renamed as (
    select
        id as launch_id,
        name as launch_name,
        rocket as launch_rocket,
        success as launch_success,
        payloads as payloads,
        date_unix,
        date_utc,
        date_local,
        upcoming as launch_upcoming
    from source

)

select * from renamed
