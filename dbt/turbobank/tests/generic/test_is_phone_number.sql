{% test is_phone_number(model, column_name) %}

with validation as (

    select
        {{ column_name }} as phone_field

    from {{ model }}

),

validation_errors as (

    select
        phone_field

    from validation
    -- Remember, we are looking for phone numbers with 9 digits only as the turbobank
    -- simulation is meant to be a simplified version of a real bank in POLAND
    -- (We use 9 digits phone numbers there ;D)
    where phone_field ~ '^[[:digit:]]{9}$'

)

select *
from validation_errors

{% endtest %}