import shutil
import os
import json
from tqdm import tqdm

attribute = {
    "gender" : {
        "na":"na",
        "m":"man", 
        "f":"woman"
        },

    "age_group" : {
        "na":"na",
        "if":"infant",
        "sc":"child",
        "tn":"teenager",
        "ya":"seniors",
        "ad":"old people"
        },


    "top_type" : {
        "na":"na",
        "jk":"jacket",
        "jp":"jumper",
        "lc":"long-coat",
        "sh":"shirt",
        "ts":"t-shirt"
        },

    "top_shape" : {
        "na":"na",
        "sh":"short-sleeve",
        "sl":"sleeveless",
        "lo":"long-sleeve"
        },

    "color" : {
        "na": " ",
        "be": "beige",
        "bk": "black",
        "bl": "blue",
        "br": "brown",
        "gr": "gray",
        "gn": "green",
        "nv": "navy",
        "or": "orange",
        "pk": "pink",
        "pu": "purple",
        "rd": "red",
        "wh": "white",
        "ye": "yellow",
        "ck": "check",
        "cb": "color-blocking",
        "pr": "printing",
        "st": "stripe",
        "pt": "pattern"
    },

    "bottom_type" : {
        "na":"na",
        "lp":"long-pants",
        "sp":"short-pants",
        "ls":"long-skirt",
        "ss":"short-skirt"
        },

    "hairstyle" : {
        "na":"na",
        "bl":"bald",
        "bh":"bobbed-hair",
        "ht":"hat",
        "hm":"helmet",
        "lh":"long-hair",
        "po":"ponytail",
        "sh":"short-hair"
        },

    "glasses" : {
        "na":"no-glasses",
        "gl":"glasses",
        "ng":"no-glasses",
        "sg":"sunglasses"
        },

    "bag" : {
        "na":"no-bag",
        "bp":"backpack",
        "cr":"carrier",
        "lb":"long-strap-bag",
        "nb":"no-bag",
        "sb":"short-strap-bag"
        },
    
    "mask" : {
        "na":"no-mask",
        "ma":"mask",
        "nm":"no-mask"
        },

    "walking_accessory" : {
        "na":"no-wf",
        "ca":"cane",
        "cr":"crutches",
        "no":"no-wf",
        "wh":"wheelchair",
        "wf":"wf"
        },

    "shoes" : {
        "na":"no-shoes",
        "bt":"boots",
        "lf":"loafers",
        "ns":"no-shoes",
        "sp":"slipper",
        "sk":"sneakers"
        }
}

data_path = r'Z:\data\auto_labeling_results'
before = "data"
after = "json_append"

for paths, dirs, files in os.walk(data_path) :
    json_files = os.listdir(paths)
    json_file = [file for file in json_files if file.endswith('.json')]
    image_file = [file for file in json_files if file.endswith('.jpg')]
    if len(json_file) > 0 and "without_bbox" in paths:
        with open(os.path.join(paths, json_file[0]), 'r', encoding="utf-8") as jb_file:
            data = json.load(jb_file)

        images = data['images']
        annotations = data['annotations']

        if len(images) == 0 :
            try :
                shutil.copytree(paths, paths.replace(before, after))
            except :
                pass
            print(paths)
            for i, image in tqdm(enumerate(image_file), desc="UPDATE") :
                image_atts = image.split("_")
                image_atts_sub = image_atts[14].split("-")

                json_images = {
                    "id": i + 1,
                    "width": 1920,
                    "height": 1080,
                    "file_name": image,
                    "licence": 0,
                    "flickr_url": "",
                    "cooc_url": "",
                    "date_captured": 0
                }
                json_ann = {
                    "id": i + 1,
                    "image_id": i + 1,
                    "category_id": 1,
                    "segmentation": [],
                    "area": 0,
                    "bbox": [
                        1124,
                        509,
                        109,
                        232
                    ],
                    "iscrowd": 0,
                    "attributes": {
                        "actor_id": image_atts_sub[0], 
                        "gender": [val for key, val in attribute["gender"].items() if key == image_atts[1]][0],
                        "age_group": [val for key, val in attribute["age_group"].items() if key == image_atts[2]][0],
                        "top_type": [val for key, val in attribute["top_type"].items() if key == image_atts[3]][0],
                        "top_shape": [val for key, val in attribute["top_shape"].items() if key == image_atts[4]][0],
                        "top_color": [val for key, val in attribute["color"].items() if key == image_atts[5]][0],
                        "bottom_type": [val for key, val in attribute["bottom_type"].items() if key == image_atts[6]][0],
                        "bottom_color": [val for key, val in attribute["color"].items() if key == image_atts[7]][0],
                        "hairstyle": [val for key, val in attribute["hairstyle"].items() if key == image_atts[8]][0],
                        "glasses": [val for key, val in attribute["glasses"].items() if key == image_atts[9]][0],
                        "bag": [val for key, val in attribute["bag"].items() if key == image_atts[10]][0],
                        "mask": [val for key, val in attribute["mask"].items() if key == image_atts[11]][0],
                        "walking_accessory": [val for key, val in attribute["walking_accessory"].items() if key == image_atts[12]][0],
                        "shoes": [val for key, val in attribute["shoes"].items() if key == image_atts[13]][0],
                        "inner_color": [val for key, val in attribute["color"].items() if key == image_atts_sub[1]][0],
                        "top_check": True if [val for key, val in attribute["color"].items() if key == image_atts[5]][0] == "check" else False,
                        "top_stripe": True if [val for key, val in attribute["color"].items() if key == image_atts[5]][0] == "stripe" else False,
                        "top_color_blocking": True if [val for key, val in attribute["color"].items() if key == image_atts[5]][0] == "color-blocking" else False,
                        "top_printing": True if [val for key, val in attribute["color"].items() if key == image_atts[5]][0] == "printing" else False,
                        "top_color1": [val for key, val in attribute["color"].items() if key == image_atts_sub[2]][0],
                        "top_color2": [val for key, val in attribute["color"].items() if key == image_atts_sub[3]][0],
                        "top_color3": [val for key, val in attribute["color"].items() if key == image_atts_sub[4]][0],
                        "bottom_pattern": True if [val for key, val in attribute["color"].items() if key == image_atts[7]][0] == "pattern" else False,
                        "bottom_color1": [val for key, val in attribute["color"].items() if key == image_atts_sub[5]][0],
                        "bottom_color2": [val for key, val in attribute["color"].items() if key == image_atts_sub[6]][0],
                        "occluded": False,
                        "rotation": 0.0,
                        "track_id": 0,
                        "keyframe": True
                    }
                }
                
                images.append(json_images)
                annotations.append(json_ann)

                with open(os.path.join(paths.replace(before, after), json_file[0]), 'w', encoding="utf-8") as ja_file:
                    json.dump(data, ja_file)
                
                