import os
import time
import requests
import io
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# Set dataset path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(SCRIPT_DIR, "../model/dataset")

def setup_driver():
    """Setup Chrome WebDriver with necessary options."""
    options = Options()
    options.add_argument("--incognito")  # Incognito mode to avoid tracking
    options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
    options.add_argument("--disable-dev-shm-usage")  # Fix crashes
    options.add_argument("--no-sandbox")  # Prevent issues in some environments
    options.add_argument("--headless")  # Run in the background (remove if you want to see browser actions)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

def handle_google_consent(driver):
    """Handle Google's consent popup if present."""
    try:
        consent_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "I agree")]'))
        )
        consent_button.click()
        print("Accepted Google's consent form.")
        time.sleep(2)
    except Exception:
        print("No consent form detected.")

def scroll_to_load_images(driver, scroll_pause_time=2, max_scrolls=10):
    """Scroll down multiple times to load more images."""
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # No new images loaded, exit scrolling loop
        last_height = new_height

def fetch_image_urls(query, max_links_to_fetch, driver):
    """Fetch image URLs from Google Images based on search query."""
    
    search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    print(f"Searching for images: {query}")
    driver.get(search_url)

    # Handle consent popup if present
    handle_google_consent(driver)

    # Scroll to load enough images
    scroll_to_load_images(driver)

    time.sleep(3)  # Allow time for images to load

    # Locate all image elements
    thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
    print(f"Found {len(thumbnails)} thumbnails. Extracting full image URLs...")

    image_urls = set()
    
    for img in thumbnails:
        try:
            img.click()
            time.sleep(1)  # Allow image to load

            actual_images = driver.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
            for actual_image in actual_images:
                url = actual_image.get_attribute("src")
                if url and "http" in url and not url.startswith("data:image/"):
                    image_urls.add(url)

            if len(image_urls) >= max_links_to_fetch:
                break  # Stop once enough images are collected
        except Exception as e:
            print(f"Error clicking image: {e}")

    print(f"Extracted {len(image_urls)} image URLs.")
    return image_urls

def persist_image(folder_path, url):
    """Download and save an image from a given URL."""
    try:
        image_content = requests.get(url, timeout=10).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')

        # Ensure the folder exists
        os.makedirs(folder_path, exist_ok=True)

        # Create a unique filename
        file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + ".jpg")
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)

        print(f"Saved: {url} → {file_path}")
    except Exception as e:
        print(f"ERROR: Could not save {url} - {e}")

def search_and_download(search_term, target_path=DATASET_PATH, number_images=50):
    """Search for images and save them into a folder named after the search term."""
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    # Setup WebDriver
    driver = setup_driver()

    try:
        image_urls = fetch_image_urls(search_term, number_images, driver)
        if not image_urls:
            print(f"No images found for {search_term}")
            return

        for url in image_urls:
            persist_image(target_folder, url)
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        driver.quit()

# SEARCH QUERIES
query_list = ["Tara Sutaria", "Tiger Shroff", "Alia Bhatt", "Hrithik Roshan", "Varun Dhawan"]

for query in query_list:
    search_and_download(query)
