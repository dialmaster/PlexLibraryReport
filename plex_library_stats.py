import configparser
import requests
from prettytable import PrettyTable
from collections import Counter, defaultdict

def read_config():
    config = configparser.ConfigParser()
    config.read('plex_config.ini')
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
    response = requests.get(url, headers=headers)
    movies_data = response.json()

    category_counts = Counter()

    for movie in movies_data:
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
    response = requests.get(url, headers=headers)
    series_data = response.json()

    total_series = len(series_data)
    total_episodes = 0
    available_episodes = 0
    complete_series = 0
    partial_series = 0

    for series in series_data:
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
    radarr_baseurl, radarr_apikey, sonarr_baseurl, sonarr_apikey = read_config()

    print("Movie Statistics:")
    total_movies, movie_table = get_movie_stats(radarr_baseurl, radarr_apikey)
    print(f"Total Movies (downloaded): {total_movies}")
    print(movie_table)

    print("\nTV Show Statistics:")
    tv_table = get_tv_stats(sonarr_baseurl, sonarr_apikey)
    print(tv_table)

if __name__ == "__main__":
    main()