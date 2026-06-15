##Note: This is a pet project and may not be updated for long periods of time. Please feel free to contribute your fixes!

# Turmeric – Home Assistant integration for Paprika App

Turmeric is a custom Home Assistant integration that connects to the [Paprika Recipe Manager](https://www.paprikaapp.com/) API and exposes two sensors:

- **`sensor.turmeric_groceries`** – your current grocery list, grouped by aisle.
- **`sensor.turmeric_meals`** – the next seven planned meals.

## Installation

### HACS (recommended)

1. Click the button below to open the repository in HACS:

   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=kitradrago&repository=Turmeric)

2. Click **Download** and restart Home Assistant.

Alternatively, open HACS manually: **HACS → Integrations → three-dot menu → Custom repositories**, paste the repository URL, select **Integration**, then download.

### Manual

```bash
cd /config/custom_components
mkdir -p turmeric
# Copy all files from custom_components/turmeric/ into this folder
```

Restart Home Assistant afterwards.

## Setup

1. Go to **Settings → Devices & Services → Integrations → Add Integration**.
2. Search for **Turmeric** and select it.
3. Enter your **Paprika email** and **password**.
4. Optionally adjust the refresh intervals for groceries and meals (in minutes).
   - Default: **360 min (6 h)** for groceries, **720 min (12 h)** for meals.
5. Click **Submit**.

The integration will automatically authenticate with the Paprika API and begin syncing your data. If your token expires, it will re-authenticate automatically using your stored credentials.

### Verify the sensors

Open **Developer Tools → States** and look for `sensor.turmeric_groceries` and `sensor.turmeric_meals`. Their state should contain data (or "Data unavailable" if something went wrong).

<<<<<<< HEAD
## API Version & Compatibility

This integration uses the **Paprika Recipe Manager API v2** (`/api/v2/sync`).

### Supported Endpoints

- `POST /api/v2/account/login/` – Authentication (v2 preferred, falls back to v1)
- `GET /api/v2/sync/groceries` – Grocery list
- `GET /api/v2/sync/meals` – Meal plan (next 7 days)

### Authentication

The integration securely stores your email and password and uses them to obtain a Bearer token for API requests. Tokens are managed automatically and refreshed when expired (401 response).

### Data Structure

**Grocery Items** (from `/api/v2/sync/groceries`):
```json
{
  "result": [
    {
      "name": "Carrots",
      "aisle": "Produce",
      ...
    }
  ]
}
```

**Meals** (from `/api/v2/sync/meals`):
```json
{
  "result": [
    {
      "name": "Pasta Carbonara",
      "date": "2026-06-15 19:00:00",
      "type": 2,
      ...
    }
  ]
}
```

Meal type codes: `0` = Breakfast, `1` = Lunch, `2` = Dinner, `3` = Snack

=======
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
## Dashboard cards (examples)

### Grocery List (Markdown card)

```yaml
type: markdown
title: Grocery List
content: |
  {% if state_attr('sensor.turmeric_groceries', 'aisles') %}
  {% for aisle, items in state_attr('sensor.turmeric_groceries', 'aisles').items() %}
  **{{ aisle }}**
  {% for item in items %}
  - {{ item }}
  {% endfor %}
  {% endfor %}
  {% else %}
  No grocery items available.
  {% endif %}
```

### Upcoming Meals (Markdown card)

```yaml
type: markdown
title: Upcoming Meals
content: |
  {% set meals = state_attr('sensor.turmeric_meals', 'meals') %}
  {% if meals %}
  {% set ns = namespace(current_date='', current_type='') %}
  {% for meal in meals %}
  {% set meal_date = strptime(meal.date, '%Y-%m-%d %H:%M:%S') %}
  {% set formatted = meal_date.strftime('%A, %B %-d, %Y') %}
  {% if formatted != ns.current_date %}
  {% set ns.current_date = formatted %}
  {% set ns.current_type = '' %}

  **{{ formatted }}**
  {% endif %}
  {% if meal.type != ns.current_type %}
  {% set ns.current_type = meal.type %}

  *{{ meal.type }}*
  {% endif %}
  - {{ meal.name }}
  {% endfor %}
  {% else %}
  No upcoming meals planned.
  {% endif %}
```

## Options

After setup, you can adjust refresh intervals at any time:

**Settings → Devices & Services → Turmeric → Configure**

| Option | Description | Default |
| --- | --- | --- |
| Groceries Refresh | How often to sync grocery data (1–1440 min) | 360 min |
| Meals Refresh | How often to sync meal plan data (1–1440 min) | 720 min |

## Manual refresh service

Call `turmeric.refresh_all` from **Developer Tools → Services** or from any automation to force an immediate sync.

```yaml
service: turmeric.refresh_all
```

<<<<<<< HEAD
Example automation:

```yaml
automation:
  - alias: "Refresh groceries every hour"
    trigger:
      platform: time_pattern
      hours: "/1"
    action:
      service: turmeric.refresh_all
```

## Debug logging

=======
## Debug logging

>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
Add the following to your `configuration.yaml` to see detailed request/response logs:

```yaml
logger:
  default: warning
  logs:
    custom_components.turmeric: debug
```

Check the logs under **Settings → System → Logs**.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Integration not listed | Files not in `/config/custom_components/turmeric/` or HA not restarted | Verify folder location, restart HA, clear browser cache |
| Sensors show "Data unavailable" | Invalid credentials or network error | Check email/password, enable debug logging |
<<<<<<< HEAD
| Invalid credentials error during setup | Incorrect email/password or Paprika account issue | Verify credentials with [Paprika web app](https://www.paprikaapp.com/account/), ensure sync is enabled |
| No periodic updates | Refresh intervals too long or options not saved | Check **Configure** page, verify `turmeric.refresh_all` service exists in Developer Tools |
| Rate-limit warnings (429) | Too many API calls to Paprika | Increase refresh intervals (minimum recommended: 60 min for groceries, 120 min for meals) |
| Token re-authentication failures | Stored credentials are invalid or Paprika API changed | Re-add the integration with current credentials |
| `refresh_all` service not appearing | services.yaml missing or HA cache needs clearing | Restart Home Assistant, clear browser cache, check Services in Developer Tools |
=======
| No periodic updates | Refresh intervals too long or options not saved | Check **Configure** page, verify `turmeric.refresh_all` service exists |
| Rate-limit warnings (429) | Too many API calls to Paprika | Increase refresh intervals |
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35

## Contributing

Pull requests, issues, and ideas are welcome! Please open them on the [GitHub repo](https://github.com/kitradrago/Turmeric).

## License

<<<<<<< HEAD
This project is released under the [MIT License](LICENSE).
=======
This project is released under the [MIT License](LICENSE).
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
