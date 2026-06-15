"""Config flow for Turmeric integration."""
<<<<<<< HEAD
import asyncio
=======
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
import logging

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

<<<<<<< HEAD
from .const import DOMAIN, LOGIN_URL_V2, LOGIN_URL_V1, API_TIMEOUT
=======
from .const import DOMAIN, LOGIN_URL_V2, LOGIN_URL_V1
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35

_LOGGER = logging.getLogger(__name__)


async def async_login_paprika(
    session: aiohttp.ClientSession, email: str, password: str
) -> str | None:
<<<<<<< HEAD
    """Authenticate with Paprika and return the bearer token, or None on failure.
    
    Tries API v2 first, falls back to v1 for backwards compatibility.
    """
    for url_name, url in [("v2", LOGIN_URL_V2), ("v1", LOGIN_URL_V1)]:
        try:
            _LOGGER.debug("Attempting Paprika authentication with API %s", url_name)
            async with session.post(
                url,
                data={"email": email, "password": password},
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT),
=======
    """Authenticate with Paprika and return the bearer token, or None on failure."""
    for url in (LOGIN_URL_V2, LOGIN_URL_V1):
        try:
            async with session.post(
                url, data={"email": email, "password": password}, timeout=aiohttp.ClientTimeout(total=10)
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    token = data.get("result", {}).get("token")
                    if token:
<<<<<<< HEAD
                        _LOGGER.debug("Successfully authenticated with Paprika API %s", url_name)
                        return token
                    _LOGGER.warning(
                        "Paprika API %s returned 200 but no token in response", url_name
                    )
                elif resp.status == 401:
                    _LOGGER.debug("Authentication failed with API %s (401)", url_name)
                else:
                    _LOGGER.warning(
                        "Paprika API %s returned unexpected status %d", url_name, resp.status
                    )
        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout connecting to Paprika API %s", url_name)
        except aiohttp.ClientError as err:
            _LOGGER.debug("Client error with Paprika API %s: %s", url_name, err)
        except Exception as err:
            _LOGGER.warning("Unexpected error with Paprika API %s: %s", url_name, err)

    _LOGGER.error("Failed to authenticate with Paprika API (tried v2 and v1)")
=======
                        return token
        except (aiohttp.ClientError, TimeoutError):
            continue
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
    return None


class TurmericConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Turmeric integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step — email + password login."""
        errors: dict[str, str] = {}

        if user_input is not None:
<<<<<<< HEAD
            email = user_input[CONF_EMAIL].strip()
=======
            email = user_input[CONF_EMAIL]
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
            password = user_input[CONF_PASSWORD]
            groceries_refresh = user_input.get("groceries_refresh", 360)
            meals_refresh = user_input.get("meals_refresh", 720)

<<<<<<< HEAD
            # Validate refresh intervals
=======
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
            if not (1 <= groceries_refresh <= 1440) or not (1 <= meals_refresh <= 1440):
                errors["base"] = "invalid_refresh_time"
            else:
                # Prevent duplicate entries for the same account
                await self.async_set_unique_id(email.lower())
                self._abort_if_unique_id_configured()

                session = async_get_clientsession(self.hass)
                token = await async_login_paprika(session, email, password)

                if token is None:
                    errors["base"] = "invalid_auth"
                else:
<<<<<<< HEAD
                    _LOGGER.info("Turmeric integration setup successful for %s", email)
=======
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
                    return self.async_create_entry(
                        title=email,
                        data={
                            CONF_EMAIL: email,
                            CONF_PASSWORD: password,
                            "api_token": token,
                            "groceries_refresh": groceries_refresh,
                            "meals_refresh": meals_refresh,
                        },
                    )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional("groceries_refresh", default=360): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=1440)
                ),
                vol.Optional("meals_refresh", default=720): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=1440)
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        from .options_flow import TurmericOptionsFlowHandler
<<<<<<< HEAD

        return TurmericOptionsFlowHandler(config_entry)
=======
        return TurmericOptionsFlowHandler(config_entry)
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
