import configparser
import logging
from tqdm import tqdm
from colorama import init, Fore, Style
import argparse
import yaml
from plexapi.server import PlexServer

# Initialize colorama
init(autoreset=True)

logging.basicConfig(
    filename='plex_rating_updater.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_config(config_file):
    """Read configuration from ini file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return (
        config['PLEX']['baseurl'],
        config['PLEX']['token'],
        config['PLEX'].get('library', None)  # Get library name from config, defaults to None
    )

def load_rating_rules(rules_file):
    """Load rating rules from YAML file."""
    try:
        with open(rules_file, 'r') as f:
            rules = yaml.safe_load(f)
            return rules.get('rating_rules', [])
    except Exception as e:
        logging.error(f"Error loading rating rules: {e}")
        return []

def should_update_rating(title, rules):
    """Check if title matches any rules and return the corresponding rating."""
    for rule in rules:
        pattern = rule.get('pattern')
        rating = rule.get('rating')
        if pattern and rating and pattern.lower() in title.lower():
            return rating
    return None

def update_library_ratings(plex, rules, library_name=None):
    """Update ratings for all items in specified library or all libraries."""
    updates = 0
    
    # Get all libraries or specific library if name provided
    if library_name:
        try:
            libraries = [plex.library.section(library_name)]
        except Exception as e:
            print(Fore.RED + f"Error: Library '{library_name}' not found")
            logging.error(f"Library not found: {library_name}")
            return updates
    else:
        libraries = plex.library.sections()

    for library in libraries:
        print(Fore.CYAN + f"\nProcessing library: {library.title}")
        
        # Process all items in the library
        items = library.all()
        for item in tqdm(items, desc=f"Processing {library.title}"):
            title = item.title
            new_rating = should_update_rating(title, rules)
            
            if new_rating and item.contentRating != new_rating:
                try:
                    # Update the content rating
                    item.editContentRating(new_rating)
                    updates += 1
                    logging.info(f"Updated rating for '{title}' to {new_rating}")
                    print(Fore.GREEN + f"Updated: {title} → {new_rating}")
                except Exception as e:
                    logging.error(f"Error updating '{title}': {e}")
                    print(Fore.RED + f"Failed to update: {title}")

    return updates

def main():
    parser = argparse.ArgumentParser(description="Update Plex content ratings based on title patterns")
    parser.add_argument("--config", default="plex_config.ini", help="Path to configuration file")
    parser.add_argument("--rules", default="rating_rules.yml", help="Path to rating rules YAML file")
    parser.add_argument("--library", help="Specific library to process (overrides config file)")
    args = parser.parse_args()

    # Load configurations
    try:
        baseurl, token, config_library = read_config(args.config)
    except Exception as e:
        print(Fore.RED + f"Error reading config file: {e}")
        print("Make sure your plex_config.ini contains:")
        print("[PLEX]")
        print("baseurl = http://localhost:32400")
        print("token = your_plex_token")
        print("library = your_library_name  # Optional")
        return

    # Load rules
    rules = load_rating_rules(args.rules)
    if not rules:
        print(Fore.RED + "No rating rules found. Please check your rules file.")
        return

    # Connect to Plex
    try:
        plex = PlexServer(baseurl, token)
    except Exception as e:
        print(Fore.RED + f"Error connecting to Plex: {e}")
        return

    print(Fore.CYAN + Style.BRIGHT + "Starting Content Rating Updates..." + Style.RESET_ALL)
    
    # Use command line library argument if provided, otherwise use config file library
    library_name = args.library if args.library else config_library
    
    # Update ratings
    total_updates = update_library_ratings(plex, rules, library_name)
    
    print(Fore.GREEN + f"\nUpdates completed: {total_updates} items updated")

if __name__ == "__main__":
    main()