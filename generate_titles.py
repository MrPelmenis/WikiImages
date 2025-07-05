import requests
import random

def get_random_wikipedia_titles(count=100):
    """Get random Wikipedia titles using the API"""
    
    print(f"Generating {count} random Wikipedia titles...")
    
    # Wikipedia API endpoint
    api_url = "https://en.wikipedia.org/w/api.php"
    
    # Categories to get diverse titles
    categories = [
        "Animals", "Countries", "Cities", "Scientists", "Artists", 
        "Historical_events", "Mountains", "Rivers", "Plants", "Foods",
        "Technologies", "Sports", "Music", "Literature", "Movies",
        "Space", "Chemistry", "Physics", "Biology", "Mathematics"
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    all_titles = []
    
    for category in categories:
        try:
            # Get pages from category
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'categorymembers',
                'cmtitle': f'Category:{category}',
                'cmlimit': 20,  # Get 20 pages per category
                'cmtype': 'page'
            }
            
            response = session.get(api_url, params=params, timeout=10)
            data = response.json()
            
            if 'query' in data and 'categorymembers' in data['query']:
                for member in data['query']['categorymembers']:
                    title = member['title']
                    # Remove "Category:" prefix if present
                    if title.startswith('Category:'):
                        continue
                    # Remove namespace prefixes
                    if ':' in title and not title.startswith('Main Page'):
                        continue
                    all_titles.append(title)
            
        except Exception as e:
            print(f"Error getting category {category}: {e}")
    
    # If we don't have enough titles, add some generic ones
    generic_titles = [
        "Cat", "Dog", "Car", "House", "Tree", "Mountain", "Ocean", "City", "Flower", "Bird",
        "Sun", "Moon", "Star", "Planet", "River", "Lake", "Forest", "Desert", "Island", "Beach",
        "Book", "Computer", "Phone", "Camera", "Clock", "Chair", "Table", "Door", "Window", "Road",
        "Bridge", "Tower", "Castle", "Church", "School", "Hospital", "Airport", "Station", "Park", "Garden",
        "Apple", "Banana", "Orange", "Grape", "Strawberry", "Blueberry", "Cherry", "Peach", "Pear", "Lemon",
        "Lion", "Tiger", "Elephant", "Giraffe", "Zebra", "Monkey", "Bear", "Wolf", "Fox", "Deer",
        "Eagle", "Hawk", "Owl", "Penguin", "Duck", "Swan", "Peacock", "Parrot", "Crow", "Sparrow",
        "Rose", "Tulip", "Daisy", "Lily", "Orchid", "Sunflower", "Dandelion", "Poppy", "Iris", "Carnation",
        "Pizza", "Hamburger", "Sushi", "Pasta", "Salad", "Soup", "Bread", "Cake", "Ice Cream", "Chocolate",
        "Guitar", "Piano", "Violin", "Drums", "Trumpet", "Saxophone", "Flute", "Clarinet", "Bass", "Cello"
    ]
    
    all_titles.extend(generic_titles)
    
    # Remove duplicates and randomize
    unique_titles = list(set(all_titles))
    random.shuffle(unique_titles)
    
    # Take the first 'count' titles
    final_titles = unique_titles[:count]
    
    # Save to file
    with open('titles.txt', 'w', encoding='utf-8') as f:
        for title in final_titles:
            f.write(f"{title}\n")
    
    print(f"Generated {len(final_titles)} unique titles and saved to titles.txt")
    print("Sample titles:", final_titles[:10])
    
    return final_titles

if __name__ == "__main__":
    get_random_wikipedia_titles(10) 