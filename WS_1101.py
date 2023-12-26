import sys
import os
import glob

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from skimage import io, img_as_ubyte
from scipy.spatial.distance import cosine
from skimage import io, img_as_ubyte

import time
from datetime import datetime

script_path = sys.argv[0]
script_name = os.path.basename(script_path)
supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

# Change to the desired folder path.
image_folder_path = r'C:\Users\kymkim\Desktop\SMARTBANK\C_202305161025_f_ya_ts_sl_be_lp_gr_bh_sg_nb_nm_no_sk_C1_1906\cropped_img'

# Excel file path to save the results
output_folder = os.path.dirname(image_folder_path)
current_datetime = time.strftime("%Y%m%d%H%M%S", time.localtime())
output_excel_file = os.path.join(output_folder, f'{os.path.basename(image_folder_path)}_{current_datetime}.xlsx')

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# 시작시간
start_time = time.time()

# List to store results
results = []

# 폴더 내의 모든 파일 목록을 가져옵니다.
all_files = glob.glob(os.path.join(image_folder_path, '*.*'))

image_files = [file for file in all_files if file.lower().endswith(supported_extensions)]

max_width = 0
max_height = 0

# 이미지 파일들의 가로와 세로 사이즈를 비교하여 가장 큰 값을 찾음
for image_file in image_files:
    img = io.imread(image_file)
    height, width = img.shape[:2]
    if width > max_width: max_width = width
    if height > max_height: max_height = height

# 이미지 리사이즈할 크기 설정
resize_size = (max_height, max_width)

# 이미지 쌍을 비교하고 결과를 저장
for i in range(len(image_files)):
    for j in range(i + 1, len(image_files)):  # 이미지를 읽어와서 사이즈 변경
        img1 = io.imread(image_files[i], as_gray=True)  # 이미지 흑백처리
        img2 = io.imread(image_files[j], as_gray=True)
        
        # 이미지 리사이즈할 크기 설정
        # avg_size = [(size1[0] + size2[0]) // 2, (size1[1] + size2[1]) // 2]
        
        # np.resize를 이용하여 이미지 리사이즈 적용
        img1_resize = np.resize(img1, resize_size)
        img2_resize = np.resize(img2, resize_size)
        
        # 이미지를 부호 없는 8비트 정수로 변환
        img1_u8 = img_as_ubyte(img1_resize)
        img2_u8 = img_as_ubyte(img2_resize)
        
        # 1D 배열로 변환
        img1_flat = img1_u8.reshape(-1)
        img2_flat = img2_u8.reshape(-1)
        
        # 부호 없는 8비트 변환 생략, 1D 배열로 변환
        img1_flat_n8 = img1_resize.reshape(-1)
        img2_flat_n8 = img2_resize.reshape(-1)
        
        # 코사인 유사도 계산
        # from sklearn.metrics.pairwise import cosine_similarity
        cos_sim = cosine_similarity([img1_flat], [img2_flat])[0][0]
        # from scipy.spatial.distance import cosine
        cos_sim_scipy = 1 - cosine(img1_flat_n8, img2_flat_n8)    # scipy cosine은 img_as_ubyte 변환 하지 않아야 함
        # from numpy.linalg import norm
        dot_product = np.dot(img1_flat_n8, img2_flat_n8)
        magnitude1 = np.linalg.norm(img1_flat_n8)
        magnitude2 = np.linalg.norm(img2_flat_n8)
        np_dot_cos_sim = dot_product / (magnitude1 * magnitude2)
        
        # 결과 저장
        result = [os.path.basename(all_files[i]), os.path.basename(all_files[j]),
                  cos_sim, cos_sim_scipy, np_dot_cos_sim, resize_size]
        results.append(result)
        
        print(f"{result}")

# 결과를 DataFrame으로 변환
result_df = pd.DataFrame(results, columns=['image1', 'image2', 'cos_sim', 'cos_sim_scipy', 'np_dot_cos_sim', 'resize_size'])

# 코사인 유사도 결과 값에서 소수점 세자리 이후 버림
result_df['cos_sim'] = result_df['cos_sim'].apply(lambda x: int(x * 1000) / 1000)

# 결과 중에서 cos_sim 컬럼의 값이 0.950 초과인 항목으로 필터링
result_df_95 = result_df[result_df['cos_sim'] >= 0.951]

# image1 and image2 에서 각각 중복 데이터 제거
image_list_rm_img1 = result_df_95['image1'].drop_duplicates().tolist()
image_list_rm_img2 = result_df_95['image2'].drop_duplicates().tolist()

# 엑셀파일로 저장
with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
    result_df.to_excel(writer, sheet_name='results', index=False)
    result_df_95.to_excel(writer, sheet_name='cos_sim >= 0.951', index=False)
    
    # image1 and image2 에서 각각 중복 데이터 제거된 파일 목록 저장
    pd.DataFrame({'images': image_list_rm_img1}).to_excel(writer, sheet_name='remove duplicate image1', index=False)
    pd.DataFrame({'images': image_list_rm_img2}).to_excel(writer, sheet_name='remove duplicate image2', index=False)
    
    # cos_sim > 0.959 시트에 image1, image2에서 중복 제거한 파일 수 확인
    count_img1 = len(result_df_95['image1'].unique())
    count_img2 = len(result_df_95['image2'].unique())
    worksheet = writer.sheets['results']
    worksheet.write('H2', count_img1)
    worksheet.write('I2', count_img2)

print(f'Results saved to {output_excel_file}')
print(f'total images : {len(all_files)}')
print(f'duplicated images(from image1) : {count_img1} ({image_list_rm_img1}) ')
print(f'duplicated images(from image2) : {count_img2} ({image_list_rm_img2}) ')

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")

script_path = sys.argv[0]
script_name = os.path.basename(script_path)
current_time = datetime.now()
current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
print(f"Current time: {current_time_str}")
print(f"script file name: {script_name}")
