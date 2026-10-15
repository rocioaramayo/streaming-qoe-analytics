# Guía de dashboard en Looker Studio

Conectar Looker Studio a las vistas de BigQuery. La conexión directa requiere un proyecto de Google Cloud con facturación habilitada.

## Página 1 — Monitor de QoE

Fuente: `v_qoe_overview`.

- Tarjetas: sesiones, usuarios, mediana de latencia, p95 de latencia, porcentaje de sesiones sin microcortes.
- Serie temporal: fecha vs. sesiones y microcortes.
- Barras: microcortes por plataforma y stream.
- Tabla: zona, sesiones, p95, microcortes, tiempo total de stall.
- Filtros: fecha, plataforma, stream y zona.

## Página 2 — Diagnóstico y causa raíz

Fuente: `v_root_cause`.

- Mapa de burbujas: latitud/longitud; tamaño = usuarios afectados; color = causa.
- Barras: microcortes por causa diagnosticada.
- Heatmap: zona vs. fecha con cantidad de microcortes.
- Tarjetas: visitas, costo de visitas y costo evitado.
- Tabla de detalle: zona, alerta externa, causa, afectados, stall promedio.

## Página 3 — Experimento y roaming

Fuentes: `v_experiment_results`, `v_experiment_lift`, `v_roaming_costs`.

- Barras: tasa de contención y tasa de visita por variante.
- Tabla: activados, contenidos, visitas, IC 95% y ahorro evitado.
- Tarjeta: lift absoluto de contención.
- Nota visible: “Resultados simulados; no representan impacto real”.
- Roaming: MB y costo por país; comparación por bitrate cap.

## Estilo recomendado

- Fondo blanco, tarjetas gris muy claro y acento violeta.
- Un color por variante; mantenerlo en todas las páginas.
- Mostrar porcentajes con un decimal y costos con moneda USD.
- Títulos orientados a una pregunta, no al tipo de gráfico.

