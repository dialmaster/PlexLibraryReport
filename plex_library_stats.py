import configparser
import requests
from prettytable import PrettyTable
from collections import Counter
import argparse
import json
from tqdm import tqdm
import logging
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

logging.basicConfig(filename='plex_library_stats.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return (
        config['RADARR']['baseurl'],
        config['RADARR']['apikey'],
        config['SONARR']['baseurl'],
        config['SONARR']['apikey']
    )

def get_resolution_category(resolution):
    if resolution == 'Unknown':
        return 'Unknown'
    try:
        width = int(resolution.split('x')[0])
        if width >= 3840:
            return '4K'
        elif width >= 1920:
            return '1080p+'
        elif width >= 1280:
            return '720p'
        else:
            return 'Under 720p'
    except:
        return 'Unknown'

def get_movie_stats(baseurl, apikey):
    url = f"{baseurl}/api/v3/movie"
    headers = {"X-Api-Key": apikey}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        movies_data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching movie data: {e}")
        return None, None

    category_counts = Counter()

    for movie in tqdm(movies_data, desc="Processing movies"):
        if movie.get('hasFile', False) and 'movieFile' in movie and movie['movieFile']:
            media_info = movie['movieFile'].get('mediaInfo', {})
            resolution = media_info.get('resolution', 'Unknown')
            category = get_resolution_category(resolution)
            category_counts[category] += 1

    total_movies = sum(category_counts.values())
    percentages = {cat: (count / total_movies) * 100 for cat, count in category_counts.items()}

    table = PrettyTable()
    table.field_names = ["Resolution", "Count", "Percentage"]
    table.align["Resolution"] = "l"
    table.align["Count"] = "r"
    table.align["Percentage"] = "r"

    for category in ['4K', '1080p+', '720p', 'Under 720p', 'Unknown']:
        count = category_counts[category]
        percentage = percentages.get(category, 0)
        table.add_row([category, count, f"{percentage:.2f}%"])

    return total_movies, table

def get_tv_stats(baseurl, apikey):
    url = f"{baseurl}/api/v3/series"
    headers = {"X-Api-Key": apikey}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        series_data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching TV data: {e}")
        return None

    total_series = len(series_data)
    total_episodes = 0
    available_episodes = 0
    complete_series = 0
    partial_series = 0

    for series in tqdm(series_data, desc="Processing TV series"):
        series_complete = True
        for season in series['seasons']:
            total_episodes += season['statistics']['totalEpisodeCount']
            available_episodes += season['statistics']['episodeFileCount']
            if season['statistics']['episodeFileCount'] < season['statistics']['totalEpisodeCount']:
                series_complete = False

        if series_complete:
            complete_series += 1
        else:
            partial_series += 1

    table = PrettyTable()
    table.field_names = ["Statistic", "Value"]
    table.align["Statistic"] = "l"
    table.align["Value"] = "r"
    table.add_row(["Total TV Series", total_series])
    table.add_row(["Total Episodes", total_episodes])
    table.add_row(["Available Episodes", available_episodes])
    table.add_row(["Complete Series", complete_series])
    table.add_row(["Partial Series", partial_series])

    return table

def main():
    parser = argparse.ArgumentParser(description="Generate Plex library statistics")
    parser.add_argument("--config", default="plex_config.ini", help="Path to configuration file")
    parser.add_argument("--output", help="Output file for JSON results")
    args = parser.parse_args()

    radarr_baseurl, radarr_apikey, sonarr_baseurl, sonarr_apikey = read_config(args.config)

    results = {}

    print(Fore.CYAN + Style.BRIGHT + "Movie Statistics:" + Style.RESET_ALL)
    total_movies, movie_table = get_movie_stats(radarr_baseurl, radarr_apikey)
    if total_movies is not None:
        print(Fore.GREEN + f"Total Movies (downloaded): {total_movies}" + Style.RESET_ALL)
        print(Fore.YELLOW + movie_table.get_string() + Style.RESET_ALL)
        results['movies'] = {
            'total': total_movies,
            'table': movie_table.get_string()
        }
    else:
        print(Fore.RED + "Failed to retrieve movie statistics." + Style.RESET_ALL)

    print("\n" + Fore.CYAN + Style.BRIGHT + "TV Show Statistics:" + Style.RESET_ALL)
    tv_table = get_tv_stats(sonarr_baseurl, sonarr_apikey)
    if tv_table is not None:
        print(Fore.YELLOW + tv_table.get_string() + Style.RESET_ALL)
        results['tv_shows'] = {
            'table': tv_table.get_string()
        }
    else:
        print(Fore.RED + "Failed to retrieve TV show statistics." + Style.RESET_ALL)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(Fore.GREEN + f"Results saved to {args.output}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()