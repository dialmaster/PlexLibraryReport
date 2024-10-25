# PlexLibraryReport

This repository contains two Python utilities for managing your Plex Media Server:
1. PlexLibraryReport - Generates detailed statistics about your media library
2. PlexContentRatingUpdater - Automatically updates content ratings based on configurable rules

## PlexLibraryReport

PlexLibraryReport is a Python script that generates a detailed report of your media library. It uses Sonarr for TV show statistics and Radarr for movie statistics, providing accurate information about your entire collection.

### Features

- Counts total number of TV series and movies in your library
- Calculates total number of episodes across all TV series
- Distinguishes between complete and partial TV series
- Categorizes movies by resolution (4K, 1080p+, 720p, Under 720p)
- Provides a breakdown of total and available episodes for TV series
- Displays statistics in formatted tables with colored output
- Supports command-line arguments for configuration and output options
- Includes progress bars for processing large libraries
- Implements error handling and logging for better debugging

## PlexContentRatingUpdater

PlexContentRatingUpdater is a Python script that automatically updates content ratings in your Plex libraries based on customizable rules. It's particularly useful for adding content ratings across media items that match specific patterns in their titles, eg, perhaps for items downloaded from Youtube.

### Features

- Updates content ratings based on title pattern matching
- Supports multiple rating rules via YAML configuration
- Can process specific libraries or all libraries
- Provides colorful console output with progress bars
- Includes detailed logging for troubleshooting
- Supports command-line arguments for flexible usage
- Can be automated via scheduled tasks

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed
- For PlexLibraryReport:
  - Sonarr running and accessible
  - Radarr running and accessible
  - Sonarr and Radarr API keys
- For PlexContentRatingUpdater:
  - Plex Media Server running and accessible
  - Plex token for API access

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/dialmaster/PlexLibraryReport.git
   cd PlexLibraryReport
   ```

2. Create a virtual environment:
   ```
   python -m venv plex_env
   ```

3. Activate the virtual environment:
   - On Windows (PowerShell):
     ```
     .\plex_env\Scripts\Activate.ps1
     ```
   - On macOS and Linux:
     ```
     source plex_env/bin/activate
     ```

4. Install the required packages:
   ```
   pip install requests configparser prettytable colorama tqdm plexapi pyyaml
   ```

## Configuration

### For PlexLibraryReport

Create a file named `plex_config.ini` with:
```ini
[SONARR]
baseurl = http://YOUR_SONARR_URL:YOUR_SONARR_PORT
apikey = YOUR_SONARR_API_KEY

[RADARR]
baseurl = http://YOUR_RADARR_URL:YOUR_RADARR_PORT
apikey = YOUR_RADARR_API_KEY
```

### For PlexContentRatingUpdater

1. Create or update `plex_config.ini` with:
```ini
[PLEX]
baseurl = http://localhost:32400
token = YOUR_PLEX_TOKEN
library = YOUR_LIBRARY_NAME
```

2. Create `rating_rules.yml` with your rating rules:
```yaml
rating_rules:
  - pattern: "pattern_to_match"
    rating: "desired_rating"
```

Example rule:
```yaml
rating_rules:
  - pattern: "BeckBroReacts"
    rating: "PG-13"
```

## Running the Scripts

You can run the scripts directly with Python, or create automation scripts for convenience.

### Direct Python Execution

For PlexLibraryReport:
```
python plex_library_stats.py [--config config_file.ini] [--output results.json]
```

For PlexContentRatingUpdater:
```
python plex_content_rating_updater.py [--config config_file.ini] [--rules rules_file.yml] [--library "Library Name"]
```

### PowerShell Automation

Create a PowerShell script (e.g., `run_plex_updater.ps1`):
```powershell
$ErrorActionPreference = "Stop"

# Change to the correct directory
Set-Location -Path "C:\Users\chris\plexlibraryreport"

# Activate the virtual environment
& ".\plex_env\Scripts\Activate.ps1"

# Run the Python script
python.exe .\plex_content_rating_updater.py

# Deactivate the virtual environment (optional but clean)
deactivate
```

This script can be scheduled to run automatically using Windows Task Scheduler.

## Troubleshooting

If you encounter any issues:

1. Check the respective log files:
   - `plex_library_stats.log` for PlexLibraryReport
   - `plex_rating_updater.log` for PlexContentRatingUpdater
2. Ensure your configuration files are correctly set up
3. Verify that your servers (Plex/Sonarr/Radarr) are running and accessible
4. Check that you're using the correct API keys and tokens
5. Make sure you've installed all required packages in your virtual environment

If problems persist, please open an issue on the GitHub repository.

## Contributing

Contributions to both utilities are welcome. Please feel free to submit a Pull Request.

## Note

PlexLibraryReport uses Sonarr and Radarr for media information, while PlexContentRatingUpdater interacts directly with your Plex Media Server through the Plex API.