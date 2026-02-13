"""Data update coordinator for Turmeric integration."""
import asyncio
import logging
from datetime import datetime, timedelta, timezone

import aiohttp

from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import BASE_URL, DEFAULT_GROCERIES_REFRESH, DEFAULT_MEALS_REFRESH

_LOGGER = logging.getLogger(__name__)


class TurmericCoordinator(DataUpdateCoordinator):
    """Custom coordinator for Turmeric integration."""

    def __init__(self, hass, entry_data, groceries_refresh, meals_refresh):
        """Initialise the coordinator.

        `groceries_refresh` and `meals_refresh` are in minutes.
        The coordinator runs at the shortest interval and decides
        internally whether each endpoint needs to be refreshed.
        """
        min_interval = min(groceries_refresh, meals_refresh)

        super().__init__(
            hass,
            _LOGGER,
            name="TurmericCoordinator",
            update_interval=timedelta(minutes=min_interval),
        )

        self._entry_data = entry_data
        self.api_token: str = entry_data.get("api_token", "")
        self.groceries_refresh = timedelta(minutes=groceries_refresh)
        self.meals_refresh = timedelta(minutes=meals_refresh)

        self.last_groceries_update: datetime = datetime.min.replace(tzinfo=timezone.utc)
        self.last_meals_update: datetime = datetime.min.replace(tzinfo=timezone.utc)

        self.groceries_data = None
        self.meals_data = None

    async def _async_re_authenticate(self) -> bool:
        """Re-authenticate with Paprika using stored credentials."""
        from .config_flow import async_login_paprika

        email = self._entry_data.get(CONF_EMAIL, "")
        password = self._entry_data.get(CONF_PASSWORD, "")
        if not email or not password:
            return False

        session = async_get_clientsession(self.hass)
        token = await async_login_paprika(session, email, password)
        if token:
            self.api_token = token
            return True
        return False

    async def _async_update_data(self):
        """Called by HA at the interval defined in update_interval."""
        now = datetime.now(timezone.utc)
        tasks: list[asyncio.Task] = []

        if now - self.last_groceries_update >= self.groceries_refresh:
            tasks.append(self._fetch_groceries())
            self.last_groceries_update = now

        if now - self.last_meals_update >= self.meals_refresh:
            tasks.append(self._fetch_meals())
            self.last_meals_update = now

        if tasks:
            await asyncio.gather(*tasks)

        return {"groceries": self.groceries_data, "meals": self.meals_data}

    async def _api_get(self, endpoint: str) -> dict:
        """Make an authenticated GET request, re-authenticating on 401."""
        session = async_get_clientsession(self.hass)
        headers = {"Authorization": f"Bearer {self.api_token}"}

        async with asyncio.timeout(10):
            async with session.get(
                f"{BASE_URL}/{endpoint}", headers=headers
            ) as resp:
                if resp.status == 401:
                    _LOGGER.debug("Token expired for %s, re-authenticating", endpoint)
                    if await self._async_re_authenticate():
                        headers["Authorization"] = f"Bearer {self.api_token}"
                        async with session.get(
                            f"{BASE_URL}/{endpoint}", headers=headers
                        ) as retry_resp:
                            retry_resp.raise_for_status()
                            return await retry_resp.json()
                    raise UpdateFailed(f"Re-authentication failed for {endpoint}")

                if resp.status == 429:
                    retry = resp.headers.get("Retry-After", "unknown")
                    _LOGGER.warning(
                        "Paprika rate-limited %s request – retry after %s seconds",
                        endpoint,
                        retry,
                    )
                    raise UpdateFailed(f"Rate limited ({endpoint})")

                resp.raise_for_status()
                return await resp.json()

    async def _fetch_groceries(self):
        """Fetch groceries data from the Paprika API."""
        try:
            self.groceries_data = await self._api_get("groceries")
            _LOGGER.debug("Fetched groceries data: %s", self.groceries_data)
        except Exception as err:
            _LOGGER.error("Error fetching groceries data: %s", err)
            raise UpdateFailed(f"Failed to update groceries: {err}") from err

    async def _fetch_meals(self):
        """Fetch meals data from the Paprika API."""
        try:
            self.meals_data = await self._api_get("meals")
            _LOGGER.debug("Fetched meals data: %s", self.meals_data)
        except Exception as err:
            _LOGGER.error("Error fetching meals data: %s", err)
            raise UpdateFailed(f"Failed to update meals: {err}") from err
