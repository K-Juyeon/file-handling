import os
import json

data_path = 'Z:\\data\\auto_labeling_results\\0801'

for paths, dirs, files in os.walk(data_path) :
    if 'with_bbox' in paths :
        filelist_wb = os.listdir(paths)
        filelist_wb_jpg = [file for file in filelist_wb if file.endswith('.jpg')]
        filelist_wob = os.listdir(paths.replace('with_bbox', 'without_bbox'))
        filelist_wob_jpg = [file for file in filelist_wob if file.endswith('.jpg')]
        json_path = [file for file in filelist_wb if file.endswith('.json')]

        if filelist_wb_jpg != filelist_wob_jpg :
            print(paths)

        with open(os.path.join(paths, json_path[0]), 'r', encoding="utf-8") as json_file:
            json_data_wb = json.load(json_file)

        with open(os.path.join(paths.replace("with_bbox", "without_bbox"), json_path[0]), 'r', encoding="utf-8") as json_file:
            json_data_wob = json.load(json_file)

        if json_data_wb != json_data_wob :
            print(json_path[0])