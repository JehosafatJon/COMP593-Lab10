import requests as rq
import image_lib

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
    response = rq.get(f"{POKE_API_URL}?limit={limit}&offset={offset}")

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

    poke_dict = search_pokemon(pokemon)
    if poke_dict == None:
        return False

    img_url = poke_dict['sprites']['other']['official-artwork']['front_shiny']

    img_data = image_lib.download_image(img_url)
    if img_data == None:
        return False

    img_path = f"{dir}\\{poke_dict['name']}.{img_url.split('.')[-1]}"

    if image_lib.save_image_file(img_data, img_path):
        return img_path
    return False

if __name__ == '__main__':
    main()