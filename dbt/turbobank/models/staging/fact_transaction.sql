{{ config(materialized='table', unique_key='transaction_id') }}

select
    id as transaction_id,
    account_id,
    (select transaction_type_id from {{ ref('dim_transaction_type') }} where transaction_type = t.transaction_type limit 1) as transaction_type_id,
    (select transaction_description_id from {{ ref('dim_transaction_description') }} where transaction_description = t.description limit 1) as transaction_description_id,
    amount,
    created_at::date as created_at
from {{ source('raw_source', 'transactions') }} t
