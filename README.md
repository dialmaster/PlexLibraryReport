# PlexLibraryReport

PlexLibraryReport is a Python script that generates a detailed report of your Plex TV Shows library. It provides statistics on the total number of TV series, episodes, complete series, and partial series in your Plex library.

## Features

- Counts total number of TV series in your Plex library
- Calculates total number of episodes across all series
- Distinguishes between complete and partial series
- Provides a breakdown of total and available episodes for each series

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed
- A Plex server running and accessible
- Plex authentication token

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
   pip install plexapi configparser
   ```

## Configuration

1. Create a file named `plex_config.ini` in the project directory with the following content:
   ```ini
   [PLEX]
   baseurl = http://YOUR_PLEX_URL:YOUR_PLEX_PORT
   token = YOUR_PLEX_TOKEN
   ```

2. Replace `YOUR_PLEX_TOKEN` with your actual Plex authentication token. You can find your token by following the instructions [here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/).

3. If your Plex server is not running on the same machine or is using a different port, update the `baseurl` accordingly.

## Usage

To run the script, ensure your virtual environment is activated, then execute:

```
python plex_tv_stats.py
```

The script will output the following information:
- Total number of TV series
- Total number of episodes
- Number of complete series
- Number of partial series
- A breakdown of total and available episodes for each series

## Troubleshooting

If you encounter any issues:

1. Ensure your `plex_config.ini` file is correctly set up and in the same directory as the script.
2. Verify that your Plex server is running and accessible.
3. Check that you're using the correct Plex authentication token.
4. Make sure you've installed all required packages in your virtual environment.

If problems persist, please open an issue on the GitHub repository.

## Contributing

Contributions to PlexLibraryReport are welcome. Please feel free to submit a Pull Request.

## Acknowledgments

- Thanks to the creators of PlexAPI for providing a Python interface to the Plex API.