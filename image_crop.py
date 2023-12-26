import os
import json
from PIL import Image
import argparse

def _get_parser():
    ''' Get arguments parser '''
    parser = argparse.ArgumentParser(description='File Count')
    parser.add_argument('--path', type=str,
                        default='Z:\\data\\auto_labeling_results',
                        help='Count File Path')

    return parser

# 최상위 폴더 경로 설정
# top_folder = 'Z:\\data\\auto_labeling_results'

# # 출력 폴더 경로 설정
# output_root_folder = 'Z:\\cropimages' + opt

def main():
    parser = _get_parser()
    opt = parser.parse_args()

    # top_folder = opt.path
    # output_root_folder = 'Z:\\cropimages_1007'
    if opt.path != "Z:\\data_final\\auto_labeling_results" :
        top_folder = os.path.join('Z:\\data_final\\auto_labeling_results', opt.path)
        output_root_folder = 'Z:\\cropimages_' + opt.path
    else :
        top_folder = opt.path
        output_root_folder = 'Z:\\cropimages'

    # 최상위 폴더 내의 모든 폴더 검색
    for root, dirs, _ in os.walk(top_folder):
        if 'without_bbox' in dirs:
            without_box_folder = os.path.join(root, 'without_bbox')
            output_folder = os.path.join(output_root_folder, os.path.basename(root))

            # "without_box" 폴더 내의 모든 JSON 파일 검색
            for file_name in os.listdir(without_box_folder):
                if file_name.endswith('.json'):
                    json_path = os.path.join(without_box_folder, file_name)

                    # JSON 파일 열기
                    with open(json_path, 'r') as json_file:
                        data = json.load(json_file)

                        # "images" 속성 확인
                        if 'images' in data:
                            images = data['images']

                            # "images" 속성 반복
                            for image_info in images:
                                image_id = image_info.get('id')
                                file_name = image_info.get('file_name')

                                if image_id is not None and file_name is not None:
                                    # 이미지 파일 경로 생성
                                    image_path = os.path.join(without_box_folder, file_name)

                                    # 이미지 파일이 존재하는 경우
                                    if os.path.exists(image_path):
                                        image = Image.open(image_path)

                                        # 해당 이미지의 bbox 정보 찾기
                                        for annotation in data.get('annotations', []):
                                            if annotation.get('image_id') == image_id:
                                                bbox = annotation.get('bbox')
                                                if bbox:
                                                    x, y, width, height = bbox
                                                    cropped_image = image.crop((x, y, x + width, y + height))

                                                    # 크롭된 이미지 저장
                                                    if not os.path.exists(output_folder):
                                                        os.makedirs(output_folder)

                                                    output_file = f'{file_name[0:-4]}_cropped.jpg'
                                                    output_path = os.path.join(output_folder, output_file)
                                                    try :
                                                        cropped_image.save(output_path)
                                                        print(f"크롭된 이미지 저장: {output_path}")
                                                    except :
                                                        print(file_name)
                                                        pass
                                    else:
                                        print(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    print("크롭된 이미지 추출 및 저장 완료.")

if __name__ == '__main__':
    main()