
# Turmeric: Home Assistant Integration for PaprikaAPP

Turmeric is a custom Home Assistant integration designed to connect with the Paprika App API. It provides sensors for grocery lists and meal plans, making them easily accessible on your Home Assistant dashboard.

---

## Features
- **Groceries Sensor**: Displays a list of grocery items grouped by aisle.
- **Meals Sensor**: Lists the next seven planned meals in chronological order.
- Configurable refresh rates for groceries and meals data.

---

## Installation

### Option 1: Install via HACS (Pending HACS Validation and Inclusion)
~~1. Open Home Assistant and go to **HACS** → **Integrations**.
2. Click the **+ Explore & Download Repositories** button.
3. Search for "Turmeric" and click **Download**.
4. Restart Home Assistant.
5. Go to **Settings** → **Devices & Services** → **Integrations**.
6. Click **Add Integration**, search for "Turmeric," and follow the setup instructions.~~

### Option 2: Manual Installation
1. Clone or download the repository into your Home Assistant `custom_components` folder.

```bash
cd /config/custom_components
mkdir turmeric
cd turmeric
# Copy the integration files here
```

2. Restart Home Assistant.

---

## Setup Instructions

### 1. Obtain Your Paprika App API Token
To use this integration, you need your Paprika App API token. Follow these steps:

1. Open a terminal or command prompt.
2. Run the following `curl` command, replacing `MY_EMAIL` with your Paprika account email and `MY_PAPRIKA_PASSWORD` with your password:

      ```bash
   curl -X POST https://paprikaapp.com/api/v1/account/login -d 'email=MY_EMAIL&password=MY_PAPRIKA_PASSWORD'
   ```
    if v1 doesnt work, try using v2.
   
   ```bash
   curl -X POST https://paprikaapp.com/api/v2/account/login -d 'email=MY_EMAIL&password=MY_PAPRIKA_PASSWORD'
   ```

4. The response will contain a field called `token`. Copy this token; you'll need it during setup.

### 2. Add the Integration
1. Go to **Settings** → **Devices & Services** → **Integrations**.
2. Click the **Add Integration** button.
3. Search for "Turmeric" and select it.
4. Enter your Paprika API token.
5. Configure the refresh intervals (in minutes) for groceries and meals (default: 360 and 720 respectively).
6. Save the configuration.

### 3. Verify Sensors
1. Navigate to **Developer Tools** → **States**.
2. Look for `sensor.turmeric_groceries` and `sensor.turmeric_meals`.
3. Verify that the data is populated correctly.

---

## Dashboard Cards

### Grocery List Card
Displays the grocery list grouped by aisle.

#### YAML Configuration
```yaml
type: markdown
title: Grocery List
content: |
  {% if state_attr('sensor.turmeric_groceries', 'aisles') %}
  **Grocery List:**
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

### Upcoming Meals Card
Displays a numbered list of the next seven planned meals.

#### YAML Configuration
```yaml
type: markdown
title: Upcoming Meals
content: |
  {% if state_attr('sensor.turmeric_meals', 'meals') %}
  {% for meal in state_attr('sensor.turmeric_meals', 'meals') %}
  {{ loop.index }}. {{ meal.name }} - {{ meal.date }}
  {% endfor %}
  {% else %}
  No upcoming meals planned.
  {% endif %}
```

---

## Configuration Options

During setup, you can configure the following options:
- **API Token**: Your Paprika App API token.
- **Groceries Refresh Rate**: Frequency (in minutes) to refresh grocery data (default: 360).
- **Meals Refresh Rate**: Frequency (in minutes) to refresh meal data (default: 720).

---

## Troubleshooting

### Common Issues
1. **Integration Not Visible**:
   - Ensure files are in `/config/custom_components/turmeric/`.
   - Restart Home Assistant and clear the browser cache.

2. **Sensors Returning `Unknown`**:
   - Verify the API token is correct.
   - Check logs under **Settings** → **System** → **Logs** for errors.

3. **Markdown Card Formatting Issues**:
   - Verify the card YAML is correctly indented.
   - Ensure the sensors are populated with data.

### Debugging Logs
Enable debug logging for the integration by adding the following to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.turmeric: debug
```

Check the logs under **Settings** → **System** → **Logs**.

---

## Future Enhancements
- Real-time push updates from Paprika App? (May not be possible)
- Optional step to use Paprika Login info to automatically pull users token.
- Options to toggle upcoming meals display by count or by date.
- Support for more Paprika API endpoints.
- Enhanced error handling and validation.

---

## Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/kitradrago/turmeric).

## Attributions

Thanks to the following inspirations: 

Darius K ( https://community.home-assistant.io/u/dariusk/ ) - RESTful sensor pull that I first found. My frustration at trying to find a nice way to format the output in this pushed me over to figuring out how to do it in an integration way to make things easier.

@mattdsteele ( https://gist.github.com/mattdsteele/7386ec363badfdeaad05a418b9a1f30a ) which helped me figure out the groceries API link and some other things.

---

## License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

Under this license:
- You are free to use, modify, and distribute the software.
- Attribution is required in any derivative works, ensuring that credit is given to the original authors.
