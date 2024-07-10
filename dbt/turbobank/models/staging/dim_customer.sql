{{ config(materialized='table', unique_key='customer_id') }}

with source as (
    select * from {{ source('raw_source', 'customers') }}
),

select
    s.id as customer_id,
    s.first_name,
    s.last_name,
    s.date_of_birth::date,
    s.phone,
    s.email,
    s.address,
    s.city,
    s.state,
    s.zip_code
from source s
