"""Options flow for Turmeric integration."""
import voluptuous as vol

from homeassistant import config_entries

from .const import DEFAULT_GROCERIES_REFRESH, DEFAULT_MEALS_REFRESH


class TurmericOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Turmeric options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the options flow handler."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the Turmeric options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    "groceries_refresh",
                    default=self.config_entry.options.get(
                        "groceries_refresh",
                        self.config_entry.data.get(
                            "groceries_refresh", DEFAULT_GROCERIES_REFRESH
                        ),
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
                vol.Optional(
                    "meals_refresh",
                    default=self.config_entry.options.get(
                        "meals_refresh",
                        self.config_entry.data.get(
                            "meals_refresh", DEFAULT_MEALS_REFRESH
                        ),
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
