import requests
import os
from pathlib import Path
from titleToimage import get_wikipedia_image_url
import time

def process_titles_and_download():
    # Create directories
    download_dir = Path("images")
    download_dir.mkdir(exist_ok=True)
    
    # Read titles from file
    with open('titles.txt', 'r', encoding='utf-8') as f:
        titles = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(titles)} titles in titles.txt")
    print(f"Images will be saved to: {download_dir}")
    print()
    
    # Create session for downloads
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Process each title
    image_urls = []
    downloaded = 0
    failed = 0
    
    for i, title in enumerate(titles, 1):
        print(f"Processing {i}/{len(titles)}: {title}")
        
        try:
            # Get image URL using your function
            image_url = get_wikipedia_image_url(title)
            
            if image_url:
                print(f"  Found image: {image_url}")
                image_urls.append(f"{title}: {image_url}")
                
                # Download the image and name it after the title
                original_filename = image_url.split('/')[-1]
                # Get file extension
                if '.' in original_filename:
                    extension = '.' + original_filename.split('.')[-1]
                else:
                    extension = '.jpg'  # Default extension
                
                # Create safe filename from title
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_title = safe_title.replace(' ', '_')
                filename = f"{safe_title}{extension}"
                local_path = download_dir / filename
                
                # Skip if already exists
                if local_path.exists():
                    print(f"  Already exists: {filename}")
                    downloaded += 1
                else:
                    # Download the image
                    response = session.get(image_url, timeout=30)
                    response.raise_for_status()
                    
                    # Save the image
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"  Downloaded: {filename}")
                    downloaded += 1
            else:
                print(f"  No image found for: {title}")
                failed += 1
            
            # Small delay
            time.sleep(1)
            
        except Exception as e:
            print(f"  Failed to process {title}: {e}")
            failed += 1
    
    # Save all image URLs to a single file
    with open('image_urls.txt', 'w', encoding='utf-8') as f:
        for url_line in image_urls:
            f.write(f"{url_line}\n")
    
    print(f"\nSummary:")
    print(f"Successfully processed: {downloaded}")
    print(f"Failed: {failed}")
    print(f"Images saved to: {download_dir}")
    print(f"URLs saved to: image_urls.txt")
    
    return downloaded, failed

if __name__ == "__main__":
    process_titles_and_download() 