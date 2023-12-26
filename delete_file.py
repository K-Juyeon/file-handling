import os

data_path = "Z:\\temp\\auto_labeling_results"

for paths, dirs, files in os.walk(data_path) :
    filelist = os.listdir(paths)
    filelist_jpg = [file for file in filelist if file.endswith('.jpg')]
    for file in filelist_jpg :
        if paths.split('\\')[4].endswith('-1') :# 짝수지우기
            if int(file[-5]) % 2 == 1 :
                print(os.path.join(paths, file))
                os.remove(os.path.join(paths, file))
        else : #홀수지우기
            if int(file[-5]) % 2 == 0 :
                print(os.path.join(paths, file))
                os.remove(os.path.join(paths, file))