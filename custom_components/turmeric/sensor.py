# sensor.py
from datetime import datetime, time
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

class TurmericSensor(CoordinatorEntity, Entity):
    """Representation of a Turmeric sensor."""

    def __init__(self, coordinator, sensor_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.type = sensor_type

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Turmeric {self.type.title()}"

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"turmeric_{self.type}"

    @property
    def state(self):
        """Return the state of the sensor."""
        try:
            if self.type == "groceries":
                items = [
                    item["name"]
                    for item in self.coordinator.data["groceries"]["result"]
                ]
                return (
                    ", ".join(items)
                    if len(items) <= 5
                    else f"{len(items)} items available"
                )
            elif self.type == "meals":
                today = datetime.combine(datetime.today(), time.min)
                meals = [
                    meal
                    for meal in self.coordinator.data["meals"]["result"]
                    if datetime.strptime(
                        meal["date"], "%Y-%m-%d %H:%M:%S"
                    )
                    >= today
                ][:7]
                return f"{len(meals)} upcoming meals" if meals else "No upcoming meals"
        except (KeyError, TypeError):
            return "Data unavailable"

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        try:
            if self.type == "groceries":
                aisles = {}
                for item in self.coordinator.data["groceries"]["result"]:
                    aisle = item.get("aisle", "Uncategorized")
                    aisles.setdefault(aisle, []).append(item["name"])
                return {"aisles": aisles}
            elif self.type == "meals":
                today = datetime.combine(datetime.today(), time.min)
                return {
                    "meals": [
                        {"name": meal["name"], "date": meal["date"]}
                        for meal in sorted(
                            self.coordinator.data["meals"]["result"],
                            key=lambda x: x["date"],
                        )
                        if datetime.strptime(
                            meal["date"], "%Y-%m-%d %H:%M:%S"
                        )
                        >= today
                    ][:7]
                }
        except (KeyError, TypeError):
            return {"error": "Data unavailable"}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Turmeric sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        TurmericSensor(coordinator, "groceries"),
        TurmericSensor(coordinator, "meals"),
    ]
    async_add_entities(sensors)