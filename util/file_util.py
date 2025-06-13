import shutil


def move_file(src_file, dest_file):
    # 将文件移动到另一个目录上
    shutil.move(src_file, dest_file)


def copy_file(src_file, dest_file):
    # 将文件复制到另一个目录上
    shutil.copy(src_file, dest_file)
