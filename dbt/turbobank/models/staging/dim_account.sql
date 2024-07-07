{{ config(materialized='table', unique_key='account_id') }}

select
    id as account_id,
    account_number,
    customer_id,
    account_type,
    balance
from {{ source('raw_source', 'accounts') }}