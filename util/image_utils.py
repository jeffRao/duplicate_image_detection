from collections import Counter
from PIL import Image
import numpy as np
import requests
import os
import traceback
import json
from io import BytesIO
import base64
from base64 import b64encode


# 计算图片中的颜色个数
def count_colors(image_path, threshold=0.75):
    # 打开并加载图像
    with Image.open(image_path).convert('RGB') as img_file:
        width, height = img_file.size
        # 长或宽大于500，则压缩图片至500像素
        if max(width, height) > 100:
            ratio = 100 / max(width, height)
            width = int(width * ratio)
            height = int(height * ratio)
        threshold_count = width * height * threshold
        img_file = img_file.resize((width, height), Image.LANCZOS)
        # 将图像数据reshape成二维数组，以获取颜色种类数量
        data = np.array(img_file)

    counts = Counter()
    for row in data:
        for item in row:
            # 为了不至于颜色统计太细，将色号泛化到十位数上
            color_key = ','.join(str(x - (x % 20)) for x in item)
            counts[color_key] += 1

    colors_count = 0
    # 对颜色进行降序排列
    sorted_counter = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    # 颜色像素总数达到阈值时的颜色个数
    point_count = 0
    for (key, value) in sorted_counter:
        colors_count += 1
        point_count += value
        if point_count > threshold_count:
            break
    return colors_count


# 获取本地图片的尺寸
def get_local_image_size(image_path):
    with Image.open(image_path) as image:
        width, height = image.size
    if max(width, height) > 1000:
        ratio = 1000 / max(width, height)
        width = int(width * ratio)
        height = int(height * ratio)
    return width, height


# 获取在线图片的尺寸
def get_online_image_size(image_url):
    response = requests.get(image_url)
    with Image.open(response.content) as image:
        width, height = image.size
    return width, height


# 获取本地图片的尺寸
def get_local_image_file_size(image_path):
    """
    :param image_path: 图片文件路径
    :return: 文件大小（单位：字节）
    """
    return os.path.getsize(image_path)


def compress_image(_img, _width, _height):
    """
    :param _img: 图片文件
    :param _width: 压缩后的宽度
    :param _height: 压缩后的高度
    :return:
    """

    # 压缩图片
    return _img.resize((_width, _height), Image.LANCZOS)


def read_image(_image):
    """
    :param _image:
    :return: 图片名称，图片后缀，图片base64编码，宽度，高度
    """
    _image = _image.strip()
    image = None
    try:
        if _image.startswith('http'):
            response = requests.get(_image)
            # 获取文件名
            file_name = os.path.basename(_image)
            # 获取文件后缀名
            file_extension = os.path.splitext(file_name)[1][1:]
            # print('图片名称：{}'.format(file_name))
            if response.status_code == 200:
                image_io = BytesIO(response.content)
                image_base64 = b64encode(image_io.read()).decode()
                # 使用PIL的Image模块打开图片
                image = Image.open(image_io)
                width, height = image.size
            else:
                raise ValueError('get image content from url failed. url :　{}'.format(_image))
        elif os.path.isabs(_image) and os.path.exists(_image):
            # 本地图片
            image = Image.open(_image)
            width, height = image.size

            # 获取文件名称
            file_name = os.path.basename(_image)
            # 获取文件扩展名
            file_extension = os.path.splitext(file_name)[1][1:]

            # 打开图片
            img = open(_image, 'rb').read()
            # base64编码
            image_base64 = base64.b64encode(img).decode('utf8')
            # image_base64 = b64encode(image.tobytes()).decode('utf-8')
        else:
            image_base64 = _image
            image_decode = base64.b64decode(_image)

            # 将解码后的图片信息读取到一个BytesIO对象中
            image_io = BytesIO(image_decode)

            # 使用PIL的Image模块打开图片
            image = Image.open(image_io)

            width, height = image.size

            # 获取图片的名称和类型
            file_name = ''
            file_extension = image.format.lower()

        return file_name, file_extension, image_base64, width, height
    except:
        print('read image info failed. ')
        traceback.print_exc()
        return None, None, None, None, None
    finally:
        if image:
            image.close()

