import os
import sys
import glob
import pandas as pd
import csv

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.models import MobileNet_V3_Small_Weights
from torch.autograd import Variable
from PIL import Image

import time
from datetime import datetime

# 시작 시간 기록
start_time = time.time()  

# pretrained model인 mobilenet_v3_small 로드
model = models.mobilenet_v3_small(pretrained=True, weights=MobileNet_V3_Small_Weights.DEFAULT)
model.eval()

def get_vector(img, model):
    def copy_data(m, i, o):
        my_embedding.copy_(o.data.reshape(o.data.size(1)))

    layer = model._modules.get('avgpool')
	# 이미지 리사이즈 (mobilenet_v3_small에 사용되기 위해 고정된 사이즈 224 X 224로 변환) 
    scaler = transforms.Resize((224, 224))
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 	# 정규화
    to_tensor = transforms.ToTensor()

    t_img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
    my_embedding = torch.zeros(576)

    h = layer.register_forward_hook(copy_data)
    model(t_img)
    h.remove()
    return my_embedding

# image 파일 경로
folder_path = r'Z:\crop_file\cropimages_0911'
if not os.path.exists(os.path.join(folder_path, 'cos_ws_2_scale')):
    os.makedirs(os.path.join(folder_path, 'cos_ws_2_scale'))

# 모든 jpg 형식의 이미지 파일 
folder_list = os.listdir(folder_path)
for folder in folder_list :
    current_datetime = time.strftime('%Y%m%d%H%M%S', time.localtime())
    output_excel_file = os.path.join(folder_path, 'cos_ws_2_scale', f'{folder}_{current_datetime}.xlsx')
    all_files = glob.glob(os.path.join(folder_path, folder, '*.jpg'))

    # 결과 저장 공간 생성
    results = []
    sum = 0

    if len(all_files) > 1:
        # 이미지 파일 리드
        images = [Image.open(file) for file in all_files]

        for i in range(len(images)):
            img1 = images[i]
            img1_vector = get_vector(img1, model)

            for j in range(i + 1, len(images)):
                img2 = images[j]
                img2_vector = get_vector(img2, model)

                # cosine similarity 계산
                cos = torch.nn.CosineSimilarity(dim=1, eps=1e-8)
                cos_sim = cos(img1_vector.unsqueeze(0), img2_vector.unsqueeze(0))
                scaled_cos_sim = (cos_sim + 1) / 2          # -1 ~ 1의 값을 백분율계산을 위해 스케일 업
                Cosine_Similarity = cos_sim.item()   # 계산을 위해 tensor 문구 제거

                # 비교한 이미지와 cosine similarity 값 저장
                result = [os.path.basename(all_files[i]), os.path.basename(all_files[j]), cos_sim, Cosine_Similarity]
                results.append(result)
                print(f'{result}')

        # 결과 저장을 위한 데이터 프레임 생성
        result_df = pd.DataFrame(results, columns=['image1', 'image2', 'cos_sim', 'Cosine_Similarity'])
        result_df['Cosine_Similarity'] = result_df['Cosine_Similarity'].round(3)

        # Cosine_Similarity 값의 소수점 셋째자리 이하 버림
        result_df['Cosine_Similarity'] = result_df['Cosine_Similarity'].apply(lambda x: int(x * 1000) / 1000)

        # 결과 중에서 Cosine_Similarity 컬럼의 값이 0.960 이상인 항목으로 필터링
        result_df_950 = result_df[result_df['Cosine_Similarity'] >= 0.950]

        # 두 번째 시트에 image1과 image2 컬럼의 데이터 중복 제거해서 리스트로 저장
        image_list_rm_img1 = result_df_950['image1'].drop_duplicates().tolist()
        image_list_rm_img2 = result_df_950['image2'].drop_duplicates().tolist()

        # 엑셀 파일로 저장
        with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
            result_df.to_excel(writer, sheet_name='results', index=False)
            result_df_950.to_excel(writer, sheet_name='cos_sim >= 0.95', index=False)

            # 중복 제거
            pd.DataFrame({'images': image_list_rm_img1}).to_excel(writer, sheet_name='remove duplicate image1', index=False)
            pd.DataFrame({'images': image_list_rm_img2}).to_excel(writer, sheet_name='remove duplicate image2', index=False)

            count_img1 = len(result_df_950['image1'].unique())
            count_img2 = len(result_df_950['image2'].unique())
            worksheet = writer.sheets['results']
            worksheet.write('H2', count_img1)
            worksheet.write('I2', count_img2)

        print(f'Results saved to {output_excel_file}')
        print(f'total images : {len(all_files)}')
        print(f'unique image1 : {count_img1}, unique image2 : {count_img2}')
        print(f'duplicated images : {count_img1},  {count_img2}')

        if count_img1 == count_img2 or count_img1 < count_img2 :
                sum += count_img1
        else :
            sum += count_img2

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")

        with open(os.path.join(folder_path, "result_ws2_scale.csv"), mode="a+", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([folder, len(all_files), count_img1, count_img2, round(count_img1 / len(all_files) * 100, 4), round(count_img2 / len(all_files) * 100, 4), sum, round(sum / len(all_files) * 100, 4)])