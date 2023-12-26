import cv2
import os
import json
from PIL import Image, ImageDraw
import shutil
import argparse
from distutils.dir_util import copy_tree

# top_folder = r"Z:\data\auto_labeling_results\0720"

def _get_parser():
    ''' Get arguments parser '''
    parser = argparse.ArgumentParser(description='File Count')
    parser.add_argument('--p', type=str,
                        default='',
                        help='Count File Path')

    return parser

def main():
    parser = _get_parser()
    opt = parser.parse_args()

    top_folder = opt.p

    # 최상위 폴더 내의 모든 폴더 검색
    for paths, dirs, _ in os.walk(top_folder):
        filelist = os.listdir(paths)
        filelist_json = [file for file in filelist if file.endswith('.json')]
        if "without_bbox" in paths :
            if len(filelist_json) >= 1 :
                if not os.path.exists(paths.replace("without_bbox", "with_bbox")):
                    os.makedirs(paths.replace("without_bbox", "with_bbox"))
                # copy_tree(os.path.join(paths, filelist_json[0]), os.path.join(paths.replace("without_bbox", "with_bbox"), filelist_json[0]))
                shutil.copy2(os.path.join(paths, filelist_json[0]), os.path.join(paths.replace("without_bbox", "with_bbox"), filelist_json[0]))

                with open(os.path.join(paths, filelist_json[0]), 'r', encoding="utf-8") as json_file:
                    data = json.load(json_file)

                if 'images' in data:
                    images = data['images']

                    # "images" 속성 반복
                    for image_info in images:
                        image_id = image_info.get('id')
                        file_name = image_info.get('file_name')

                        if image_id is not None and file_name is not None:
                            # with_bbox에 이미지 복사
                            shutil.copy2(os.path.join(paths, file_name), os.path.join(paths.replace("without_bbox", "with_bbox"), file_name))

                            # 이미지 파일 경로 생성
                            image_path = os.path.join(paths.replace("without_bbox", "with_bbox"), file_name)

                            # 이미지 파일이 존재하는 경우
                            if os.path.exists(image_path):
                                image = Image.open(image_path)
                                draw = ImageDraw.Draw(image)

                                # 해당 이미지의 bbox 정보 찾기
                                for annotation in data.get('annotations', []):
                                    if annotation.get('image_id') == image_id:
                                        bbox = annotation.get('bbox')
                                        if bbox:
                                            x, y, width, height = bbox
                                            draw.rectangle(xy=[(x, y), (x + width, y + height)], outline='green', width=1)
                                            # rectangle_image = cv2.rectangle(image, (x, y + height), (x + width, y), (0,255,0), thickness=2) # 좌상 우하 좌표로 그림
                                            image.save(image_path)
                                            print(file_name)

if __name__ == '__main__':
    main()