from typing import List

class ProcessedImage:
    image_name: str = None
    dir_name: str = None
    vector_list: List[float] = []
    image_size: int = None
    new_file_name: str = None

    def __init__(self, image_name, dir_name, vector_list, image_size):
        self.image_name = image_name
        self.dir_name = dir_name
        self.vector_list = vector_list
        self.image_size = image_size

    def set_new_file_name(self, new_file_name):
        self.new_file_name = new_file_name