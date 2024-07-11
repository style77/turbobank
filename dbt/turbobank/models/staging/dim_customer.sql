{{ config(materialized='table', unique_key='customer_id') }}

select
    id as customer_id,
    first_name,
    last_name,
    date_of_birth::date,
    phone,
    email,
    address,
    city,
    state,
    zip_code
from {{ source('raw_source', 'customers') }}
