# coordinator.py
import logging
import aiohttp
import asyncio
import async_timeout
from datetime import datetime, timedelta
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import BASE_URL, DEFAULT_GROCERIES_REFRESH, DEFAULT_MEALS_REFRESH

_LOGGER = logging.getLogger(__name__)

class TurmericCoordinator(DataUpdateCoordinator):
    """Custom coordinator for Turmeric integration."""

    def __init__(self, hass, api_token, groceries_refresh, meals_refresh):
        """
        Initialise the coordinator.

        * `groceries_refresh` and `meals_refresh` are expressed in minutes.
        * The coordinator runs at the *shortest* interval and decides internally
          whether each endpoint needs to be refreshed.
        """
        # Determine the smallest interval – this drives the HA scheduler
        min_interval = min(groceries_refresh, meals_refresh)

        super().__init__(
            hass,
            _LOGGER,
            name="TurmericCoordinator",
            update_interval=timedelta(minutes=min_interval),
        )

        self.api_token = api_token
        self.groceries_refresh = timedelta(minutes=groceries_refresh)
        self.meals_refresh = timedelta(minutes=meals_refresh)

        # Track the last successful fetch for each endpoint
        self.last_groceries_update = datetime.min
        self.last_meals_update = datetime.min

        self.groceries_data = None
        self.meals_data = None

    async def _async_update_data(self):
        """Called by HA at the interval defined in ``update_interval``."""
        now = datetime.utcnow()
        tasks = []

        # Refresh groceries if its interval has elapsed
        if now - self.last_groceries_update >= self.groceries_refresh:
            tasks.append(self._fetch_groceries())
            self.last_groceries_update = now

        # Refresh meals if its interval has elapsed
        if now - self.last_meals_update >= self.meals_refresh:
            tasks.append(self._fetch_meals())
            self.last_meals_update = now

        if tasks:
            await asyncio.gather(*tasks)

        return {"groceries": self.groceries_data, "meals": self.meals_data}

    async def _fetch_groceries(self):
        """Fetch groceries data from the Paprika API."""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with async_timeout.timeout(10):
                    async with session.get(
                        f"{BASE_URL}/groceries", headers=headers
                    ) as resp:
                        if resp.status == 429:
                            retry = resp.headers.get("Retry-After", "unknown")
                            _LOGGER.warning(
                                "Paprika rate‑limited groceries request – retry after %s seconds",
                                retry,
                            )
                            raise UpdateFailed("Rate limited (groceries)")
                        resp.raise_for_status()
                        self.groceries_data = await resp.json()
                        _LOGGER.debug(
                            "Fetched groceries data: %s", self.groceries_data
                        )
        except Exception as err:  # pragma: no cover
            _LOGGER.error("Error fetching groceries data: %s", err)
            raise UpdateFailed(f"Failed to update groceries: {err}")

    async def _fetch_meals(self):
        """Fetch meals data from the Paprika API."""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with async_timeout.timeout(10):
                    async with session.get(
                        f"{BASE_URL}/meals", headers=headers
                    ) as resp:
                        if resp.status == 429:
                            retry = resp.headers.get("Retry-After", "unknown")
                            _LOGGER.warning(
                                "Paprika rate‑limited meals request – retry after %s seconds",
                                retry,
                            )
                            raise UpdateFailed("Rate limited (meals)")
                        resp.raise_for_status()
                        self.meals_data = await resp.json()
                        _LOGGER.debug(
                            "Fetched meals data: %s", self.meals_data
                        )
        except Exception as err:  # pragma: no cover
            _LOGGER.error("Error fetching meals data: %s", err)
            raise UpdateFailed(f"Failed to update meals: {err}")