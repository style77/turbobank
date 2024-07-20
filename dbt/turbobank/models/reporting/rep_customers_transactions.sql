{{ config(materialized='incremental', unique_key='transaction_id') }}

WITH customer_transactions AS (
    SELECT 
        ft.transaction_id,
        ft.created_at as transaction_date,
        ft.amount as transaction_amount,
        dtt.transaction_type,
        dc.customer_id,
        CONCAT(dc.first_name, ' ', dc.last_name) as customer_name,
        da.account_id
    FROM {{ ref('fact_transaction') }} ft
    LEFT JOIN {{ ref('dim_account') }} da ON ft.account_id = da.account_id
    LEFT JOIN {{ ref('dim_customer') }} dc ON da.customer_id = dc.customer_id
    LEFT JOIN {{ ref('dim_transaction' ) }} dt ON ft.transaction_id = dt.transaction_id
    LEFT JOIN {{ ref('transaction_types') }} dtt ON dt.transaction_type_id = dtt.id
)

SELECT 
    transaction_id,
    transaction_date,
    transaction_amount,
    transaction_type,
    customer_id,
    customer_name,
    account_id
FROM customer_transactions