# Machine Learning para prevención y diagnóstico

El proyecto contiene dos modelos complementarios.

## 1. Alerta temprana

Predice si una sesión sufrirá un microcorte en los próximos cinco minutos usando
solo telemetría anterior al evento. Entrenamiento e inferencia:

```powershell
python ml/train_microcut_risk_model.py
python ml/predict_microcut_risk.py
```

La separación se realiza por usuario, por lo que ninguna persona aparece a la
vez en entrenamiento y prueba. Los resultados y limitaciones se documentan en
`docs/prevention_model_card.md`.

## 2. Diagnóstico de causa raíz

Clasificador multiclase que predice la causa raíz de un microcorte usando la
telemetría disponible en el momento de detección.

### Objetivo

Predecir una de estas causas:

- `WIFI_WEAK`
- `DEVICE_POWER_OR_THERMAL`
- `EXTERNAL_ZONE`
- `NETWORK_OR_CDN`

### Variables utilizadas

Se usan intensidad de Wi-Fi, latencia, bitrate, duración del corte, plataforma,
plan, conexión, estado eléctrico, temperatura, alerta externa y nodo AMBA.

No se utilizan el diagnóstico registrado, el resultado de resolución ni la
solicitud de visita técnica como variables de entrada. Esto evita fuga de
información desde el futuro.

### Entrenamiento

```powershell
python ml/train_diagnosis_model.py
```

El script realiza una partición estratificada 80/20, validación cruzada de cinco
folds, comparación contra una línea base y genera:

- `metrics.json`
- `classification_report.csv`
- `confusion_matrix.csv`
- `feature_importance.csv`
- `test_predictions.csv`
- `diagnosis_model.joblib`

### Inferencia de ejemplo

```powershell
python ml/predict_incident.py
```

> El modelo se entrena con datos sintéticos. Sus métricas demuestran el flujo
> técnico completo, pero no equivalen a desempeño validado en producción.
