-- Reemplazar YOUR_PROJECT_ID antes de ejecutar.
CREATE SCHEMA IF NOT EXISTS `YOUR_PROJECT_ID.streaming_qoe_analytics`
OPTIONS(location = 'southamerica-east1');

-- Las tablas base se crean cargando los CSV con autodetección.
-- Nombres: ga4_events_flat, experiment_assignments,
-- external_amba_alerts y tracking_plan.

