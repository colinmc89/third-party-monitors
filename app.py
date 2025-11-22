from flask import Flask, render_template, request, jsonify
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# In-memory storage - in production this would be a database
MONITORS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Wayfair API",
        "api_endpoint": "https://api.wayfair.com/v1/products",
        "status": "healthy",
        "last_check": (datetime.now() - timedelta(minutes=2)).isoformat(),
        "availability_monitoring": {
            "enabled": True,
            "threshold_minutes": 5,
            "last_incident": None,
            "history": []
        },
        "data_quality_monitoring": {
            "enabled": True,
            "null_threshold_percent": 10,
            "fields_monitored": ["price", "inventory", "shipping_fee", "edd"],
            "current_null_rate": 2.3,
            "history": []
        },
        "anomaly_detection": {
            "enabled": True,
            "checks": [
                "price_spikes",
                "shipping_fee_anomalies",
                "past_edds",
                "inventory_drops",
                "shipping_fluctuations"
            ],
            "recent_anomalies": [],
            "history": []
        },
        "integrations": {
            "slack": {
                "enabled": True,
                "webhook_url": "https://hooks.slack.com/services/..."
            },
            "email": {
                "enabled": True,
                "recipients": ["eng@minoan.com", "ops@minoan.com"]
            }
        },
        "created_at": (datetime.now() - timedelta(days=7)).isoformat()
    }
]

ALERTS: List[Dict[str, Any]] = []

@app.get("/")
def index():
    """Main dashboard for third party monitors"""
    # Get recent alerts for display
    recent_alerts = sorted(ALERTS, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]
    
    return render_template(
        "index.html",
        monitors=MONITORS,
        recent_alerts=recent_alerts,
        integrations_config={
            "slack": {"enabled": True},
            "email": {"enabled": True}
        }
    )

@app.get("/api/monitors")
def get_monitors():
    """API endpoint to get all monitors"""
    return jsonify(MONITORS)

@app.get("/api/monitors/<int:monitor_id>")
def get_monitor(monitor_id: int):
    """API endpoint to get a specific monitor"""
    monitor = next((m for m in MONITORS if m["id"] == monitor_id), None)
    if not monitor:
        return jsonify({"error": "Monitor not found"}), 404
    return jsonify(monitor)

@app.put("/api/monitors/<int:monitor_id>")
def update_monitor(monitor_id: int):
    """API endpoint to update a monitor"""
    monitor = next((m for m in MONITORS if m["id"] == monitor_id), None)
    if not monitor:
        return jsonify({"error": "Monitor not found"}), 404
    
    data = request.get_json()
    
    # Handle integration toggles
    if "integrations" in data:
        monitor["integrations"].update(data["integrations"])
    
    # Handle monitoring feature toggles
    if "availability_monitoring" in data:
        monitor["availability_monitoring"].update(data["availability_monitoring"])
    if "data_quality_monitoring" in data:
        monitor["data_quality_monitoring"].update(data["data_quality_monitoring"])
    if "anomaly_detection" in data:
        monitor["anomaly_detection"].update(data["anomaly_detection"])
    
    return jsonify(monitor)

@app.post("/api/monitors")
def create_monitor():
    """API endpoint to create a new monitor"""
    data = request.get_json()
    
    monitor = {
        "id": len(MONITORS) + 1,
        "name": data.get("name", ""),
        "api_endpoint": data.get("api_endpoint", ""),
        "status": "healthy",
        "last_check": datetime.now().isoformat(),
        "availability_monitoring": {
            "enabled": data.get("availability_enabled", True),
            "threshold_minutes": data.get("threshold_minutes", 5),
            "last_incident": None,
            "history": []
        },
        "data_quality_monitoring": {
            "enabled": data.get("data_quality_enabled", True),
            "null_threshold_percent": data.get("null_threshold_percent", 10),
            "fields_monitored": data.get("fields_monitored", ["price", "inventory", "shipping_fee", "edd"]),
            "current_null_rate": 0.0,
            "history": []
        },
        "anomaly_detection": {
            "enabled": data.get("anomaly_enabled", True),
            "checks": data.get("anomaly_checks", [
                "price_spikes",
                "shipping_fee_anomalies",
                "past_edds",
                "inventory_drops",
                "shipping_fluctuations"
            ]),
            "recent_anomalies": [],
            "history": []
        },
        "integrations": {
            "slack": {
                "enabled": data.get("slack_enabled", True),
                "webhook_url": data.get("slack_webhook", "")
            },
            "email": {
                "enabled": data.get("email_enabled", True),
                "recipients": data.get("email_recipients", [])
            }
        },
        "created_at": datetime.now().isoformat()
    }
    
    MONITORS.append(monitor)
    return jsonify(monitor), 201

@app.get("/api/alerts")
def get_alerts():
    """API endpoint to get all alerts"""
    return jsonify(ALERTS)

@app.post("/api/alerts/test")
def create_test_alert():
    """Create a test alert for demonstration"""
    alert_type_param = request.args.get("type", "").lower()
    
    alert_types = {
        "availability": {
            "type": "availability",
            "severity": "critical",
            "title": "API Unresponsive",
            "message": "Wayfair API has not responded for 6 minutes",
            "monitor_id": 1
        },
        "data_quality": {
            "type": "data_quality",
            "severity": "warning",
            "title": "High Null Rate Detected",
            "message": "15% of responses missing price field (threshold: 10%)",
            "monitor_id": 1
        },
        "anomaly": {
            "type": "anomaly",
            "severity": "warning",
            "title": "Price Spike Detected",
            "message": "Product #12345 price increased 300% in last hour",
            "monitor_id": 1
        }
    }
    
    # If specific type requested, use it; otherwise random
    if alert_type_param in alert_types:
        alert_data = alert_types[alert_type_param]
    else:
        alert_data = random.choice(list(alert_types.values()))
    
    alert = {
        "id": len(ALERTS) + 1,
        "timestamp": datetime.now().isoformat(),
        **alert_data
    }
    
    ALERTS.append(alert)
    
    # Also add to the specific monitor's history
    monitor = next((m for m in MONITORS if m["id"] == alert_data["monitor_id"]), None)
    if monitor:
        if alert_data["type"] == "availability":
            monitor["availability_monitoring"]["history"].insert(0, alert)
            monitor["availability_monitoring"]["last_incident"] = alert
        elif alert_data["type"] == "data_quality":
            monitor["data_quality_monitoring"]["history"].insert(0, alert)
        elif alert_data["type"] == "anomaly":
            monitor["anomaly_detection"]["history"].insert(0, alert)
    
    return jsonify(alert), 201

@app.put("/api/integrations")
def update_integrations():
    """Update global integration settings"""
    data = request.get_json()
    
    # Update all monitors' integration settings
    for monitor in MONITORS:
        if "slack" in data:
            monitor["integrations"]["slack"]["enabled"] = data["slack"].get("enabled", False)
        if "email" in data:
            monitor["integrations"]["email"]["enabled"] = data["email"].get("enabled", False)
    
    return jsonify({"message": "Integrations updated"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5002))
    app.run(debug=True, host="0.0.0.0", port=port)
