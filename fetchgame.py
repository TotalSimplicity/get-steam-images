from steamgrid import SteamGridDB, StyleType, PlatformType, MimeType, ImageType
import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()
sgdb = SteamGridDB(os.getenv("STEAMGRID_APIKEY"))


def sanitize_filename(name):
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = name.replace(' ', '_')
    return name

def download_image(image, folder, image_type):
    if image:
        url = image.url
        mime = image.mime
        # Handle Microsoft icon mime type
        if mime == "image/vnd.microsoft.icon":
            ext = "png"
        else:
            ext = mime.split('/')[1]
        filename = os.path.join(folder, f"{image_type}.{ext}")
        print(f"Downloading {image_type} from {url} to {filename}")
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {image_type} successfully.")
        else:
            print(f"Failed to download {image_type}. Status code: {response.status_code}")
    else:
        print(f"No {image_type} found.")


search_term = input("Enter the game name to search: ")
result = sgdb.search_game(search_term)
game_name = result[0].name
game_id = result[0].id



print("Found game:", game_name, "with ID:", game_id)

folder_name = sanitize_filename(game_name)
print("Creating folder:", folder_name)
os.makedirs(folder_name, exist_ok=True)

print("Downloading images...")
grid = sgdb.get_grids_by_gameid([game_id])[0]
hero = sgdb.get_heroes_by_gameid([game_id])[0]
logo = sgdb.get_logos_by_gameid([game_id])[0]
icon = sgdb.get_icons_by_gameid([game_id])[0]


download_image(grid, folder_name, "grid")
download_image(hero, folder_name, "hero")
download_image(logo, folder_name, "logo")
download_image(icon, folder_name, "icon")


