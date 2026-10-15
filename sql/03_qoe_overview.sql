CREATE OR REPLACE VIEW `YOUR_PROJECT_ID.streaming_qoe_analytics.v_qoe_overview` AS
WITH sessions AS (
  SELECT
    event_date,
    session_id,
    ANY_VALUE(user_pseudo_id) AS user_pseudo_id,
    ANY_VALUE(platform) AS platform,
    ANY_VALUE(stream_id) AS stream_id,
    ANY_VALUE(amba_zone_id) AS amba_zone_id,
    APPROX_QUANTILES(NULLIF(live_latency_ms, 0), 100)[SAFE_OFFSET(50)] AS median_latency_ms,
    APPROX_QUANTILES(NULLIF(live_latency_ms, 0), 100)[SAFE_OFFSET(95)] AS p95_latency_ms,
    COUNTIF(event_name = 'playback_microcut_detected') AS microcuts,
    SUM(IF(event_name = 'playback_microcut_detected', stall_duration_ms, 0)) AS stall_ms
  FROM `YOUR_PROJECT_ID.streaming_qoe_analytics.v_events_clean`
  WHERE session_id IS NOT NULL
  GROUP BY event_date, session_id
)
SELECT *, IF(microcuts = 0, 1, 0) AS session_without_microcuts
FROM sessions;

