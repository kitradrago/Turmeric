"""Sensor platform for Turmeric integration."""
<<<<<<< HEAD
from datetime import datetime, timezone
=======
from datetime import datetime, time, timezone
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from .const import DOMAIN, MEAL_TYPES

_LOGGER = __import__("logging").getLogger(__name__)

=======
from .const import DOMAIN
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35


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
                    if isinstance(item, dict) and "name" in item
                ]
                return (
                    ", ".join(items)
                    if len(items) <= 5
                    else f"{len(items)} items available"
                )
            elif self.type == "meals":
                today = datetime.now(timezone.utc).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                meals = [
                    meal
                    for meal in self.coordinator.data["meals"]["result"]
<<<<<<< HEAD
                    if isinstance(meal, dict) and "date" in meal
                    and datetime.strptime(meal["date"], "%Y-%m-%d %H:%M:%S")
=======
                    if datetime.strptime(meal["date"], "%Y-%m-%d %H:%M:%S")
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
                    .replace(tzinfo=timezone.utc)
                    >= today
                ][:7]
                return (
                    f"{len(meals)} upcoming meals"
                    if meals
                    else "No upcoming meals"
                )
<<<<<<< HEAD
        except (KeyError, TypeError, ValueError) as err:
            _LOGGER.warning("Error computing state for %s: %s", self.type, err)
=======
        except (KeyError, TypeError):
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
            return "Data unavailable"

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        try:
            if self.type == "groceries":
                aisles: dict[str, list[str]] = {}
                for item in self.coordinator.data["groceries"]["result"]:
                    if not isinstance(item, dict) or "name" not in item:
                        continue
                    aisle = item.get("aisle", "Uncategorized")
                    aisles.setdefault(aisle, []).append(item["name"])
                return {"aisles": aisles}

            elif self.type == "meals":
                today = datetime.now(timezone.utc).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
<<<<<<< HEAD
                meals_list = []

                for meal in sorted(
                    self.coordinator.data["meals"]["result"],
                    key=lambda x: (x.get("date", ""), x.get("type", 0)),
                    reverse=True,
                ):
                    if not isinstance(meal, dict) or "name" not in meal or "date" not in meal:
                        continue

                    try:
                        meal_date = datetime.strptime(meal["date"], "%Y-%m-%d %H:%M:%S")
                        meal_date_utc = meal_date.replace(tzinfo=timezone.utc)
                    except ValueError:
                        _LOGGER.warning("Invalid meal date format: %s", meal.get("date"))
                        continue

                    if meal_date_utc >= today:
                        meal_type = meal.get("type", 2)
                        meals_list.append(
                            {
                                "name": meal["name"],
                                "date": meal["date"],
                                "type": MEAL_TYPES.get(meal_type, "Meal"),
                            }
                        )

                return {"meals": meals_list[:7]}

        except (KeyError, TypeError, ValueError) as err:
            _LOGGER.warning("Error computing attributes for %s: %s", self.type, err)
=======
                type_names = {
                    0: "Breakfast",
                    1: "Lunch",
                    2: "Dinner",
                    3: "Snack",
                }
                return {
                    "meals": [
                        {
                            "name": meal["name"],
                            "date": meal["date"],
                            "type": type_names.get(
                                meal.get("type", 2), "Meal"
                            ),
                        }
                        for meal in sorted(
                            self.coordinator.data["meals"]["result"],
                            key=lambda x: (x["date"], x.get("type", 0)),
                            reverse=True,
                        )
                        if datetime.strptime(meal["date"], "%Y-%m-%d %H:%M:%S")
                        .replace(tzinfo=timezone.utc)
                        >= today
                    ][:7]
                }
        except (KeyError, TypeError):
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
            return {"error": "Data unavailable"}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Turmeric sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        TurmericSensor(coordinator, "groceries"),
        TurmericSensor(coordinator, "meals"),
    ]
    async_add_entities(sensors)
