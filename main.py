import os.path
import argparse
from service.image_detect import detect_image
from service.image_process import process_image


def main_process(input_path, output_path, oper_type):
    processed_image_list = process_image(input_path)
    print(f'process image successfully. image count: {len(processed_image_list)}')

    detect_image(processed_image_list, output_path, oper_type)
    print(f'process image successfully.')
    successful_dir = os.path.join(output_path, 'processed')
    # 计算successful_dir下的文件数量
    successful_image_count = len(
        [name for name in os.listdir(successful_dir) if os.path.isfile(os.path.join(successful_dir, name))])
    print(f'process image successfully count: {successful_image_count}')
    remove_dir = os.path.join(output_path, 'remove')
    # 计算successful_dir下的文件数量
    remove_image_count = len(
        [name for name in os.listdir(remove_dir) if os.path.isfile(os.path.join(remove_dir, name))])
    print(f'remove image successfully count: {remove_image_count}')


if __name__ == '__main__':

    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="Process some integers.")

    # 添加 --work_path 参数
    parser.add_argument('--input_dir', type=str, required=True, default=r'F:\照片备份', help='Specify the input dir')
    parser.add_argument('--output_dir', type=str, required=True, default=r'F:\照片整理\2024', help='Specify the output dir')
    parser.add_argument('--process_type', type=str, default='copy', help='Specify the process type')

    # 解析命令行参数
    args = parser.parse_args()
    input_dir = r'F:\照片备份'
    output_dir = r'F:\照片整理\2024'
    process_type = 'copy' # move or copy, move 图片移动到 output_dir 中，copy图片复制到 output_dir 中

    main_process(input_dir, output_dir, process_type)
