
# Turmeric – Home Assistant integration for Paprika App

Turmeric is a custom Home Assistant integration that talks to the Paprika App API and exposes two sensors:

* **`sensor.turmeric_groceries`** – the current grocery list, grouped by aisle.  
* **`sensor.turmeric_meals`** – the next seven planned meals.

> **v1.1.0 – 2025‑12‑15**  
> * Automatic periodic refresh (user‑defined intervals)  
> * Options page to change refresh intervals at any time  
> * Manual service `turmeric.refresh_all` for on‑demand sync  
> * Better error handling (timeouts, rate‑limit warnings)  

---

## ✨ New Features (v1.1.0)

| Feature | What it does |
|---------|--------------|
| **Automatic syncing** | The integration now refreshes groceries and meals automatically based on the intervals you set (default 6 h for groceries, 12 h for meals). |
| **Adjustable refresh intervals** | Via **Settings → Devices & Services → Turmeric → Options** you can change the refresh rate for each sensor (1‑1440 minutes). Changes are applied instantly. |
| **Manual refresh service** | Call `turmeric.refresh_all` from Developer Tools → Services or from any automation to force an immediate pull from Paprika. |
| **Improved logging** | Debug logs now include the raw payloads; warnings appear only on rate‑limit (`429`) responses or unexpected errors. |
| **Timeout & rate‑limit handling** | Each API request times out after 10 seconds. If Paprika returns a `429` you’ll see a warning with the suggested retry delay. |
| **Cleaner code** | Centralised constants, type hints, and documentation comments. |

---

## 📦 Installation

### Option 1 – HACS (hopefully coming soon)


### Option 2 – Manual

```bash
# From the Home Assistant config folder (/config)
cd custom_components
mkdir -p turmeric
cd turmeric
# Copy all integration files (manifest.json, *.py, strings.json, etc.) into this folder
Restart Home Assistant afterwards.

🔧 Setup
1️⃣ Get a Paprika App API token
# First try the v1 endpoint, fall back to v2 if needed
curl -X POST https://paprikaapp.com/api/v1/account/login \
     -d "email=YOUR_EMAIL&password=YOUR_PASSWORD"

# If that fails, try v2
curl -X POST https://paprikaapp.com/api/v2/account/login \
     -d "email=YOUR_EMAIL&password=YOUR_PASSWORD"
The JSON response contains a field called token. Copy that value – you’ll need it in the next step.

2️⃣ Add the integration
Settings → Devices & Services → Integrations → Add Integration.
Search for Turmeric and select it.
Paste the API token.
Set the Groceries Refresh and Meals Refresh intervals (minutes).
Defaults: 360 min (6 h) for groceries, 720 min (12 h) for meals.
Finish the wizard.
3️⃣ Verify the sensors
Open Developer Tools → States.
Look for sensor.turmeric_groceries and sensor.turmeric_meals.
Their state should contain data (or “Data unavailable” if something went wrong).
📊 Dashboard cards (example)
Grocery List (Markdown card)
type: markdown
title: Grocery List
content: |
  {% if state_attr('sensor.turmeric_groceries', 'aisles') %}
  **Grocery List**
  {% for aisle, items in state_attr('sensor.turmeric_groceries', 'aisles').items() %}
  **{{ aisle }}**
  {% for item in items %}
  - {{ item }}
  {% endfor %}
  {% endfor %}
  {% else %}
  No grocery items available.
  {% endif %}
Upcoming Meals (Markdown card)
type: markdown
title: Upcoming Meals
content: |
  {% if state_attr('sensor.turmeric_meals', 'meals') %}
  {% for meal in state_attr('sensor.turmeric_meals', 'meals') %}
  {{ loop.index }}. {{ meal.name }} – {{ meal.date }}
  {% endfor %}
  {% else %}
  No upcoming meals planned.
  {% endif %}
⚙️ Advanced usage
Manual refresh service
service: turmeric.refresh_all
You can call this from an automation, a button card, or the Services UI to force an immediate sync.

Debug logging
Add the following to your configuration.yaml to see detailed request/response logs:

logger:
  default: warning
  logs:
    custom_components.turmeric: debug
Check the logs under Settings → System → Logs.

🛠️ Troubleshooting
Symptom	Likely cause	Fix
Integration not listed	Files not placed in /config/custom_components/turmeric/ or HA not restarted.	Verify folder location, restart HA, clear browser cache.
Sensors show unknown or Data unavailable	Invalid API token or network error.	Re‑run the token request, ensure the token is correct, enable debug logging to view the HTTP status.
No periodic updates	Running an older version (pre‑v1.1.0) or update_interval overridden.	Update to the latest code, confirm the service turmeric.refresh_all exists, and that the options page shows the intervals you set.
Rate‑limit warnings (429)	Paprika limits the number of calls.	Increase the refresh intervals, or let the integration wait for the suggested retry‑after period (shown in the warning).
🚀 Future roadmap (ideas)
Real‑time push updates from Paprika (if the API ever supports it).
Optional login flow that automatically retrieves the token.
Ability to toggle how many meals are displayed or filter by date.
Additional Paprika endpoints (e.g., recipe lookup, ingredient scaling).
🤝 Contributing
Pull requests, issues, and ideas are welcome! Please open them on the GitHub repo:

🔗 https://github.com/kitradrago/turmeric

When contributing, make sure to:

Follow the existing code style (PEP 8, type hints).
Add or update unit tests if you introduce new logic.
Update this README if you add user‑visible features.
📜 License
This project is released under the MIT License – see the LICENSE file for the full text.

Happy cooking and automating!
