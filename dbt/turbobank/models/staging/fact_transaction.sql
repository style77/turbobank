{{ config(materialized='table', unique_key='transaction_id') }}

select
    t.id as transaction_id,
    t.account_id,
    dt.transaction_id as transaction_meta_id,
    t.amount,
    t.created_at::date as created_at
from {{ source('raw_source', 'transactions') }} t
left join {{ ref('dim_transaction') }} dt
    on t.id = dt.transaction_id