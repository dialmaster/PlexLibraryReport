import configparser
from plexapi.server import PlexServer
from collections import defaultdict

def read_config():
    config = configparser.ConfigParser()
    config.read('plex_config.ini')
    return config['PLEX']['baseurl'], config['PLEX']['token']

# Read configuration
baseurl, token = read_config()

# Connect to your Plex server
plex = PlexServer(baseurl, token)

# Get the TV Shows library
tv_library = plex.library.section('TV Shows')  # Change 'TV Shows' if your library has a different name

total_series = 0
total_episodes = 0
complete_series = 0
partial_series = 0
series_stats = defaultdict(lambda: {'total_episodes': 0, 'available_episodes': 0})

# Iterate through all TV series
for show in tv_library.all():
    total_series += 1
    show_complete = True
    
    for season in show.seasons():
        for episode in season.episodes():
            series_stats[show.title]['total_episodes'] += 1
            if episode.media:  # Check if the episode has media
                series_stats[show.title]['available_episodes'] += 1
                total_episodes += 1
            else:
                show_complete = False

    if show_complete:
        complete_series += 1
    else:
        partial_series += 1

# Print results
print(f"Total TV Series: {total_series}")
print(f"Total Episodes: {total_episodes}")
print(f"Complete Series: {complete_series}")
print(f"Partial Series: {partial_series}")

# Optionally, print details for each series
#for series, stats in series_stats.items():
#    print(f"\n{series}:")
#    print(f"  Total Episodes: {stats['total_episodes']}")
#    print(f"  Available Episodes: {stats['available_episodes']}")