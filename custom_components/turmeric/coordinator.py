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

<<<<<<< HEAD
from .const import (
    BASE_URL,
    DEFAULT_GROCERIES_REFRESH,
    DEFAULT_MEALS_REFRESH,
    API_TIMEOUT,
    GROCERY_REQUIRED_FIELDS,
    MEAL_REQUIRED_FIELDS,
)
=======
from .const import BASE_URL, DEFAULT_GROCERIES_REFRESH, DEFAULT_MEALS_REFRESH
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35

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
<<<<<<< HEAD
            _LOGGER.error("Missing email or password for re-authentication")
=======
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
            return False

        session = async_get_clientsession(self.hass)
        token = await async_login_paprika(session, email, password)
        if token:
            self.api_token = token
<<<<<<< HEAD
            _LOGGER.debug("Successfully re-authenticated with Paprika API")
            return True

        _LOGGER.error("Re-authentication failed: Invalid token returned from Paprika API")
=======
            return True
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
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

<<<<<<< HEAD
    async def _validate_response(self, data: dict, endpoint: str) -> bool:
        """Validate API response structure matches expectations."""
        if not isinstance(data, dict):
            _LOGGER.warning(f"Invalid response type for {endpoint}: expected dict")
            return False

        if "result" not in data:
            _LOGGER.warning(f"Missing 'result' field in {endpoint} response")
            return False

        if not isinstance(data["result"], list):
            _LOGGER.warning(f"Invalid 'result' type for {endpoint}: expected list")
            return False

        # Validate individual items
        if endpoint == "groceries":
            for item in data["result"]:
                if not isinstance(item, dict) or "name" not in item:
                    _LOGGER.warning(f"Grocery item missing required 'name' field: {item}")
                    return False

        elif endpoint == "meals":
            for item in data["result"]:
                if not isinstance(item, dict) or "name" not in item or "date" not in item:
                    _LOGGER.warning(f"Meal item missing required fields: {item}")
                    return False

        return True

    async def _api_get(self, endpoint: str, max_retries: int = 3) -> dict:
        """Make an authenticated GET request with exponential backoff on rate limit."""
        session = async_get_clientsession(self.hass)

        for attempt in range(max_retries):
            headers = {"Authorization": f"Bearer {self.api_token}"}

            try:
                async with asyncio.timeout(API_TIMEOUT):
                    async with session.get(
                        f"{BASE_URL}/{endpoint}", headers=headers
                    ) as resp:
                        if resp.status == 401:
                            _LOGGER.debug(
                                "Token expired for %s, attempting re-authentication",
                                endpoint,
                            )
                            if await self._async_re_authenticate():
                                headers["Authorization"] = f"Bearer {self.api_token}"
                                async with session.get(
                                    f"{BASE_URL}/{endpoint}", headers=headers
                                ) as retry_resp:
                                    if retry_resp.status == 200:
                                        data = await retry_resp.json()
                                        if self._validate_response(data, endpoint):
                                            return data
                                        raise UpdateFailed(
                                            f"Invalid response structure from {endpoint}"
                                        )
                                    retry_resp.raise_for_status()

                            raise UpdateFailed(f"Re-authentication failed for {endpoint}")

                        if resp.status == 429:
                            retry_after = resp.headers.get("Retry-After", "unknown")
                            if attempt < max_retries - 1:
                                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                                _LOGGER.warning(
                                    "Paprika API rate-limited for %s – "
                                    "retrying in %d seconds (attempt %d/%d)",
                                    endpoint,
                                    wait_time,
                                    attempt + 1,
                                    max_retries,
                                )
                                await asyncio.sleep(wait_time)
                                continue
                            else:
                                _LOGGER.error(
                                    "Paprika API rate-limited for %s – "
                                    "max retries exceeded (retry-after: %s seconds)",
                                    endpoint,
                                    retry_after,
                                )
                                raise UpdateFailed(
                                    f"Rate limited ({endpoint}) – retry after {retry_after}s"
                                )

                        if resp.status == 200:
                            data = await resp.json()
                            if self._validate_response(data, endpoint):
                                return data
                            raise UpdateFailed(
                                f"Invalid response structure from {endpoint}"
                            )

                        resp.raise_for_status()

            except asyncio.TimeoutError:
                _LOGGER.error("Timeout while fetching %s (attempt %d/%d)", endpoint, attempt + 1, max_retries)
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise UpdateFailed(f"Timeout while fetching {endpoint}")

            except aiohttp.ClientError as err:
                _LOGGER.error(
                    "Client error while fetching %s (attempt %d/%d): %s",
                    endpoint,
                    attempt + 1,
                    max_retries,
                    err,
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise UpdateFailed(f"Client error while fetching {endpoint}: {err}")

        raise UpdateFailed(f"Failed to fetch {endpoint} after {max_retries} attempts")
=======
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
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35

    async def _fetch_groceries(self):
        """Fetch groceries data from the Paprika API."""
        try:
            self.groceries_data = await self._api_get("groceries")
<<<<<<< HEAD
            _LOGGER.debug(
                "Successfully fetched groceries: %d items",
                len(self.groceries_data.get("result", [])),
            )
=======
            _LOGGER.debug("Fetched groceries data: %s", self.groceries_data)
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
        except Exception as err:
            _LOGGER.error("Error fetching groceries data: %s", err)
            raise UpdateFailed(f"Failed to update groceries: {err}") from err

    async def _fetch_meals(self):
        """Fetch meals data from the Paprika API."""
        try:
            self.meals_data = await self._api_get("meals")
<<<<<<< HEAD
            _LOGGER.debug(
                "Successfully fetched meals: %d items",
                len(self.meals_data.get("result", [])),
            )
        except Exception as err:
            _LOGGER.error("Error fetching meals data: %s", err)
            raise UpdateFailed(f"Failed to update meals: {err}") from err
=======
            _LOGGER.debug("Fetched meals data: %s", self.meals_data)
        except Exception as err:
            _LOGGER.error("Error fetching meals data: %s", err)
            raise UpdateFailed(f"Failed to update meals: {err}") from err
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
