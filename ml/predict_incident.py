"""Run one example inference with the trained diagnosis model."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "ml" / "artifacts" / "diagnosis_model.joblib"


def main() -> None:
    model = joblib.load(MODEL_PATH)
    incident = pd.DataFrame(
        [
            {
                "wifi_rssi_dbm": -84,
                "live_latency_ms": 24000,
                "bitrate_kbps": 850,
                "stall_duration_ms": 7200,
                "platform": "ANDROID_TV",
                "subscription_tier": "FLOW_FULL",
                "connection_type": "HOME_WIFI",
                "device_power_status": "NORMAL",
                "thermal_state": "NORMAL",
                "external_alert": "NONE",
                "amba_zone_id": "AMBA_SUR_NODO_08",
            }
        ]
    )
    predicted = model.predict(incident)[0]
    confidence = model.predict_proba(incident).max(axis=1)[0]
    print(f"Predicted cause: {predicted}")
    print(f"Confidence: {confidence:.2%}")


if __name__ == "__main__":
    main()
