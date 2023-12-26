import os
import json
import shutil

data_path = r'Z:\workin\검수완\1204'
output_path = r'Z:\att_json'

if not os.path.exists(output_path) :
    os.makedirs(output_path)

for paths, dirs, files in os.walk(data_path) :
    if 'without_bbox' in paths :
        filelist_wb = os.listdir(paths)
        json_path = [file for file in filelist_wb if file.endswith('.json')]

        with_path = os.path.join(paths, json_path[0])
        
        if len(json_path) > 0 :
            shutil.copy2(with_path, os.path.join(output_path, json_path[0]))