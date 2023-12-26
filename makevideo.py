import cv2
import os
from tqdm import tqdm
from PIL import Image
import numpy as np

data_path = r"Z:\data_final"
output_path = r"Z:\makevideo"

for date in tqdm(os.listdir(data_path)) :
    modellist = os.listdir(os.path.join(data_path, date))
    for model in modellist :
        cliplist = os.listdir(os.path.join(data_path, date, model))
        if not os.path.exists(cliplist) :
            os.makedirs(cliplist)
        for clip in cliplist :
            final_path = os.path.join(data_path, date, model, clip, 'without_bbox')
            filelist = os.listdir(final_path)
            filelist_jpg = [file for file in filelist if file.endswith('.jpg')]
            filelist_json = [file for file in filelist if file.endswith('.json')]

            firstimage = np.array(Image.open(os.path.join(final_path, filelist_jpg[0])))

            video_path = os.path.join(output_path, date, model)
            height, width, _ = firstimage.shape

            video = cv2.VideoWriter(f"{os.path.join(video_path, video_path)}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

            for img in filelist_jpg:
                img = np.array(Image.open(os.path.join(final_path, img)))
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                video.write(img)

            video.release()
        