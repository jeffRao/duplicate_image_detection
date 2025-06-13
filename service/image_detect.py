import os
from time import time
from typing import List

from service.image_context import ProcessedImage
from util import file_util
from util.calculator_util import cosine_similarity


def detect_image(image_list: List[ProcessedImage], root_dir: str, oper_type: str = 'copy'):

    detected_list = []
    # 根据 oper_type 来判断是使用 file_util.move_file 还是使用 file_util.copy_file，并记录下方法名称，在后续的实际操作中使用
    if oper_type == 'move':
        operate_image_method = file_util.move_file
    else:
        operate_image_method = file_util.copy_file

    processed_dir = os.path.join(root_dir, 'processed')
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    remove_dir = os.path.join(root_dir, 'remove')
    if not os.path.exists(remove_dir):
        os.makedirs(remove_dir)

    index = 1
    for image in image_list:
        for detected_image in detected_list:
            similarity = cosine_similarity(image, detected_image)
            if similarity > 0.95:
                operate_repeat_image(image, detected_image, detected_list, root_dir, operate_image_method)
                break
            elif similarity > 0.6:
                # 图片高度相似，取文件尺寸较大的图片
                operate_similar_image(image, detected_image, detected_list, root_dir, operate_image_method)
                break
        if image.new_file_name is None:
            operate_different_image(image, index, detected_list, root_dir, operate_image_method)
            index += 1


def operate_repeat_image(new_image, processed_image, detected_list, root_dir: str, oper_method):
    """
    图片高度相似，取文件尺寸较大的图片
    :param new_image:
    :param processed_image:
    :param detected_list:
    :param root_dir:
    :param oper_method:
    :return:
    """
    if new_image.image_size > processed_image.image_size:
        detected_list.remove(processed_image)
        detected_list.append(new_image)
        new_image.new_file_name = processed_image.new_file_name
        # 将已经移动到processed中的文件，重新移动到remove中
        file_util.move_file(os.path.join(root_dir, 'processed', processed_image.new_file_name),
                            os.path.join(root_dir, 'remove', processed_image.image_name))
        oper_method(os.path.join(new_image.dir_name, new_image.image_name),
                    os.path.join(root_dir, 'processed', new_image.new_file_name))
    else:
        # 直接将图片移动到remove中
        oper_method(os.path.join(new_image.dir_name, new_image.image_name),
                    os.path.join(root_dir, 'remove', new_image.image_name))


def operate_similar_image(image, detected_image, detected_list, root_dir: str, oper_method):
    # image-0001-20250613230756444.jpg
    detect_new_file_name = detected_image.new_file_name
    detect_name, _ = detect_new_file_name.split('.')
    file_parts = detect_name.split('-')

    similar_ext = image.image_name.split('.')[-1]
    # 获取当前时间戳的字符串，格式如下：20250613230756444
    timestamp = str(int(round(time() * 1000)))
    similar_file_new = f'image-{file_parts[1]}-{timestamp}.{similar_ext}'
    image.new_file_name = similar_file_new
    oper_method(os.path.join(image.dir_name, image.image_name),
                os.path.join(root_dir, 'processed', image.new_file_name))

    detected_list.append(image)


def operate_different_image(image, index: int, detected_list, root_dir: str, oper_method):

    # 将index格式化为字符串，确保数字长度为4位
    index_str = str(index).zfill(4)
    image_ext = image.image_name.split('.')[-1]
    image.new_file_name = f'image-{index_str}.{image_ext}'

    oper_method(os.path.join(image.dir_name, image.image_name), os.path.join(root_dir, 'processed', image.new_file_name))

    detected_list.append(image)
