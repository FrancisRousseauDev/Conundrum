from pydub import AudioSegment
from excel_convert import convertExcel
import numpy as np
index = 0
def overlay(all_layers, id):
    file_name = 'output/' + str(id) + ".mp3"
    print(all_layers)
    sound1 = all_layers[0]
    for index, remaining in enumerate(all_layers):
        if index != 0:
            sound1 = sound1.overlay(remaining, position=0)
    sound1.export(file_name, format="mp3")

def create_new_sound(layers, all_images):
    global index
    image = {}

    for layer in layers:
        image[layer["name"]] = np.random.choice(layer["values"], size=1, replace=False, p=layer["weights"])[0]

    print(str(index) + ') ' + str(image))
    index = index + 1
    if image in all_images:
        return create_new_sound(layers, all_images)
    else:
       return image

def start_processing(layers, number):
    print('Generation images started')

    all_traits = {}
    for trait in layers:
        all_traits[trait["name"]] = {}
        for x, key in enumerate(trait["values"]):
            all_traits[trait["name"]][key] = trait["filename"][x]

    all_sounds = []
    for i in range(number):
        image = create_new_sound(layers, all_sounds)
        all_sounds.append(image)
    generate_sounds(layers, all_sounds, all_traits, number)

def generate_sounds(layers, all, traits, number):
    # add to every item a token ID
    i = 0
    for item in all:
        item["tokenId"] = i
        i += 1

    #generate_metadata(all, number)

    # go over every item with specifics and generate an image
    for item in all:

        allLayers = []
        for index, attr in enumerate(item):
            # for each layer except the token ID add it to layers
            # example now is:
            # layer[0] = background_yellow.png
            # layer[1] = foreground_yellow.png
            if attr != 'tokenId':
                allLayers.append([])
                allLayers[index] = AudioSegment.from_mp3(f'{layers[index]["trait_path"]}/{traits[attr][item[attr]]}')

        # based on the number of layers we will compose an image
        overlay(allLayers, item['tokenId'])

if __name__ == '__main__':
    start_processing(convertExcel(), 10)
