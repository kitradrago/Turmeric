# Changelog

All notable changes to the Turmeric project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-02-15

### Added
- **services.yaml** - Properly registers `turmeric.refresh_all` service in Home Assistant UI (fixes issue #6)
- Response validation for Paprika API endpoints to catch malformed data
- Exponential backoff retry logic for rate-limited requests (429 responses)
- Enhanced error logging for debugging API issues with context-aware messages
- Meal type mapping constants (Breakfast, Lunch, Dinner, Snack)
- Comprehensive API version documentation in README with endpoint details
- Improved troubleshooting guide with API-specific solutions
- Debug logging in service registration and options updates

### Changed
- Updated README with API v2 endpoint details and data structure documentation
- Enhanced coordinator logging for better debugging of API interactions
- Improved error messages with specific context and retry information
- Better handling of malformed API responses with validation
- Config flow now uses API_TIMEOUT constant for consistency
- Service logging now indicates when `turmeric.refresh_all` is called

### Fixed
- Fixed handling of unexpected API response structures (issue #6)
- Improved timeout error handling in API requests with retry logic
- Added validation for required fields in API responses
- Fixed parsing of meal date strings with better error handling
- Options flow configuration now properly updates and reloads integration
- Service registration logging for troubleshooting

### Technical Details
- Added response validation: checks for "result" field and item structure
- Exponential backoff: waits 1s, 2s, 4s between retries on rate limit
- API timeout: 10 seconds per request (configurable via const.py)
- Max retries: 3 attempts per API request before failure

## [1.2.0] - 2026-02-13

### Added
- Initial release
- Home Assistant integration for Paprika Recipe Manager
- Support for Paprika API v2/v1 (with fallback)
- Grocery list sensor with aisle grouping
- Meal plan sensor (7-day forecast)
- Configurable refresh intervals
- Manual refresh service (`turmeric.refresh_all`)
- Automatic token re-authentication
- Debug logging support
- Dashboard card examples (Markdown)

### Features
- Secure credential storage
- Bearer token authentication
- Rate limit handling (429 responses)
- Automatic token expiration handling (401 responses)

## Known Limitations

- Paprika API v2 is not officially documented; this integration uses reverse-engineered endpoints
- Refresh intervals: minimum 1 minute, maximum 24 hours (1440 minutes)
- Rate limiting: Paprika API may throttle requests; increasing refresh intervals is recommended
- No support for recipes endpoint (currently groceries and meals only)

## Future Planned Updates

- [ ] Support for recipe data endpoint
- [ ] Support for additional meal fields (serving size, recipe links)
- [ ] Ingredient-level grocery list organization
- [ ] Custom meal filtering and categorization
- [ ] Integration with automation triggers (meal on specific date, etc.)
- [ ] Support for multiple Paprika accounts simultaneously