# Checklist para publicarlo hoy

## 1. BigQuery

1. Crear un proyecto de Google Cloud o usar uno existente con facturación habilitada.
2. Crear el dataset `streaming_qoe_analytics` en `southamerica-east1`.
3. Cargar los CSV con autodetección:
   - `ga4_events_flat.csv` → `ga4_events_flat`
   - `experiment_assignments.csv` → `experiment_assignments`
   - `external_amba_alerts.csv` → `external_amba_alerts`
   - `tracking_plan.csv` → `tracking_plan`
4. Abrir cada archivo de `sql/`, reemplazar `YOUR_PROJECT_ID` y ejecutarlo en orden.
5. Si `tracking_plan.csv` quedó con columnas `string_field_*`, ejecutar
   `08_tracking_plan_view.sql` para exponer el esquema normalizado y excluir
   la fila de encabezado importada como dato.
6. Ejecutar `07_data_quality_checks.sql`: todos los controles críticos deben dar cero.

## 2. Looker Studio

Seguir `looker/dashboard_build_guide.md`. Para publicar hoy alcanza con tres capturas: overview, causa raíz/mapa y experimento.

## 3. Firebase

1. Crear un proyecto Firebase y registrar una aplicación web.
2. Activar Google Analytics.
3. Copiar `firebase-config.example.js` como `firebase-config.js` y reemplazar los valores.
4. Servir la carpeta con `python -m http.server 8080`.
5. Abrir `http://localhost:8080`, generar eventos y sacar captura del panel local y de DebugView.
6. Crear parámetros de Remote Config con los nombres indicados en el prototipo.

## 4. GitHub y LinkedIn

1. Subir el repositorio sin `firebase-config.js`.
2. Agregar tres imágenes en una carpeta `assets/` y enlazarlas en el README.
3. Publicar el texto de `LINKEDIN_POST.md` y adjuntar las capturas.
4. No usar logos de Flow ni afirmar que el trabajo fue realizado para la empresa.

