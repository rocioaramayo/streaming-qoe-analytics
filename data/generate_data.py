from __future__ import annotations

import csv
import hashlib
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


SEED = 20261015
USER_COUNT = 4000
START = datetime(2026, 10, 2, 18, 0, tzinfo=timezone.utc)
EXPERIMENT_ID = "qoe_smart_diagnosis_v1"
OUT = Path(__file__).resolve().parent

rng = random.Random(SEED)


def bounded_int(value: float, lower: int, upper: int) -> int:
    """Round and clip a simulated sensor value to a realistic range."""
    return max(lower, min(upper, round(value)))

ZONES = [
    ("AMBA_NORTE_NODO_14", "Vicente López", "Buenos Aires", -34.5167, -58.4833, "EDENOR"),
    ("AMBA_NORTE_NODO_22", "Tigre", "Buenos Aires", -34.4251, -58.5797, "EDENOR"),
    ("AMBA_NORTE_NODO_19", "San Isidro", "Buenos Aires", -34.4708, -58.5286, "EDENOR"),
    ("AMBA_SUR_NODO_08", "Avellaneda", "Buenos Aires", -34.6611, -58.3667, "EDESUR"),
    ("AMBA_SUR_NODO_15", "Lomas de Zamora", "Buenos Aires", -34.7609, -58.4063, "EDESUR"),
    ("AMBA_SUR_NODO_21", "Quilmes", "Buenos Aires", -34.7206, -58.2545, "EDESUR"),
    ("AMBA_OESTE_NODO_05", "Morón", "Buenos Aires", -34.6534, -58.6198, "EDENOR"),
    ("AMBA_CABA_NODO_03", "Palermo", "Ciudad Autónoma de Buenos Aires", -34.5795, -58.4230, "EDENOR"),
    ("AMBA_CABA_NODO_07", "Belgrano", "Ciudad Autónoma de Buenos Aires", -34.5621, -58.4567, "EDENOR"),
    ("AMBA_CABA_NODO_11", "Caballito", "Ciudad Autónoma de Buenos Aires", -34.6158, -58.4333, "EDESUR"),
]

STREAMS = [
    "FUTBOL_LIVE_01",
    "FUTBOL_LIVE_02",
    "BASQUET_LIVE_01",
    "TENIS_LIVE_01",
    "NOTICIAS_LIVE_01",
]

PLATFORMS = ["ANDROID_TV", "ANDROID", "IOS"]
PLATFORM_WEIGHTS = [0.44, 0.29, 0.27]

TRACKING_PLAN = [
    ("stream_start", "Inicio de reproducción en vivo", "stream_id, session_id, platform, connection_type", "Medir inicios de sesión y concurrencia"),
    ("live_playback_heartbeat", "Cada 60 segundos de reproducción", "live_latency_ms, bitrate_kbps, wifi_rssi_dbm, amba_zone_id", "Monitorear latencia y calidad de reproducción"),
    ("playback_microcut_detected", "Buffer stall mayor a 1500 ms", "stall_duration_ms, wifi_rssi_dbm, device_power_status, thermal_state", "Clasificar causa raíz de microcortes"),
    ("self_diagnosis_started", "Usuario abre el diagnóstico guiado", "incident_id, diagnosed_cause, variant", "Medir adopción del flujo de autogestión"),
    ("router_photo_uploaded", "Usuario carga una foto del router", "incident_id, wifi_rssi_dbm", "Medir avance del diagnóstico de Wi-Fi"),
    ("self_diagnosis_resolved", "Incidente resuelto sin visita en siete días", "incident_id, resolution_outcome, avoided_visit_cost_usd", "Calcular contención y ahorro operativo"),
    ("technical_visit_requested", "Usuario solicita visita técnica", "incident_id, diagnosed_cause, visit_cost_usd", "Medir fallas no contenidas"),
    ("roaming_stream_alert", "Reproducción sobre roaming internacional", "country_iso, roaming_mb_consumed, roaming_cost_usd, bitrate_cap_kbps", "Controlar costo mayorista de datos"),
]


def stable_variant(user_id: str) -> str:
    digest = hashlib.sha256(f"{EXPERIMENT_ID}:{user_id}".encode()).hexdigest()
    return "B_TREATMENT_SMART_DIAGNOSIS" if int(digest[:8], 16) % 2 else "A_CONTROL_GENERIC_REBOOT"


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


alerts = []
for alert_number in range(1, 25):
    zone = rng.choice(ZONES)
    start = START + timedelta(days=rng.randrange(14), hours=rng.randrange(0, 5), minutes=rng.randrange(60))
    duration = rng.randrange(30, 150)
    alert_type = rng.choices(["POWER_OUTAGE", "FLOOD_ALERT", "NETWORK_NODE_INCIDENT"], [0.5, 0.2, 0.3])[0]
    alerts.append(
        {
            "alert_id": f"alert_{alert_number:03d}",
            "amba_zone_id": zone[0],
            "partido_amba": zone[1],
            "electric_utility": zone[5],
            "alert_type": alert_type,
            "alert_start_ts": start.isoformat(),
            "alert_end_ts": (start + timedelta(minutes=duration)).isoformat(),
            "source_type": "synthetic",
        }
    )


assignments = []
users = []
for number in range(1, USER_COUNT + 1):
    user_id = f"usr_{number:06d}"
    variant = stable_variant(user_id)
    zone = rng.choice(ZONES)
    platform = rng.choices(PLATFORMS, PLATFORM_WEIGHTS)[0]
    tier = rng.choices(["FLOW_FLEX", "FLOW_FULL", "FLOW_FULL_4K"], [0.35, 0.48, 0.17])[0]
    activated = rng.random() < 0.82
    diagnosis = rng.choices(
        ["WIFI_WEAK", "DEVICE_POWER_OR_THERMAL", "EXTERNAL_ZONE", "NETWORK_OR_CDN"],
        [0.39, 0.25, 0.18, 0.18],
    )[0]
    containment_probability = 0.67 if variant.startswith("B_") else 0.62
    contained = activated and rng.random() < containment_probability
    visit_requested = int(activated and not contained)
    photo_uploaded = int(activated and variant.startswith("B_") and diagnosis == "WIFI_WEAK" and rng.random() < 0.68)
    roaming_cap_applied = int(variant.startswith("B_") and rng.random() < 0.92)
    assignment = {
        "experiment_id": EXPERIMENT_ID,
        "user_pseudo_id": user_id,
        "variant": variant,
        "assignment_ts": (START - timedelta(days=1)).isoformat(),
        "activated": int(activated),
        "primary_diagnosis": diagnosis if activated else "NO_INCIDENT",
        "contained_7d": int(contained),
        "technical_visit_requested": visit_requested,
        "router_photo_uploaded": photo_uploaded,
        "roaming_cap_applied": roaming_cap_applied,
        "avoided_visit_cost_usd": 25.0 if contained else 0.0,
        "visit_cost_usd": 25.0 if visit_requested else 0.0,
        "source_type": "synthetic",
    }
    assignments.append(assignment)
    users.append((user_id, variant, zone, platform, tier, assignment))


events = []
event_number = 1


def add_event(base: dict, name: str, ts: datetime, **values) -> None:
    global event_number
    row = dict(base)
    row.update(
        {
            "event_id": f"evt_{event_number:08d}",
            "event_date": ts.strftime("%Y%m%d"),
            "event_timestamp": int(ts.timestamp() * 1_000_000),
            "event_datetime_utc": ts.isoformat(),
            "event_name": name,
        }
    )
    row.update(values)
    events.append(row)
    event_number += 1


for user_id, variant, zone, platform, tier, assignment in users:
    session_count = rng.choices([1, 2, 3], [0.46, 0.39, 0.15])[0]
    incident_emitted = False
    for session_index in range(1, session_count + 1):
        session_id = f"ses_{user_id[4:]}_{session_index:02d}"
        stream_id = rng.choice(STREAMS)
        session_start = START + timedelta(
            days=rng.randrange(14),
            hours=rng.randrange(0, 5),
            minutes=rng.randrange(0, 60),
            seconds=rng.randrange(0, 60),
        )
        roaming = platform != "ANDROID_TV" and rng.random() < 0.035
        connection = "INTERNATIONAL_ROAMING" if roaming else rng.choices(
            ["HOME_WIFI", "LOCAL_CELLULAR", "HOME_WIFI_NO_INTERNET"], [0.84, 0.11, 0.05]
        )[0]
        base = {
            "user_pseudo_id": user_id,
            "session_id": session_id,
            "incident_id": "",
            "stream_id": stream_id,
            "platform": platform,
            "subscription_tier": tier,
            "experiment_id": EXPERIMENT_ID,
            "ab_test_variant": variant,
            "amba_zone_id": zone[0],
            "partido_amba": zone[1],
            "province": zone[2],
            "latitude": round(zone[3] + rng.uniform(-0.025, 0.025), 6),
            "longitude": round(zone[4] + rng.uniform(-0.025, 0.025), 6),
            "electric_utility": zone[5],
            "external_alert": "NONE",
            "connection_type": connection,
            "wifi_rssi_dbm": "",
            "device_power_status": "NORMAL",
            "thermal_state": "NORMAL",
            "live_latency_ms": "",
            "bitrate_kbps": "",
            "stall_duration_ms": 0,
            "diagnosed_cause": "NORMAL",
            "router_photo_uploaded": 0,
            "resolution_outcome": "NOT_APPLICABLE",
            "technical_visit_requested": 0,
            "visit_cost_usd": 0.0,
            "avoided_visit_cost_usd": 0.0,
            "roaming_country_iso": "",
            "roaming_mb_consumed": 0.0,
            "roaming_cost_usd": 0.0,
            "remote_config_smart_diagnosis": int(variant.startswith("B_")),
            "remote_config_bitrate_cap_kbps": 720 if variant.startswith("B_") else 0,
            "source_type": "synthetic",
        }
        add_event(base, "stream_start", session_start, live_latency_ms=rng.randrange(3500, 9000), bitrate_kbps=rng.randrange(2200, 6500))

        heartbeat_count = rng.randrange(2, 6)
        will_emit_incident = bool(assignment["activated"] and not incident_emitted)
        if will_emit_incident:
            degradation_strength = rng.uniform(0.30, 1.0)
        elif rng.random() < 0.24:
            # Transient degradation that recovers without becoming a microcut.
            degradation_strength = rng.uniform(0.25, 0.85)
        else:
            degradation_strength = rng.uniform(0.0, 0.18)
        for heartbeat in range(1, heartbeat_count + 1):
            ts = session_start + timedelta(minutes=heartbeat)
            progress = heartbeat / heartbeat_count
            # Positive and negative windows overlap. Some incidents have only a
            # weak warning and some healthy sessions show transient degradation.
            latency = bounded_int(
                rng.gauss(7600 + progress * 8200 * degradation_strength, 3100),
                3000,
                27000,
            )
            bitrate = bounded_int(
                rng.gauss(4700 - progress * 2200 * degradation_strength, 950),
                700,
                6800,
            )
            wifi = "" if roaming else bounded_int(
                rng.gauss(-57 - progress * 12 * degradation_strength, 7),
                -90,
                -40,
            )
            add_event(
                base,
                "live_playback_heartbeat",
                ts,
                wifi_rssi_dbm=wifi,
                live_latency_ms=latency,
                bitrate_kbps=bitrate,
            )

        if roaming:
            cap = assignment["roaming_cap_applied"]
            minutes_streamed = rng.randrange(10, 70)
            mb_per_minute = rng.uniform(3.8, 6.5) if cap else rng.uniform(9.0, 15.0)
            mb = round(minutes_streamed * mb_per_minute, 1)
            country = rng.choice(["BR", "UY", "CL", "PY"])
            add_event(
                base,
                "roaming_stream_alert",
                session_start + timedelta(minutes=1),
                roaming_country_iso=country,
                roaming_mb_consumed=mb,
                roaming_cost_usd=round(mb * 0.015, 2),
                live_latency_ms=rng.randrange(12000, 30000),
                bitrate_kbps=720 if cap else rng.randrange(1800, 4500),
                diagnosed_cause="ROAMING_COST_RISK",
            )

        if assignment["activated"] and not incident_emitted:
            incident_emitted = True
            incident_id = f"inc_{user_id[4:]}"
            cause = assignment["primary_diagnosis"]
            # Sensor signals overlap deliberately: production telemetry is noisy,
            # incomplete and may contain false positives. This prevents the ML
            # task from becoming a deterministic rules engine.
            wifi_center = -79 if cause == "WIFI_WEAK" else -64
            wifi = bounded_int(rng.gauss(wifi_center, 7), -92, -40)

            device_issue = cause == "DEVICE_POWER_OR_THERMAL"
            power = "VOLTAGE_DROP" if rng.random() < (0.55 if device_issue else 0.04) else "NORMAL"
            thermal = "CRITICAL_OVERHEAT" if rng.random() < (0.45 if device_issue else 0.03) else "NORMAL"

            zone_issue = cause == "EXTERNAL_ZONE"
            ext = "ACTIVE_POWER_OR_CLIMATE_ALERT" if rng.random() < (0.72 if zone_issue else 0.05) else "NONE"

            network_issue = cause == "NETWORK_OR_CDN"
            latency_center = 30000 if network_issue else 22000
            bitrate_center = 850 if network_issue else 1350
            stall_center = 9000 if network_issue else 6200
            latency = bounded_int(rng.gauss(latency_center, 6000), 10000, 45000)
            bitrate = bounded_int(rng.gauss(bitrate_center, 500), 350, 2600)
            stall = bounded_int(rng.gauss(stall_center, 3500), 1600, 18000)
            incident_base = dict(base)
            incident_base["incident_id"] = incident_id
            incident_base["external_alert"] = ext
            incident_ts = session_start + timedelta(minutes=heartbeat_count + 1)
            add_event(
                incident_base,
                "playback_microcut_detected",
                incident_ts,
                wifi_rssi_dbm=wifi,
                device_power_status=power,
                thermal_state=thermal,
                live_latency_ms=latency,
                bitrate_kbps=bitrate,
                stall_duration_ms=stall,
                diagnosed_cause=cause,
            )
            if variant.startswith("B_"):
                add_event(
                    incident_base,
                    "self_diagnosis_started",
                    incident_ts + timedelta(seconds=15),
                    wifi_rssi_dbm=wifi,
                    device_power_status=power,
                    thermal_state=thermal,
                    diagnosed_cause=cause,
                )
            if assignment["router_photo_uploaded"]:
                add_event(
                    incident_base,
                    "router_photo_uploaded",
                    incident_ts + timedelta(seconds=40),
                    wifi_rssi_dbm=wifi,
                    diagnosed_cause=cause,
                    router_photo_uploaded=1,
                )
            outcome_ts = incident_ts + timedelta(minutes=rng.randrange(2, 25))
            if assignment["contained_7d"]:
                add_event(
                    incident_base,
                    "self_diagnosis_resolved",
                    outcome_ts,
                    diagnosed_cause=cause,
                    router_photo_uploaded=assignment["router_photo_uploaded"],
                    resolution_outcome="CONTAINED_WITHOUT_VISIT_7D",
                    avoided_visit_cost_usd=25.0,
                )
            else:
                add_event(
                    incident_base,
                    "technical_visit_requested",
                    outcome_ts,
                    diagnosed_cause=cause,
                    router_photo_uploaded=assignment["router_photo_uploaded"],
                    resolution_outcome="VISIT_REQUESTED",
                    technical_visit_requested=1,
                    visit_cost_usd=25.0,
                )


event_fields = [
    "event_id", "event_date", "event_timestamp", "event_datetime_utc", "user_pseudo_id", "session_id",
    "incident_id", "stream_id", "platform", "event_name", "subscription_tier", "experiment_id",
    "ab_test_variant", "amba_zone_id", "partido_amba", "province", "latitude", "longitude",
    "electric_utility", "external_alert", "connection_type", "wifi_rssi_dbm", "device_power_status",
    "thermal_state", "live_latency_ms", "bitrate_kbps", "stall_duration_ms", "diagnosed_cause",
    "router_photo_uploaded", "resolution_outcome", "technical_visit_requested", "visit_cost_usd",
    "avoided_visit_cost_usd", "roaming_country_iso", "roaming_mb_consumed", "roaming_cost_usd",
    "remote_config_smart_diagnosis", "remote_config_bitrate_cap_kbps", "source_type",
]
assignment_fields = list(assignments[0].keys())
alert_fields = list(alerts[0].keys())
tracking_fields = ["event_name", "trigger", "key_parameters", "business_purpose"]

write_csv(OUT / "ga4_events_flat.csv", events, event_fields)
write_csv(OUT / "experiment_assignments.csv", assignments, assignment_fields)
write_csv(OUT / "external_amba_alerts.csv", alerts, alert_fields)
write_csv(
    OUT / "tracking_plan.csv",
    [dict(zip(tracking_fields, row)) for row in TRACKING_PLAN],
    tracking_fields,
)

print(f"Generated {len(events):,} events for {len(assignments):,} users")
