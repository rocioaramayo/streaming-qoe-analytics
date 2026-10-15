CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_root_cause` AS
WITH incidents AS (
  SELECT
    incident_id,
    ANY_VALUE(event_date) AS event_date,
    ANY_VALUE(user_pseudo_id) AS user_pseudo_id,
    ANY_VALUE(amba_zone_id) AS amba_zone_id,
    ANY_VALUE(partido_amba) AS partido_amba,
    ANY_VALUE(latitude) AS latitude,
    ANY_VALUE(longitude) AS longitude,
    ANY_VALUE(diagnosed_cause) AS diagnosed_cause,
    ANY_VALUE(external_alert) AS external_alert,
    MAX(IF(event_name = 'playback_microcut_detected', stall_duration_ms, NULL)) AS stall_duration_ms,
    MAX(technical_visit_requested) AS technical_visit_requested,
    MAX(avoided_visit_cost_usd) AS avoided_visit_cost_usd,
    MAX(visit_cost_usd) AS visit_cost_usd
  FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.v_events_clean`
  WHERE incident_id IS NOT NULL
  GROUP BY incident_id
)
SELECT
  event_date,
  amba_zone_id,
  partido_amba,
  latitude,
  longitude,
  diagnosed_cause,
  external_alert,
  COUNT(*) AS microcuts,
  COUNT(DISTINCT user_pseudo_id) AS affected_users,
  AVG(stall_duration_ms) AS avg_stall_ms,
  SUM(technical_visit_requested) AS visits,
  SUM(avoided_visit_cost_usd) AS avoided_visit_cost_usd,
  SUM(visit_cost_usd) AS visit_cost_usd
FROM incidents
GROUP BY ALL;

CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_zone_concurrency_5m` AS
SELECT
  TIMESTAMP_BUCKET(event_ts, INTERVAL 5 MINUTE) AS bucket_5m,
  amba_zone_id,
  COUNT(DISTINCT session_id) AS concurrent_sessions,
  APPROX_QUANTILES(NULLIF(live_latency_ms, 0), 100)[SAFE_OFFSET(95)] AS p95_latency_ms,
  COUNTIF(event_name = 'playback_microcut_detected') AS microcuts
FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.v_events_clean`
GROUP BY bucket_5m, amba_zone_id;

