{{ config(materialized='table', unique_key='transaction_id') }}

WITH transactions AS (
    SELECT
        id as transaction_id,
        transaction_type
    FROM {{ source('raw_source', 'transactions') }}
)

SELECT
    t.transaction_id,
    tt.id as transaction_type_id
FROM transactions t
LEFT JOIN {{ ref('transaction_types') }} tt
ON t.transaction_type = tt.transaction_type
