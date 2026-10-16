-- Vista normalizada para cargas de tracking_plan.csv en las que BigQuery
-- haya importado el encabezado como una fila y creado nombres genéricos.
CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_tracking_plan` AS
SELECT
  string_field_0 AS event_name,
  string_field_1 AS trigger,
  string_field_2 AS key_parameters,
  string_field_3 AS business_purpose
FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.tracking_plan`
WHERE string_field_0 <> 'event_name';
