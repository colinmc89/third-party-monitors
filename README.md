# Third Party Monitors - Reliability Layer Prototype

A prototype monitoring system designed to protect customer trust by detecting when third-party data sources (starting with Wayfair API) become slow, inconsistent, or incorrect.

## 🎯 Purpose

This reliability layer has three core components:

1. **API Unresponsive Alerts** (Availability Monitoring)
   - Detects when APIs stop responding for more than X minutes
   - Alerts via Slack, Email, and internal admin tool

2. **API Acting Weird Alerts** (Data Quality Monitoring)
   - Detects when key fields return null or inconsistent values
   - Monitors: price, inventory, shipping_fee, EDD
   - Triggers when null rate exceeds threshold

3. **Data Looks Wrong Alerts** (Anomaly Detection)
   - Detects illogical or unsafe values:
     - Sudden price spikes
     - Shipping fees higher than product price
     - EDDs in the past
     - Out-of-stock rates dropping to near zero
     - Shipping fees/times fluctuating wildly

## 🚀 Getting Started

1. Install dependencies:
   ```bash
   cd /Users/colinmcd/Downloads/third_party_monitors
   python3 -m pip install -r requirements.txt
   ```

2. Start the web app:
   ```bash
   python3 app.py
   ```

3. Open your browser at:
   ```
   http://127.0.0.1:5002/
   ```

## 🎮 Features

- **Integration Controls**: Toggle Slack and Email notifications on/off from the home dashboard
- **Monitor Configuration**: Enable/disable each monitoring type per API
- **Real-time Status**: See current health status and last check time
- **Alert Dashboard**: View recent alerts with severity indicators
- **Test Alerts**: Generate sample alerts to demonstrate the system

## 📋 Current Prototype

The prototype includes:
- Wayfair API monitor (pre-configured)
- All three monitoring types enabled
- Slack and Email integrations (toggleable)
- Sample alert generation

## 🔧 Next Steps for Production

- [ ] Connect to actual API endpoints for real monitoring
- [ ] Implement background workers for continuous checks
- [ ] Add database persistence (currently in-memory)
- [ ] Configure actual Slack webhooks and email SMTP
- [ ] Add alert history and filtering
- [ ] Implement anomaly detection algorithms
- [ ] Add metrics and analytics dashboard

