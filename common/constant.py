import os
from typing import List

collection_name = 'image_search_collection_v1'
collection_name_redis = 'image_search_collection'

video_search_capture_collection = 'video_search_capture_collection'
video_search_abstract_es_index = 'video_search_abstract_index'

# 向量数据点类型。 FLOAT32， FLOAT64
redis_vector_data_type = 'FLOAT32'

CONVNEXT_BASE_MODEL = 'convnext_base'
CONVNEXT_LARGE_MODEL = 'convnext_large'
MOBILENET_SMALL_MODEL = 'mobilenet_small'
MOBILENET_LARGE_MODEL = 'mobilenet_large'
SQUEEZENET_MODEL = 'squeezenet'

CNN_BASE_INDEX = 'image_search_cnn_base'
CNN_LARGE_INDEX = 'image_search_cnn_large'
MOBILE_SMALL_INDEX = 'image_search_mobile_small'
MOBILE_LARGE_INDEX = 'image_search_mobile_large'
SQUEEZENET_INDEX = 'image_search_squeezenet'

VIDEO_SEARCH_TEMP_DIR = r'D:\temp\video_search'


def get_model_path():
    # 获取当前脚本所在的目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # 获取工程根目录
    project_root = os.path.abspath(os.path.join(current_directory, '..'))

    return os.path.join(project_root, 'model')


emb_model_name = 'stella-large'
cn_clip_model_name = 'ViT-H-14'
cn_clip_model_lib = os.path.join(get_model_path(), 'cn_clip')


class VectorNameEnums:
    ocr_vector_name = 'ocr'
    abstract_vector_name = 'abstract'
    tags_vector_name = 'tags'
    type_vector_name = 'type'
    source_vector_name = 'source'
    image_vector_name = 'image'


class ImageSearchInfo:
    # 文件名称
    file_name: str
    # 图片高度
    height: int
    # 图片宽度
    width: int
    # 文档中心专属字段，用于标记图片所属文档的权限
    # 文档库id
    bookId: str = None
    # 文档id
    docId: str = None
    # 文档权限：
    visibility: str = None
    # 文档开放
    open_scope: str = None

    def __init__(self, ocr_content: str, source: str, abstract: str, context: str, img_type: str, img_url: str,
                 tags: List):
        # ocr 内容
        self.ocr_content = ocr_content
        # 图片来源
        self.source = source
        # 图片上下文描述
        self.context = context
        # 图片摘要
        self.abstract = abstract
        # 图片类型
        self.img_type = img_type
        # 图片url
        self.img_url = img_url
        # 图片标签（关键字）
        self.tags = tags


class ImageInfo:
    # 图片高度
    height: int
    # 图片宽度
    width: int
    # 图片类型
    type: str
    # ocr 内容
    ocr_content: str = ''
    # 图片上下文
    desc: str = ''
    # 图片摘要
    abstract: str = ''
    # 图片标签/关键字
    tags: List = []


class VideoContext:
    def __init__(self, url: str, local_path: str, video_type: str, video_name: str, doc_id: str = None):
        # 视频url
        self.url = url
        # 视频本地地址
        self.local_path = local_path
        # 视频类型
        self.video_type = video_type
        # 视频名称
        self.video_name = video_name
        # 视频所在的文档id
        self.doc_id = doc_id


class VideoAbstractDoc:
    def __init__(self, url: str, video_type: str, video_name: str, text_content: str, time_stamp: float,
                 doc_id: str = None):
        # 视频url
        self.url = url
        # 视频类型
        self.video_type = video_type
        # 视频名称
        self.video_name = video_name
        # 视频所在的文档id
        self.doc_id = doc_id
        # 时间戳
        self.time_stamp = time_stamp
        # 文本内容
        self.text_content = text_content


PROPERTIES_MAPPING = {
    video_search_abstract_es_index: {
        "url": {"type": "text"},
        "video_type": {"type": "text"},
        "video_name": {"type": "text"},
        "doc_id": {"type": "text"},
        "time_stamp": {"type": "float"},
        "text_content": {"type": "text"}
    }
}
