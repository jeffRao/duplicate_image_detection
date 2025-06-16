import os

from torchvision.datasets.folder import is_image_file

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

    # 按时间顺序处理图片
    # 获取文件列表并按创建时间排序
    image_files = [os.path.join(image_path, f) for f in os.listdir(image_path)]
    image_files.sort(key=lambda x: os.path.getctime(x))
    for image_file in image_files:
        image_file_name = os.path.basename(image_file)
        print(f'processing image: {image_file}')
        if os.path.isfile(image_file):
            if is_image_file(image_file_name):
                vectors = cnn_encoding(image_file, constant.MOBILENET_LARGE_MODEL)
            else:
                # 非图片文件，不计算特征向量
                vectors = []
            size = get_local_image_file_size(image_file)
            image = ProcessedImage(image_file_name, image_path, vectors, size)
            processed_image_list.append(image)
        elif os.path.isdir(image_file):
            processed_image_list.extend(process_image(image_file))

    return processed_image_list
