# __init__.py
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_API_TOKEN
from .coordinator import TurmericCoordinator
from .const import DOMAIN, DEFAULT_GROCERIES_REFRESH, DEFAULT_MEALS_REFRESH

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Turmeric from a config entry."""

    # ------------------------------------------------------------------
    # 1️⃣  Pull values – first from options (user‑editable), then fall back
    #     to the original data dict or defaults.
    # ------------------------------------------------------------------
    api_token = entry.data.get(CONF_API_TOKEN) or entry.options.get(CONF_API_TOKEN)
    groceries_refresh = entry.options.get(
        "groceries_refresh",
        entry.data.get("groceries_refresh", DEFAULT_GROCERIES_REFRESH),
    )
    meals_refresh = entry.options.get(
        "meals_refresh",
        entry.data.get("meals_refresh", DEFAULT_MEALS_REFRESH),
    )

    coordinator = TurmericCoordinator(
        hass, api_token, groceries_refresh, meals_refresh
    )
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Perform the very first refresh (so entities have data right away)
    await coordinator.async_config_entry_first_refresh()

    # Forward the entry to the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    )

    # ------------------------------------------------------------------
    # 2️⃣  Register a manual‑refresh service for debugging / automation
    # ------------------------------------------------------------------
    async def _handle_refresh(call):
        """Service handler – force an immediate refresh of both datasets."""
        await coordinator.async_refresh()

    hass.services.async_register(DOMAIN, "refresh_all", _handle_refresh)

    # ------------------------------------------------------------------
    # 3️⃣  Listen for option changes so a reload happens automatically
    # ------------------------------------------------------------------
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    return True


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the integration when the user changes options."""
    _LOGGER.debug("Turmeric options updated – reloading entry")
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the Turmeric config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok