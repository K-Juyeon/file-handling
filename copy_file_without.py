import shutil
import os

data_path = 'Z:\\data\\auto_labeling_results\\0808'
output_path = 'Z:\\without_data\\auto_labeling_results'

if not os.path.exists(output_path) :
    os.makedirs(output_path)
# dt_list = ['0802', '0809', '0814', '0816', '0817', '0818', '0821', '0825', '0830', '0831', '0901', '0904', '0905', '0906', '0907', '0908']
# dt_list = ['0901', '0904', '0905', '0906', '0907', '0908', '0911']
dt_list = ['0808']
for paths, dirs, files in os.walk(data_path) :
    date = paths.split('\\')
    if len(date) == 4 :
        for paths, dirs, files in os.walk(paths) :
            if date[3] in dt_list :
                if 'without_bbox' in paths :
                    shutil.copytree(paths, paths.replace('data', 'without_data'))
            else : 
                print('PASS', paths)
                break
        print('COPY', paths)