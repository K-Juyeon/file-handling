import os
import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import csv
import pandas as pd
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image
from skimage import io, img_as_ubyte

data_path = "Z:\\cropimages_1011"
# data_path = "Z:\\cropimages_split_0921"
# data_path = "C:\\Users\\User\\Downloads\\cropped_img"

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

def main():
    for paths, dirs, files in os.walk(data_path) :
        # Set image file path
        image_file_names = os.listdir(paths)
        filelist_jpg = [file for file in image_file_names if file.endswith('.jpg')]
        
        # Get parent folder name
        parent_folder_name = paths.split("\\")[-1]

        # Calculate cosine similarity between image files
        results = []
        for i in range(len(filelist_jpg)):
            for j in range(i + 1, len(filelist_jpg)):
                image_path_1 = os.path.join(paths, filelist_jpg[i])
                image_path_2 = os.path.join(paths, filelist_jpg[j])

                cosine_sim = calculate_cosine_similarity(image_path_1, image_path_2)

                if cosine_sim is not None:
                    results.append([filelist_jpg[i], filelist_jpg[j], cosine_sim])
                    print(f"Comparing {filelist_jpg[i]} and {filelist_jpg[j]}... Similarity: {cosine_sim}")

        # Output the results as a CSV file in the parent folder
        output_csv_filename = f"{parent_folder_name}.csv"
        output_csv_path = os.path.join(data_path, output_csv_filename)
        with open(output_csv_path, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Image1", "Image2", "Similarity"])
            for row in results:
                writer.writerow(row)

        dup_file1 = []
        # dt_result = pd.DataFrame(results)
        for result in results :
            if result[2] > 0.950 :
                dup_file1.append(result[0])
        dup_file1 = list(set(dup_file1))

        with open(os.path.join(data_path, "result_vector.csv"), mode="a+", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([parent_folder_name, len(filelist_jpg), len(dup_file1), round(len(dup_file1) / len(filelist_jpg) * 100, 4)])

def calculate_cosine_similarity(image_path_1, image_path_2):
    try:
        # vector
        image_1 = Image.open(image_path_1)
        image_2 = Image.open(image_path_2)

        img1_vector = get_vector(image_1, model)
        img2_vector = get_vector(image_2, model)

        cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        cosine_sim = cos(img1_vector.unsqueeze(0), img2_vector.unsqueeze(0))

        return cosine_sim[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
if __name__ == '__main__':
    main()