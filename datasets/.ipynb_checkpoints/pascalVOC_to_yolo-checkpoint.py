import os
import argparse
import xml.etree.ElementTree as ET


def convert_annotation(voc_path, yolo_path, classes):
    if not os.path.exists(yolo_path):
        os.makedirs(yolo_path)

    for xml_file in os.listdir(voc_path):
        if not xml_file.endswith('.xml'):
            continue

        tree = ET.parse(os.path.join(voc_path, xml_file))
        root = tree.getroot()

        # Get image dimensions
        width = float(root.find('size/width').text)
        height = float(root.find('size/height').text)

        yolo_file = os.path.join(yolo_path, xml_file.replace('.xml', '.txt'))
        with open(yolo_file, 'w') as out_file:
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                if class_name not in classes:
                    continue

                class_id = classes.index(class_name)
                bbox = obj.find('bndbox')
                xmin = float(bbox.find('xmin').text)
                ymin = float(bbox.find('ymin').text)
                xmax = float(bbox.find('xmax').text)
                ymax = float(bbox.find('ymax').text)

                # Convert to YOLO format
                x_center = (xmin + xmax) / 2 / width
                y_center = (ymin + ymax) / 2 / height
                w = (xmax - xmin) / width
                h = (ymax - ymin) / height

                out_file.write(f"{class_id} {x_center} {y_center} {w} {h}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PascalVOC to YOLO format")
    parser.add_argument('voc_path', type=str, help='Path to PascalVOC annotations')
    parser.add_argument('yolo_path', type=str, help='Path to save YOLO annotations')
    parser.add_argument('classes_file', type=str, help='File with class names')

    args = parser.parse_args()

    with open(args.classes_file) as f:
        classes = [line.strip() for line in f]

    convert_annotation(args.voc_path, args.yolo_path, classes)
