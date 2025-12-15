# config_flow.py
import logging
import voluptuous as vol
import aiohttp
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from .const import DOMAIN, CONF_API_TOKEN, BASE_URL

_LOGGER = logging.getLogger(__name__)

class TurmericConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Turmeric integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            api_token = user_input.get(CONF_API_TOKEN)
            groceries_refresh = user_input.get("groceries_refresh", 360)
            meals_refresh = user_input.get("meals_refresh", 720)

            if not await self.async_validate_api_token(api_token):
                errors[CONF_API_TOKEN] = "invalid_api_token"
            elif not (1 <= groceries_refresh <= 1440):
                errors["groceries_refresh"] = "invalid_refresh_time"
            elif not (1 <= meals_refresh <= 1440):
                errors["meals_refresh"] = "invalid_refresh_time"
            else:
                return self.async_create_entry(
                    title="Turmeric",
                    data={
                        CONF_API_TOKEN: api_token,
                        "groceries_refresh": groceries_refresh,
                        "meals_refresh": meals_refresh,
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_TOKEN): selector.TextSelector(
                    selector.TextSelectorConfig(type="password")
                ),
                vol.Optional(
                    "groceries_refresh", default=360
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
                vol.Optional(
                    "meals_refresh", default=720
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_validate_api_token(self, api_token: str) -> bool:
        """Validate the API token against the Turmeric API."""
        try:
            headers = {"Authorization": f"Bearer {api_token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/groceries", headers=headers) as resp:
                    _LOGGER.debug("Validation response status: %s", resp.status)
                    if resp.status == 200:
                        return True
                    _LOGGER.debug(
                        "Validation response text: %s", await resp.text()
                    )
                    return False
        except Exception as err:  # pragma: no cover
            _LOGGER.error("Error validating API token: %s", err)
            return False