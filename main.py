import os.path

from service.image_detect import detect_image
from service.image_process import process_image

if __name__ == '__main__':
    image_path = r'F:\壁纸'
    output_path = r'F:\壁纸测试'
    process_type = 'copy' # move or copy, move 图片移动到output_path中，copy图片复制到output_path中

    processed_image_list = process_image(image_path)
    print(f'process image successfully. image count: {len(processed_image_list)}')

    detect_image(processed_image_list, output_path, process_type)
    print(f'process image successfully.')
    successful_dir = os.path.join(output_path, 'processed')
    # 计算successful_dir下的文件数量
    successful_image_count = len([name for name in os.listdir(successful_dir) if os.path.isfile(os.path.join(successful_dir, name))])
    print(f'process image successfully count: {successful_image_count}')
    remove_dir = os.path.join(output_path, 'remove')
    # 计算successful_dir下的文件数量
    remove_image_count = len([name for name in os.listdir(remove_dir) if os.path.isfile(os.path.join(remove_dir, name))])
    print(f'remove image successfully count: {remove_image_count}')