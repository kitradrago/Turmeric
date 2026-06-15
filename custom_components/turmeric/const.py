<<<<<<< HEAD
"""Constants for the Turmeric integration."""

DOMAIN = "turmeric"

# API endpoints
BASE_URL = "https://www.paprikaapp.com/api/v2/sync"
LOGIN_URL_V2 = "https://www.paprikaapp.com/api/v2/account/login/"
LOGIN_URL_V1 = "https://www.paprikaapp.com/api/v1/account/login/"

# Default refresh intervals (minutes)
DEFAULT_GROCERIES_REFRESH = 360  # 6 hours
DEFAULT_MEALS_REFRESH = 720  # 12 hours

# API request timeout (seconds)
API_TIMEOUT = 10

# Meal type mapping
MEAL_TYPES = {
    0: "Breakfast",
    1: "Lunch",
    2: "Dinner",
    3: "Snack",
}

# Expected response fields
GROCERY_REQUIRED_FIELDS = ["name"]
GROCERY_OPTIONAL_FIELDS = ["aisle"]
MEAL_REQUIRED_FIELDS = ["name", "date"]
MEAL_OPTIONAL_FIELDS = ["type"]
=======
# const.py
DOMAIN = "turmeric"
BASE_URL = "https://www.paprikaapp.com/api/v2/sync"
LOGIN_URL_V2 = "https://www.paprikaapp.com/api/v2/account/login/"
LOGIN_URL_V1 = "https://www.paprikaapp.com/api/v1/account/login/"

# Default refresh intervals (minutes)
DEFAULT_GROCERIES_REFRESH = 360  # 6 hours
DEFAULT_MEALS_REFRESH = 720  # 12 hours
>>>>>>> d606a24d74e32d92a3c366ffe03c4c1908295b35
