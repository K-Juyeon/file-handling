import os

data_path = r"Z:\video\make_video"

for paths, dirs, files in os.walk(data_path) :
        json_files = os.listdir(paths)
        json_file = [file for file in json_files if file.endswith('.json')]
        img_files = os.listdir(paths)
        img_file = [file for file in img_files if file.endswith('.jpg')]
        if len(json_file) > 0 and len(img_file) > 0:
            video_paths = paths.replace(r"data_final", r"video\make_video").split("\\")
            video_path = "\\".join(video_paths[0:-1])
            if not os.path.exists(video_path) :
                print(f"{paths}")