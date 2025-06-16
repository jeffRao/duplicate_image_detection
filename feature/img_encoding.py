import base64
import os
import traceback
from io import BytesIO

import torch
from torchvision import models, transforms
from PIL import Image

import common.constant as constant
from util.image_utils import read_image

# 选择第一个可用的GPU或CPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

preprocess = transforms.Compose([
    # transforms.RandomRotation(10),
    # transforms.GaussianBlur(kernel_size=(5, 5), sigma=(0.1, 3.0)),
    # transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[0.26862954, 0.26130258, 0.27577711])
])
print('load preprocess succeed.')
MODEL_PATH_DICT = {constant.CONVNEXT_BASE_MODEL: 'convnext/convnext_base.pth',
              constant.CONVNEXT_LARGE_MODEL: 'convnext/convnext_large.pth',
              constant.MOBILENET_SMALL_MODEL: 'mobilenet/mobilenet_v3_small.pth',
              constant.MOBILENET_LARGE_MODEL: 'mobilenet/mobilenet_v3_large.pth',
              constant.SQUEEZENET_MODEL: 'squeezenet/squeezenet1_1.pth'}

def get_convnext_base_model():
    weight_file_path = MODEL_PATH_DICT[constant.CONVNEXT_BASE_MODEL]
    weight_file = os.path.join(constant.get_model_path(), weight_file_path)
    if not os.path.exists(weight_file):
        return None
    model = models.convnext_base()
    model.eval()

    # 使用torch.load()加载权重文件
    state_dict = torch.load(weight_file)
    # 将加载的权重赋值给模型
    model.load_state_dict(state_dict)

    print('load convnext base model to {}'.format(device))
    model = model.to(device)

    return model


def get_convnext_large_model():
    weight_file_path = MODEL_PATH_DICT[constant.CONVNEXT_LARGE_MODEL]
    weight_file = os.path.join(constant.get_model_path(), weight_file_path)
    if not os.path.exists(weight_file):
        return None
    model = models.convnext_large()
    model.eval()

    # 使用torch.load()加载权重文件
    state_dict = torch.load(weight_file)
    # 将加载的权重赋值给模型
    model.load_state_dict(state_dict)

    print('load convnext large model to {}'.format(device))
    model = model.to(device)

    return model


def get_mobilenet_v3_small_model():
    weight_file_path = MODEL_PATH_DICT[constant.MOBILENET_SMALL_MODEL]
    weight_file = os.path.join(constant.get_model_path(), weight_file_path)
    if not os.path.exists(weight_file):
        return None
    model = models.mobilenet_v3_small()
    model.eval()

    # 使用torch.load()加载权重文件
    state_dict = torch.load(weight_file)
    # 将加载的权重赋值给模型
    model.load_state_dict(state_dict)

    print('load mobilenet v3 small model to {}'.format(device))
    model = model.to(device)

    return model


def get_mobilenet_v3_large_model():
    weight_file_path = MODEL_PATH_DICT[constant.MOBILENET_LARGE_MODEL]
    weight_file = os.path.join(constant.get_model_path(), weight_file_path)
    if not os.path.exists(weight_file):
        return None
    model = models.mobilenet_v3_large()
    model.eval()

    # 使用torch.load()加载权重文件
    state_dict = torch.load(weight_file)
    # 将加载的权重赋值给模型
    model.load_state_dict(state_dict)

    print('load mobilenet v3 small model to {}'.format(device))
    model = model.to(device)

    return model


def get_squeezenet_model():
    weight_file_path = MODEL_PATH_DICT[constant.SQUEEZENET_MODEL]
    weight_file = os.path.join(constant.get_model_path(), weight_file_path)
    if not os.path.exists(weight_file):
        return None
    model = models.squeezenet1_1()
    model.eval()

    # 使用torch.load()加载权重文件
    state_dict = torch.load(weight_file)
    # 将加载的权重赋值给模型
    model.load_state_dict(state_dict)

    print('load squeezenet model to {}'.format(device))
    model = model.to(device)

    return model


model_pool = {constant.CONVNEXT_BASE_MODEL: get_convnext_base_model(),
              constant.CONVNEXT_LARGE_MODEL: get_convnext_large_model(),
              constant.MOBILENET_SMALL_MODEL: get_mobilenet_v3_small_model(),
              constant.MOBILENET_LARGE_MODEL: get_mobilenet_v3_large_model(),
              constant.SQUEEZENET_MODEL: get_squeezenet_model()}


def cnn_encoding(image_path: str, model_name: str):
    image_info = read_image(image_path)
    # print('image_info[0]:{}'.format(image_info[0]))
    # print('image_info[1]:{}'.format(image_info[1]))

    model = model_pool[model_name]
    model_path = MODEL_PATH_DICT[model_name]

    if model is None:
        print('模型 {} 不存在，请确认是否已下载对应的模型权重文件，以及目录({})是否正确。'.format(model_name, model_path))

    # 解码图片
    if image_info[2] is None:
        return []

    try:
        image_decode = base64.b64decode(image_info[2])
        # 将解码后的图片信息读取到一个BytesIO对象中
        image_io = BytesIO(image_decode)
        # 使用PIL的Image模块打开图片， 并将彩色图像转换为灰度图像
        # img = Image.open(image_io).convert('L').convert('RGB')
        with Image.open(image_io).convert('RGB') as img:
            input_batch = preprocess(img).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(input_batch)
        # extract the feature vector from the model output
        # feature_vector = output[0].detach().numpy()
        feature_vector = output[0].detach()

        return feature_vector.tolist()
    except:
        traceback.print_exc()
        print('encoding image failed. image : {}'.format(image_path))
        return None


# if __name__ == '__main__':
#     image = r"D:\工作资料\15-浩鲸大模型\图片摘要\样例图片\logo-apple.png"
#     img_features = cnn_encoding(image, 'squeezenet')
#     print(img_features)
