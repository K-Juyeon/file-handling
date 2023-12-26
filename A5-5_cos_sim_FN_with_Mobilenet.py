import os
import torch
import glob
import pandas as pd

import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image

# Load the pretrained model
model = models.mobilenet_v3_small(pretrained=True)
model.eval()


def get_vector(img, model):

    def copy_data(m, i, o):
        my_embedding.copy_(o.data.reshape(o.data.size(1)))

    layer = model._modules.get('avgpool')

    scaler = transforms.Resize((224, 224))
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    to_tensor = transforms.ToTensor()

    t_img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
    my_embedding = torch.zeros(576)

    h = layer.register_forward_hook(copy_data)
    model(t_img)
    h.remove()
    return my_embedding


# 원하는 숫자들을 포함한 folder_list를 설정 (문자열로 변환)
# folder_list = ['0622', '0801', '0802', '0803', '0804', '0808', '0809', '0814', '0816', '0817', '0818', '0825', '0831', '0901', '0904', '0905', '0907', '0908', '0912', '0914']
# folder_list = ['0816', '0817', '0818', '0825', '0831', '0901', '0904', '0905', '0907', '0908', '0912', '0914']
folder_list = ["0612"]
for folder_num in folder_list:
    # 폴더 경로 설정
    top_folder_path = f'../OUTPUT/cropped_images/{folder_num}'  # 폴더 이름을 문자열로 사용

    # 결과를 저장할 폴더 경로 설정
    output_folder = '../OUTPUT/cos_similarity_results'

    # 결과 폴더가 없다면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 하위 폴더 리스트
    subfolders = os.listdir(top_folder_path)

    # 결과를 저장할 리스트
    results = []

    # 이미지 쌍을 비교하고 결과를 저장합니다.
    for subfolder in subfolders:
        folder_path = os.path.join(top_folder_path, subfolder)
        if os.path.isdir(folder_path):
            # 폴더 내의 모든 파일 목록을 가져옵니다.
            all_files = glob.glob(os.path.join(folder_path, '*.jpg'))  # jpg 확장자에 맞게 수정

            if len(all_files) > 1:  # 그룹 내에 2개 이상의 이미지가 있어야 비교 가능
                # 이미지를 읽고 크기를 저장합니다.
                images = []
                sizes = []
                for file in all_files:
                    image = Image.open(file)
                    images.append(image)

                # 이미지 쌍을 비교하고 결과를 저장합니다.
                for i in range(len(images)):
                    img1 = images[i]
                    img1_vector = get_vector(img1, model)

                    for j in range(i + 1, len(images)):
                        img2 = images[j]
                        img2_vector = get_vector(img2, model)

                        cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
                        cos_sim = cos(img1_vector.unsqueeze(0), img2_vector.unsqueeze(0))

                        # 결과를 리스트에 추가
                        result = [os.path.basename(all_files[i]), os.path.basename(all_files[j]), cos_sim, 0, 0, 0]
                        results.append(result)

    # 결과를 DataFrame으로 변환
    result_df = pd.DataFrame(results, columns=['image1', 'image2', 'cos_sim', 'size1', 'size2', 'avg_size'])

    # 결과 중에서 cos_sim 컬럼의 값이 0.95 초과인 것들만 선택합니다.
    result_df_95 = result_df[result_df['cos_sim'] > 0.95]

    # 두 번째 시트에 image1과 image2 컬럼의 데이터 중복 제거해서 리스트로 저장합니다.
    image_list = pd.concat([result_df_95['image1'], result_df_95['image2']]).drop_duplicates().tolist()

    # 엑셀 파일에 저장합니다.
    output_excel_file = os.path.join(output_folder, 'output.xlsx')  # 출력 파일 경로 수정
    with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, sheet_name='Sheet1', index=False)
        result_df_95.to_excel(writer, sheet_name='Sheet2', index=False)
        pd.DataFrame({'images': image_list}).to_excel(writer, sheet_name='Sheet3', index=False)

    print(f'Results for folder {folder_num} saved to {output_excel_file}')
