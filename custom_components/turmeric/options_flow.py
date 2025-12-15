# options_flow.py
from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers import selector
from .const import DOMAIN, CONF_API_TOKEN

class TurmericOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Turmeric options."""

    def __init__(self, config_entry):
        """Initialize the options flow handler."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the Turmeric options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Required(
                    CONF_API_TOKEN,
                    default=self.config_entry.options.get(CONF_API_TOKEN, ""),
                ): selector.TextSelector(
                    selector.TextSelectorConfig(type="password")
                ),
                vol.Optional(
                    "groceries_refresh",
                    default=self.config_entry.options.get(
                        "groceries_refresh", 360
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
                vol.Optional(
                    "meals_refresh",
                    default=self.config_entry.options.get("meals_refresh", 720),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
            }
        )

        return self.async_show_form(
            step_id="init", data_schema=options_schema
        )