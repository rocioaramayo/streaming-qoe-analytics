-- Vistas para la página "Predicción y prevención" de Looker Studio.
-- Cargar antes los CSV de data/ con los nombres de tabla indicados.

CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_ml_risk_dashboard` AS
SELECT
  user_pseudo_id,
  session_id,
  TIMESTAMP(window_end_ts) AS window_end_ts,
  platform,
  subscription_tier,
  connection_type,
  amba_zone_id,
  SAFE_CAST(latency_last AS FLOAT64) AS latency_last,
  SAFE_CAST(latency_mean AS FLOAT64) AS latency_mean,
  SAFE_CAST(bitrate_last AS FLOAT64) AS bitrate_last,
  SAFE_CAST(bitrate_mean AS FLOAT64) AS bitrate_mean,
  SAFE_CAST(wifi_last AS FLOAT64) AS wifi_last,
  SAFE_CAST(wifi_mean AS FLOAT64) AS wifi_mean,
  SAFE_CAST(microcut_next_5m AS INT64) AS actual_microcut,
  SAFE_CAST(microcut_risk_probability AS FLOAT64) AS microcut_risk_probability,
  SAFE_CAST(microcut_risk_probability AS FLOAT64) * 100 AS microcut_risk_pct,
  SAFE_CAST(predicted_microcut AS INT64) AS predicted_microcut,
  risk_level,
  evaluation_split
FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.ml_microcut_risk_predictions`;

CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_ml_diagnosis_dashboard` AS
SELECT
  incident_id,
  user_pseudo_id,
  platform,
  subscription_tier,
  connection_type,
  amba_zone_id,
  SAFE_CAST(wifi_rssi_dbm AS FLOAT64) AS wifi_rssi_dbm,
  SAFE_CAST(live_latency_ms AS FLOAT64) AS live_latency_ms,
  SAFE_CAST(bitrate_kbps AS FLOAT64) AS bitrate_kbps,
  SAFE_CAST(stall_duration_ms AS FLOAT64) AS stall_duration_ms,
  diagnosed_cause AS actual_cause,
  predicted_cause,
  SAFE_CAST(prediction_confidence AS FLOAT64) AS prediction_confidence,
  SAFE_CAST(prediction_confidence AS FLOAT64) * 100 AS prediction_confidence_pct,
  SAFE_CAST(correct_prediction AS INT64) AS correct_prediction,
  evaluation_split
FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.ml_diagnosis_predictions`;

CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_ml_model_metrics` AS
SELECT
  model_name,
  metric_name,
  SAFE_CAST(metric_value AS FLOAT64) AS metric_value,
  SAFE_CAST(metric_value AS FLOAT64) * 100 AS metric_pct,
  dataset_type,
  model_version
FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.ml_model_metrics`;
