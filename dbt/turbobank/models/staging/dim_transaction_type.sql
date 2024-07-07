{{ config(materialized='table', unique_key='transaction_type_id') }}

select
    id as transaction_type_id,
    transaction_type
from (
    select distinct
        row_number() over (order by transaction_type) as id,
        transaction_type
    from {{ source('raw_source', 'transactions') }}
) distinct_transaction_types