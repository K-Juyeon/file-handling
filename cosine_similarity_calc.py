from sklearn.metrics.pairwise import cosine_similarity
from skimage import io, img_as_ubyte
from scipy.spatial.distance import cosine

import numpy as np
import os

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.models import MobileNet_V3_Small_Weights
from torch.autograd import Variable
from PIL import Image

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

def calculate_cosine_similarity(image_path_1, image_path_2):
    # vector
    image_1 = Image.open(image_path_1)
    image_2 = Image.open(image_path_2)

    img1_vector = get_vector(image_1, model)
    img2_vector = get_vector(image_2, model)

    cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
    cosine_sim = cos(img1_vector.unsqueeze(0), img2_vector.unsqueeze(0))

    return cosine_sim[0]

def nomis(images) :
    results = []
    for i in range(len(images)):
        for j in range(i + 1, len(images)):
            image_1 = Image.open(images[i])
            image_2 = Image.open(images[j])

            img1_vector = get_vector(image_1, model)
            img2_vector = get_vector(image_2, model)

            cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
            cos_sim = cos(img1_vector.unsqueeze(0), img2_vector.unsqueeze(0))[0]

            result = [os.path.basename(images[i]), os.path.basename(images[j]), cos_sim, 0, 0, 0]
            results.append(result)
    return results

def WS_1018(images) :
    results = []
    for i in range(len(images)):
        for j in range(i + 1, len(images)):  # 이미지를 읽고 크기를 저장
            img1 = io.imread(images[i], as_gray=True)
            img2 = io.imread(images[j], as_gray=True)

            size1 = img1.shape[:2]
            size2 = img2.shape[:2]
            
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
            result = [os.path.basename(images[i]), os.path.basename(images[j]), cos_sim, size1, size2, avg_size]
            results.append(result)

            # print(f"{result}")
    return results

def WS_1026(images) :
    results = []
    for i in range(len(images)):
        for j in range(i + 1, len(images)):
            img1 = Image.open(images[i])
            img2 = Image.open(images[j])

            img1_vector = get_vector(img1, model)
            img2_vector = get_vector(img2, model)

            # cosine similarity 계산
            cos = torch.nn.CosineSimilarity(dim=1, eps=1e-8)
            cos_sim = cos(img1_vector.unsqueeze(0), img2_vector.unsqueeze(0))
            scaled_cos_sim = (cos_sim + 1) / 2          # -1 ~ 1의 값을 백분율계산을 위해 스케일 업
            Cosine_Similarity = scaled_cos_sim.item()   # 계산을 위해 tensor 문구 제거

            # 비교한 이미지와 cosine similarity 값 저장
            result = [os.path.basename(images[i]), os.path.basename(images[j]), Cosine_Similarity, 0, 0, 0]
            results.append(result)

            # print(f'{result}')
    return results

def WS_1030(images) :
    results = []
    for i in range(len(images)):
        for j in range(i + 1, len(images)):            # 이미지를 읽어와서 사이즈 변경
            img1 = io.imread(images[i], as_gray=True)  # 이미지 흑백처리
            img2 = io.imread(images[j], as_gray=True)
            
            size1 = img1.shape[:2]
            size2 = img2.shape[:2]

            # 이미지 리사이즈할 크기 설정
            avg_size = [(size1[0] + size2[0]) // 2, (size1[1] + size2[1]) // 2]

            # np.resize를 이용하여 이미지 리사이즈 적용
            img1_resize = np.resize(img1, (avg_size[1], avg_size[0]))
            img2_resize = np.resize(img2, (avg_size[1], avg_size[0]))

            # 이미지를 부호 없는 8비트 정수로 변환
            img1_u8 = img_as_ubyte(img1_resize)
            img2_u8 = img_as_ubyte(img2_resize)
            
            # 1D 배열로 변환
            img1_flat = img1_u8.reshape(-1)
            img2_flat = img2_u8.reshape(-1)

            # 코사인 유사도 계산
            cos_sim = cosine_similarity([img1_flat], [img2_flat])[0][0]
            #cos_sim_scipy = 1 - cosine(img1_flat, img2_flat)

            # 결과 저장
            result = [os.path.basename(images[i]), os.path.basename(images[j]), cos_sim, size1, size2, avg_size]
            results.append(result)
        
            # print(f"{result}")
    return results

def WS_1101(images) :
    max_width = 0
    max_height = 0
    results = []

    for image_file in images:
        img = io.imread(image_file)
        height, width = img.shape[:2]
        if width > max_width: max_width = width
        if height > max_height: max_height = height

    # 이미지 리사이즈할 크기 설정
    resize_size = (max_height, max_width)

    for i in range(len(images)):
        for j in range(i + 1, len(images)):  # 이미지를 읽어와서 사이즈 변경
            img1 = io.imread(images[i], as_gray=True)  # 이미지 흑백처리
            img2 = io.imread(images[j], as_gray=True)
            
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
            result = [os.path.basename(images[i]), os.path.basename(images[j]), cos_sim, cos_sim_scipy, np_dot_cos_sim, resize_size]
            results.append(result)
            
            # print(f"{result}")
    return results

        