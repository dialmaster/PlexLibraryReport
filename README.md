# PlexLibraryReport

PlexLibraryReport is a Python script that generates a detailed report of your media library. It uses Sonarr for TV show statistics and Radarr for movie statistics, providing accurate information about your entire collection.

## Features

- Counts total number of TV series and movies in your library
- Calculates total number of episodes across all TV series
- Distinguishes between complete and partial TV series
- Categorizes movies by resolution (4K, 1080p+, 720p, Under 720p)
- Provides a breakdown of total and available episodes for TV series
- Displays statistics in formatted tables with colored output
- Supports command-line arguments for configuration and output options
- Includes progress bars for processing large libraries
- Implements error handling and logging for better debugging

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed
- Sonarr running and accessible
- Radarr running and accessible
- Sonarr and Radarr API keys

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
   pip install requests configparser prettytable colorama tqdm
   ```

## Configuration

1. Create a file named `plex_config.ini` in the project directory with the following content:
   ```ini
   [SONARR]
   baseurl = http://YOUR_SONARR_URL:YOUR_SONARR_PORT
   apikey = YOUR_SONARR_API_KEY

   [RADARR]
   baseurl = http://YOUR_RADARR_URL:YOUR_RADARR_PORT
   apikey = YOUR_RADARR_API_KEY
   ```

2. Replace `YOUR_SONARR_API_KEY` with your Sonarr API key. You can find this in Sonarr under Settings -> General.

3. Replace `YOUR_RADARR_API_KEY` with your Radarr API key. You can find this in Radarr under Settings -> General.

4. Update the `baseurl` for both Sonarr and Radarr if they are not running on the same machine or are using different ports.

## Usage

To run the script with default settings, ensure your virtual environment is activated, then execute:

```
python plex_library_stats.py
```

You can also use command-line arguments:

- `--config`: Specify a custom config file location (default is `plex_config.ini` in the current directory)
- `--output`: Specify a file to save the JSON output

Example:
```
python plex_library_stats.py --config my_config.ini --output results.json
```

The script will output the following information:

For Movies:
- Total number of movies
- Breakdown of movies by resolution category (4K, 1080p+, 720p, Under 720p, Unknown)

For TV Shows:
- Total number of TV series
- Total number of episodes
- Number of available episodes
- Number of complete series
- Number of partial series

## Troubleshooting

If you encounter any issues:

1. Check the `plex_library_stats.log` file for error messages and debugging information.
2. Ensure your `plex_config.ini` file is correctly set up and in the specified location.
3. Verify that your Sonarr and Radarr servers are running and accessible.
4. Check that you're using the correct API keys for both Sonarr and Radarr.
5. Make sure you've installed all required packages in your virtual environment.

If problems persist, please open an issue on the GitHub repository.

## Contributing

Contributions to PlexLibraryReport are welcome. Please feel free to submit a Pull Request.

## Acknowledgments

- Thanks to the creators of Sonarr and Radarr for providing comprehensive APIs for media management.

## Note

This script uses Sonarr for TV show information and Radarr for movie information. It does not directly interact with Plex, but provides statistics about the media that would typically be managed by Plex.