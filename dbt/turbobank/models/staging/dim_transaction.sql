{{ config(materialized='table', unique_key='transaction_id') }}

select
    id as transaction_id,
    transaction_type
from (
    select distinct
        id as transaction_id,
        transaction_type
    from {{ source('raw_source', 'transactions') }}
) distinct_transactions