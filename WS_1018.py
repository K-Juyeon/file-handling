import os
import glob
import cv2
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from skimage import io, img_as_ubyte
import time
import csv

# 원하는 폴더 경로로 변경하세요.
folder_path = r'Z:\crop_file\cropimages_0921'

# 시작시간
start_time = time.time()

# 폴더 내의 모든 파일 목록을 가져옵니다.
folder_list = os.listdir(folder_path)
if not os.path.exists(os.path.join(folder_path, 'cos_ws_1')) :
    os.makedirs(os.path.join(folder_path, 'cos_ws_1'))

for folder in folder_list :
    # 결과를 저장할 엑셀 파일 경로
    current_datetime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    output_excel_file = os.path.join(folder_path, 'cos_ws_1', f'{folder}_{current_datetime}.xlsx')
    
    all_files = glob.glob(os.path.join(folder_path, folder, '*.jpg'))

    # 파일들을 이름군으로 그룹화 (폴더내 다른 폴더의 파일이 포함되었을 경우 구분하여 비교함)
    file_groups = {}
    for file in all_files:
        filename = os.path.basename(file)
        name_group = filename.split('_')[0]
        if name_group in file_groups:
            file_groups[name_group].append(file)
        else:
            file_groups[name_group] = [file]

    # 결과를 저장할 리스트
    results = []
    sum = 0

    # 이미지 쌍을 비교하고 결과를 저장
    for name_group, group_files in file_groups.items():
        if len(group_files) > 1:    # 그룹 내에 2개 이상의 이미지가 있어야 비교 가능,
            images = []
            sizes = []
            for file in group_files:
                image = io.imread(file, as_gray=True)  # 이미지 읽어 올때 흑백 처리
                size = image.shape[:2]
                sizes.append(size)
                images.append(image)

            for i in range(len(images)):
                for j in range(i + 1, len(images)):  # 이미지를 읽고 크기를 저장
                    img1 = images[i]
                    img2 = images[j]
                    size1 = sizes[i]
                    size2 = sizes[j]
                    
                    # 이미지 리사이즈할 크기 설정
                    avg_size = [(size1[0] + size2[0]) // 2, (size1[1] + size2[1]) // 2]

                    # np.resize를 이용하여 이미지 리사이즈 적용
                    img1_resize = np.resize(img1, (avg_size[1], avg_size[0]))
                    img2_resize = np.resize(img2, (avg_size[1], avg_size[0]))

                    # 이미지를 부호 없는 8비트 정수로 변환
                    img1_u8 = img_as_ubyte(img1_resize)
                    img2_u8 = img_as_ubyte(img2_resize)

                    # 벡터 값으로 변환
                    img1_flat = img1_u8.reshape(-1)
                    img2_flat = img2_u8.reshape(-1)
                    
                    # 코사인 유사도 계산
                    cos_sim = cosine_similarity([img1_flat], [img2_flat])[0][0]

                    # 결과를 리스트에 추가
                    result = [os.path.basename(group_files[i]), os.path.basename(group_files[j]),
                            cos_sim, size1, size2, avg_size
                            ]
                    results.append(result)

                    print(f"{result}")
                
            # 결과를 DataFrame으로 변환
            result_df = pd.DataFrame(results, columns=['image1', 'image2', 'cos_sim', 'size1', 'size2', 'avg_size'])

            # 코사인 유사도 결과 값에서 소수점 세자리 이후 버림
            result_df['cos_sim'] = result_df['cos_sim'].apply(lambda x: int(x * 1000) / 1000)

            # 결과 중에서 cos_sim 컬럼의 값이 0.950 초과인 항목으로 필터링
            result_df_95 = result_df[result_df['cos_sim'] >= 0.950]

            # image1과 image2 컬럼의 데이터 중복 제거해서 리스트로 저장
            image_list_rm_img1 = result_df_95['image1'].drop_duplicates().tolist()
            image_list_rm_img2 = result_df_95['image2'].drop_duplicates().tolist()

            # 엑셀 파일로 저장
            with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
                result_df.to_excel(writer, sheet_name='results', index=False)
                result_df_95.to_excel(writer, sheet_name='cos_sim >= 0.951', index=False)
                
                # 중복 제거한 이미지 목록 출력
                pd.DataFrame({'images': image_list_rm_img1}).to_excel(writer, sheet_name='remove duplicate image1', index=False)
                pd.DataFrame({'images': image_list_rm_img2}).to_excel(writer, sheet_name='remove duplicate image2', index=False)

                # cos_sim > 0.96 시트에 A, B열 카운트 결과 출력
                count_img1 = len(result_df_95['image1'].unique())
                count_img2 = len(result_df_95['image2'].unique())
                worksheet = writer.sheets['results']
                worksheet.write('G2', count_img1)
                worksheet.write('H2', count_img2)
                
            print(f'Results saved to {output_excel_file}')
            print(f'image count : {len(group_files)}')
            print(f'image1 : {count_img1}, image2 : {count_img2}')

            if count_img1 == count_img2 or count_img1 < count_img2 :
                sum += count_img1
            else :
                sum += count_img2

            # Record the end time
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds")

            with open(os.path.join(folder_path, "result_ws1.csv"), mode="a+", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow([folder, len(images), count_img1, count_img2, round(count_img1 / len(images) * 100, 4), round(count_img2 / len(images) * 100, 4), sum])
