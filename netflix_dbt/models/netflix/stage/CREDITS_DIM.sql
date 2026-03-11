SELECT 
* 
FROM {{ source('netflix', 'CREDITS') }}
WHERE ROLE IN ('ACTOR','DIRECTOR')