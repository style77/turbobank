{{ config(materialized='table', unique_key='transaction_id') }}

select
    t.id as transaction_id,
    t.account_id,
    dt.transaction_id as dim_transaction_id,
    dtt.transaction_type_id,
    dtd.transaction_description_id,
    t.amount,
    t.created_at::date as created_at
from {{ source('raw_source', 'transactions') }} t
join {{ ref('dim_transaction') }} dt
    on t.transaction_type = dt.transaction_type