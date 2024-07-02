import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

output_dir = "C:\\Users\\jv777\\OneDrive\\Documentos\\student-research-team\\Palms\\Palms_Augmented"
input_dir = "C:\\Users\\jv777\\OneDrive\\Documentos\\student-research-team\\Palms\\CroppedPalms"
num_samples = 5
image_size = 224

def generate_rand_sample(input_dir, output_dir, num_samples, image_size):
    ## Get file names array from input_dir
    img_list = os.listdir(input_dir)

    itr = 1
    for file_name in img_list:
        ## obtain img from file
        path=os.path.join(input_dir, file_name)
        img = Image.open(path)

        ## generate num_samples of size img_size
        k = image_size
        m, n = img.size

        ## convert pillow into numpy array
        arr_img = np.array(img)
        arr_img = arr_img[:, :, 0:3]

        for i in range(0, num_samples):
            rand_i = np.random.randint(0, m-k + 1)
            rand_j = np.random.randint(0, n-k + 1)

            patch = arr_img[rand_i:k + rand_i, rand_j: k + rand_j, :]

            patch_img = Image.fromarray(patch)
            image_name = f"FCAT2APPK_NonPalm_{itr}.tif"

            if not (os.path.exists(output_dir)):
                os.makedirs(output_dir)

            path=os.path.join(output_dir, image_name)
            patch_img.save(path)

            if itr%100 == 0:
                print(f"{itr} annotations cropped so far, up to {image_name}")
            
            itr = itr + 1

generate_rand_sample(input_dir, output_dir, num_samples, image_size)
print("done")