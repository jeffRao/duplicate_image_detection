import os

from common import constant
from feature.img_encoding import cnn_encoding
from service.image_context import ProcessedImage
from util.image_utils import get_local_image_file_size


def process_image(image_path):
    """
    处理图片，将所有图片的特征向量提取出来
    :param image_path: 图片目录
    :return:
    """
    processed_image_list = []

    if not os.path.exists(image_path):
        return []

    for image_file_name in os.listdir(image_path):
        image_file = os.path.join(image_path, image_file_name)
        if os.path.isfile(image_file):
            vectors = cnn_encoding(image_file, constant.MOBILENET_LARGE_MODEL)
            size = get_local_image_file_size(image_file)
            image = ProcessedImage(image_file_name, image_path, vectors, size)
            processed_image_list.append(image)
        elif os.path.isdir(image_file):
            processed_image_list.extend(process_image(image_file))

    return processed_image_list
