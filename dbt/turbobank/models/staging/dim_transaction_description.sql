{{ config(materialized='table', unique_key='transaction_description_id') }}

select
    id as transaction_description_id,
    description as transaction_description
from (
    select distinct
        row_number() over (order by description) as id,
        description
    from {{ source('raw_source', 'transactions') }}
) distinct_transaction_descriptions