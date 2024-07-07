{% test is_email_address(model, column_name) %}

with validation as (
    
    select
        {{ column_name }} as email_field

    from {{ model }}

),

validation_errors as (

    select
        email_field

    from validation
    where not email_field ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

)

select *
from validation_errors

{% endtest %}