import configparser
import requests
from collections import defaultdict

def read_config():
    config = configparser.ConfigParser()
    config.read('plex_config.ini')
    return config['SONARR']['baseurl'], config['SONARR']['apikey']

# Read configuration
baseurl, apikey = read_config()

# Set up the API request
url = f"{baseurl}/api/v3/series"
headers = {
    "X-Api-Key": apikey
}

# Make the API request
response = requests.get(url, headers=headers)
series_data = response.json()

# Initialize counters
total_series = len(series_data)
total_episodes = 0
available_episodes = 0
complete_series = 0
partial_series = 0
series_stats = defaultdict(lambda: {'total_episodes': 0, 'available_episodes': 0})

# Process the data
for series in series_data:
    series_title = series['title']
    series_complete = True

    for season in series['seasons']:
        total_episodes += season['statistics']['totalEpisodeCount']
        available_episodes += season['statistics']['episodeFileCount']
        series_stats[series_title]['total_episodes'] += season['statistics']['totalEpisodeCount']
        series_stats[series_title]['available_episodes'] += season['statistics']['episodeFileCount']

        if season['statistics']['episodeFileCount'] < season['statistics']['totalEpisodeCount']:
            series_complete = False

    if series_complete:
        complete_series += 1
    else:
        partial_series += 1

# Print results
print(f"Total TV Series: {total_series}")
print(f"Total Episodes: {total_episodes}")
print(f"Available Episodes: {available_episodes}")
print(f"Complete Series: {complete_series}")
print(f"Partial Series: {partial_series}")

# Optionally, print details for each series
#for series, stats in series_stats.items():
#    print(f"\n{series}:")
#    print(f"  Total Episodes: {stats['total_episodes']}")
#    print(f"  Available Episodes: {stats['available_episodes']}")