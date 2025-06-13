from service.image_process import ProcessedImage
import numpy as np


def cosine_similarity(image1: ProcessedImage, image2: ProcessedImage):
    """
    计算余弦相似度
    :param image1:
    :param image2:
    :return:
    """

    v1 = image1.vector_list
    v2 = image2.vector_list

    # 将列表转换为 NumPy 数组
    vec1 = np.array(v1)
    vec2 = np.array(v2)

    # 计算点积
    dot_product = np.dot(vec1, vec2)

    # 计算模
    magnitude_vec1 = np.linalg.norm(vec1)
    magnitude_vec2 = np.linalg.norm(vec2)

    # 计算余弦相似度
    if magnitude_vec1 == 0 or magnitude_vec2 == 0:
        return 0  # 如果任一向量为零向量，相似度为0
    return float(dot_product) / (float(magnitude_vec1) * float(magnitude_vec2))


