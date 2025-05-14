import os
import requests

# Replace this with your Pixabay API key
PIXABAY_API_KEY = '50284110-3a3923dac6a2261e553dabc84'

def download_images(search_term, num_images, save_dir='images'):
    # Create the output directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Pixabay API endpoint to search for photos
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={search_term}&image_type=photo&per_page=200&page=1"

    # Track downloaded images
    downloaded = 0
    while downloaded < num_images:
        # Make the request to Pixabay API
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return

        # Get the JSON data
        data = response.json()
        images = data['hits']

        # Download each image
        for image in images:
            img_url = image['webformatURL']  # Use web format URL for faster download
            img_data = requests.get(img_url).content
            ext = img_url.split('.')[-1].split('?')[0]
            filename = os.path.join(save_dir, f"{search_term.replace(' ', '_')}_{downloaded+1}.{ext}")

            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded: {filename}")
            downloaded += 1

            if downloaded >= num_images:
                break
        
        # Increment page number for the next batch of images
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={search_term}&image_type=photo&per_page=200&page={((downloaded // 200) + 1)}"

if __name__ == "__main__":
    search_term = input("Enter the search term: ")
    while True:
        try:
            num_images = int(input("Enter the number of images to download: "))
            break
        except ValueError:
            print("Please enter a valid number.")

    download_images(search_term, num_images)
