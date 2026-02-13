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
  {% if state_attr('sensor.turmeric_meals', 'meals') %}
  {% for meal in state_attr('sensor.turmeric_meals', 'meals') %}
  {{ loop.index }}. {{ meal.name }} – {{ meal.date }}
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

## Debug logging

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
| No periodic updates | Refresh intervals too long or options not saved | Check **Configure** page, verify `turmeric.refresh_all` service exists |
| Rate-limit warnings (429) | Too many API calls to Paprika | Increase refresh intervals |

## Contributing

Pull requests, issues, and ideas are welcome! Please open them on the [GitHub repo](https://github.com/kitradrago/Turmeric).

## License

This project is released under the [MIT License](LICENSE).
