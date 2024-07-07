{{ config(materialized='table', unique_key='address_id') }}

with address_data as (
    select
        address,
        city,
        state,
        zip_code,
        row_number() over (order by address, city, state, zip_code) as address_id
    from (
        select distinct
            address,
            city,
            state,
            zip_code
        from {{ source('raw_source', 'customers') }}
    ) distinct_addresses
)

select
    address_id,
    address,
    city,
    state,
    zip_code
from address_data
