import os
import shutil
import numpy as np


def split_dataset(images_dir, labels_dir, output_dir, train_size=0.8, val_size=0.1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create directories for training, validation, and test sets
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_dir, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'labels', split), exist_ok=True)

    # List all image files
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.png'))]
    np.random.shuffle(image_files)

    total_images = len(image_files)
    train_end = int(total_images * train_size)
    val_end = int(total_images * (train_size + val_size))

    # Split into training, validation, and test sets
    train_files = image_files[:train_end]
    val_files = image_files[train_end:val_end]
    test_files = image_files[val_end:]

    def copy_files(file_list, set_name):
        for file in file_list:
            # Copy image
            shutil.copy(os.path.join(images_dir, file), os.path.join(output_dir, 'images', set_name, file))
            # Copy label
            label_file = os.path.splitext(file)[0] + '.txt'
            if os.path.exists(os.path.join(labels_dir, label_file)):
                shutil.copy(os.path.join(labels_dir, label_file),
                            os.path.join(output_dir, 'labels', set_name, label_file))

    # Copy files to respective directories
    copy_files(train_files, 'train')
    copy_files(val_files, 'val')
    copy_files(test_files, 'test')

    print(
        f"Dataset split into {len(train_files)} training, {len(val_files)} validation, and {len(test_files)} testing images.")


# Usage
split_dataset(
    '/home/haid/PycharmProjects/datasets/images',  # Path to original images
    '/home/haid/PycharmProjects/datasets/yolo_labels',  # Path to original labels
    '/home/haid/PycharmProjects/datasets/split'  # Path to save split datasets
)
