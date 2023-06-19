import os
from PIL import Image
import numpy as np

def categorize_image(image, original):
    image_gray = image.convert('L')
    original_gray = original.convert('L')

    
    diff = np.abs(np.array(image_gray) - np.array(original_gray))

    
    percent_diff = np.sum(diff > 50) / diff.size

   
    if percent_diff < 0.2:
        return 'Level3'
    elif percent_diff < 0.35:
        return 'Level2'
    
    elif percent_diff < 0.5:
        return 'Level1'
    else:
        return 'Level0'
def process_images(original_folder, mask_folder, output_folder):
    for filename in os.listdir(original_folder):
        if filename.endswith('.jpg'):
           
            original_image_path = os.path.join(original_folder, filename)
            original_img = Image.open(original_image_path)

            
            mask_image_path = os.path.join(mask_folder, filename.rsplit('.', 1)[0] + '.png')
            if not os.path.isfile(mask_image_path):
                continue
            mask_img = Image.open(mask_image_path)

            
            category = categorize_image(mask_img, original_img)

            
            for image_type, image in [("img", original_img), ("mask", mask_img)]:
                save_format = 'PNG' if image_type == 'mask' else 'JPEG'
                #not save level 0
                if category == 'Level0':
                    continue
                save_filename = filename.rsplit('.', 1)[0] + '.' + save_format.lower()
                save_path = os.path.join(output_folder, category, image_type, save_filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                image.save(save_path, format=save_format)


original_folder = "/Users/lijunyi/Downloads/imagedata/P3M-10k/train/blurred_image"
mask_folder = "/Users/lijunyi/Downloads/imagedata/P3M-10k/train/mask"
output_folder = "/Users/lijunyi/Downloads/imagedata/d"

process_images(original_folder, mask_folder, output_folder)
