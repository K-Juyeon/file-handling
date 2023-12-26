import os
import argparse

import os
import glob
import pandas as pd
import time
import csv

import time

import cosine_similarity_calc as cs
import cosine_count_attribute as cca

def _get_parser():
    ''' Get arguments parser '''
    parser = argparse.ArgumentParser(description='Cosine Similarity')
    parser.add_argument('--p', type=str,
                        default='',
                        help='Count File Path')
    parser.add_argument('--v', type=str,
                        default='',
                        help='Cosine Similarity Version')

    return parser

def main():
    parser = _get_parser()
    opt = parser.parse_args()

    folder_path = opt.p
    version = opt.v
    date = folder_path.split('_')[-1]

    start_time = time.time()
    results = []
    remove_img = []
    att_results = []

    if not os.path.exists(os.path.join(folder_path, 'WS_1018')):
        os.makedirs(os.path.join(folder_path, 'WS_1018'))
    if not os.path.exists(os.path.join(folder_path, 'WS_1026')):
        os.makedirs(os.path.join(folder_path, 'WS_1026'))
    if not os.path.exists(os.path.join(folder_path, 'WS_1030')):
        os.makedirs(os.path.join(folder_path, 'WS_1030'))
    if not os.path.exists(os.path.join(folder_path, 'WS_1101')):
        os.makedirs(os.path.join(folder_path, 'WS_1101'))
    if not os.path.exists(os.path.join(folder_path, 'WS_nomis')):
        os.makedirs(os.path.join(folder_path, 'WS_nomis'))

    result_file = open(os.path.join(folder_path, "WS_" + version + ".csv"), "w", newline='', encoding="utf-8")
    wr = csv.writer(result_file)

    progress = 0
    folder_list = [folder for folder in os.listdir(folder_path) if folder.startswith('2')]

    for folder in folder_list :
        progress += 1
        sum = 0
        # current_datetime = time.strftime('%Y%m%d%H%M%S', time.localtime())
        output_excel_file = os.path.join(folder_path, 'WS_' + version, f'{folder}.xlsx')
        images = glob.glob(os.path.join(folder_path, folder, '*.jpg'))

        if len(images) > 1:
            if version == "1018" :
                results = cs.WS_1018(images)
            elif version == "1026" :
                results = cs.WS_1026(images)
            elif version == "1030" :
                results = cs.WS_1030(images)
            elif version == "1101" :
                results = cs.WS_1101(images)
            elif version =="nomis" :
                results = cs.nomis(images)

            # 결과를 DataFrame으로 변환
            result_df = pd.DataFrame(results, columns=['image1', 'image2', 'cos_sim', 'size1', 'size2', 'avg_size'])

            # 코사인 유사도 결과 값에서 소수점 세자리 이후 버림
            result_df['cos_sim'] = result_df['cos_sim'].apply(lambda x: int(x * 1000) / 1000)

            # 결과 중에서 cos_sim 컬럼의 값이 0.950 초과인 항목으로 필터링
            result_df_95 = result_df[result_df['cos_sim'] >= 0.950]

            # image1 and image2 에서 각각 중복 데이터 제거
            image_list_rm_img1 = result_df_95['image1'].drop_duplicates().tolist()
            image_list_rm_img2 = result_df_95['image2'].drop_duplicates().tolist()

            # 엑셀파일로 저장
            with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
                result_df.to_excel(writer, sheet_name='results', index=False)
                result_df_95.to_excel(writer, sheet_name='cos_sim >= 0.950', index=False)

                # image1 and image2 에서 각각 중복 데이터 제거된 파일 목록 저장
                pd.DataFrame({'images': image_list_rm_img1}).to_excel(writer, sheet_name='remove duplicate image1', index=False)
                pd.DataFrame({'images': image_list_rm_img2}).to_excel(writer, sheet_name='remove duplicate image2', index=False)

                # cos_sim > 0.959 시트에 image1, image2에서 중복 제거한 파일 수 확인
                count_img1 = len(result_df_95['image1'].unique())
                count_img2 = len(result_df_95['image2'].unique())
                worksheet = writer.sheets['results']
                worksheet.write('H2', count_img1)
                worksheet.write('I2', count_img2)

            print(f"Progress {progress}/{len(folder_list)}")
            print(f'Results saved to {os.path.basename(output_excel_file)}')
            print(f'total images : {len(images)}')
            print(f'duplicated images(from image1) : {count_img1}')
            print(f'duplicated images(from image2) : {count_img2}')


            if count_img1 == count_img2 or count_img1 < count_img2 :
                sum += count_img1
                remove_img += [img.split('\\')[-1] for img in images if img.split('\\')[-1] not in image_list_rm_img1]
            else :
                sum += count_img2
                remove_img += [img.split('\\')[-1] for img in images if img.split('\\')[-1] not in image_list_rm_img2]

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds\n")
            
            wr.writerow([folder, len(images), count_img1, count_img2, round(count_img1 / len(images) * 100, 4), round(count_img2 / len(images) * 100, 4), sum, round(sum / len(images) * 100, 4)])

    att_results = cca.count_attribute(remove_img, date, att_results)
    result_df = pd.DataFrame(att_results, columns=['date', 'man', 'woman', 'infant', 'child', 'teenager', 'senior',
                                               'old_people', 'jumper', 'shirt', 'jacket', 'long_coat', 't_shirt',
                                               'long_sleeve', 'short_sleeve', 'sleeveless', 'top_brown', 'top_red', 'top_orange',
                                               'top_yellow', 'top_green', 'top_beige', 'top_navy', 'top_blue', 'top_purple',
                                               'top_pink', 'top_gray', 'top_white', 'top_black', 'top_check', 'top_stripe',
                                               'top_colorblocking', 'top_printing', 'long_pants', 'short_pants', 'long_skirt', 'short_skirt',
                                               'bottom_brown', 'bottom_red', 'bottom_orange',
                                               'bottom_yellow', 'bottom_green', 'bottom_beige', 'bottom_navy', 'bottom_blue', 'bottom_purple',
                                               'bottom_pink', 'bottom_gray', 'bottom_white', 'bottom_black', 'bottom_pattern',
                                               'short_hair', 'bobbed_hair', 'long_hair', 'ponytail', 'blad', 'hat', 'halmet',
                                               'glass', 'sunglass', 'no_glass', 'long_strap_bag', 'short_strap_bag', 'backpack',
                                               'carrier', 'no_bag', 'mask', 'no_mask', 'crutches', 'wheelchair',
                                               'cane', 'wf', 'no_wf', 'boots', 'loafers', 'sneakers',
                                               'slipper', 'no_shoes'])
    
    with pd.ExcelWriter(f".\\count_attribute_excel_{date}.xlsx", engine='xlsxwriter') as writer:
        result_df.to_excel(writer, sheet_name='results', index=False)

if __name__ == '__main__':
    main()