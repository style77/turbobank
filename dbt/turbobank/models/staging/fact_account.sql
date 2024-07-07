{{ config(materialized='table', unique_key='account_id') }}

select
    id as account_id,
    customer_id,
    balance,
    created_at::date
from {{ source('raw_source', 'accounts') }}
