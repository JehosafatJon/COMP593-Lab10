import requests as rq
import image_lib
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon'

def main():

    ### TEST ###

    download_pokemon_artwork("pikachu","C:\\temp")


    pass

def search_pokemon(search_term):
    """ Gets information about a pokemon from the pokeapi and returns a dictionary with that information

    Args:
        search_term (str/int): pokemon name (str) OR pokedex number (int)

    Returns:
        dict: A dictionary of information about the pokemon
    """
    
    # Cleans the search term and prints live synopsis
    search_term = str(search_term).strip().lower()
    print(f'Retrieving information for {search_term.title()if search_term.isalpha() else "pokedex #"+search_term}...', end=' ') # Proper output if word or number
    
    # Gets information from pokeapi and checks if succesful
    response = rq.get(f"{POKE_API_URL}/{search_term}")
    if response.ok:
        print('Success!')
        return response.json() # returns dict of pokemon info
    else:
        print('Failed!')
        print(f"Response code: {response.status_code} {response.reason}")
    
    return 

def get_pokemon_names(limit=10000, offset=0):
    """Gets every pokemon from PokeAPI and returns 
    a list ofnames

    Args:
        limit (int, optional): Set a maximum number of pokemon to request. Defaults to 10000 for all pokemon.
        offset (int, optional): The starting index for the API to return results for. Defaults to 0 for the beginning/all.

    Returns:
        poke_name_list (list): A list of strings, all pokemon names 
    """

    # PokeAPI Request
    response = rq.get(f"{POKE_API_URL}?limit={limit}&offset={offset}")

    # Prints status of request
    # If request successful, format and return all pokemon names
    if response.ok:
        print('Success!')
        resp_dict = response.json()
        poke_name_list = [pokemon['name'] for pokemon in resp_dict['results']]
        return poke_name_list 
    else:
        print('Failed!')
        print(f"Response code: {response.status_code} {response.reason}")

    return

def download_pokemon_artwork(pokemon, dir):
    """Given a specified pokemon and directory, downloads and saves an image from a sprite URL proided by PokeAPI to a resource image directory within the specified directory.

    Args:
        pokemon (str): The name of the pokemon
        dir (str): The path of the script directory

    Returns:
        str: The full path of the saved image
    """

    # Get a dictionary of info of the selected pokemon and checks success
    poke_dict = search_pokemon(pokemon)
    if poke_dict == None:
        return False

    # Determine sprite URL from info, download the image and checks success
    img_url = poke_dict['sprites']['other']['official-artwork']['front_shiny']
    img_data = image_lib.download_image(img_url)
    if img_data == None:
        return False

    # Creates an image resource directory within the 
    # given (script) directory, if doesnt exist
    img_dir = os.path.join(dir, 'pokemon_images')
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    # Construct the file path of the img file to save,
    # then save the image data, and checks success
    img_path = f"{img_dir}\\{poke_dict['name']}.{img_url.split('.')[-1]}"
    if image_lib.save_image_file(img_data, img_path):
        return img_path # Returns saved image path
    return False

if __name__ == '__main__':
    main()