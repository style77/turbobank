{{ config(materialized='table', unique_key='customer_id') }}

with source as (
    select * from {{ source('raw_source', 'customers') }}
),
address_mapping as (
    select
        s.id as customer_id,
        dca.address_id
    from source s
    join {{ ref('dim_customer_address') }} dca
    on s.address = dca.address
    and s.city = dca.city
    and s.state = dca.state
    and s.zip_code = dca.zip_code
)

select
    s.id as customer_id,
    am.address_id,
    s.first_name,
    s.last_name,
    s.date_of_birth::date,
    s.phone,
    s.email
from source s
join address_mapping am
    on s.id = am.customer_id
