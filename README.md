# duplicate_image_detection

## 介绍
检测重复图片，识别相似图片，并进行图片分类。

最近在整理照片，由于照片的量太多了，并且有很多类似的照片，我希望能够将这一堆照片中的重复图片清理掉，同时将类似的，或者比较相近的照片放到一起。
比如，在同一个场景，或者穿着同一套衣服的照片，希望能够集中整理。

然而，我的台式机上并没有一张很好的显卡，显然跑不了VL模型，我想大多数人的电脑上，应该都没有能够跑动VL模型的显卡。

好在，我只要简单的做一些图片的相似度检测。

在本项目中，我用到了一些CNN模型，这些模型比较小，可以在常规的CPU上进行推理，效率也很快，我使用的模型是`mobilenet_v3_large`，处理700张10m以上的照片，大概10分钟内完成。

## 使用

本项目没有WEBUI界面，也没有封装的执行文件，只有一些脚本，配合python环境运行。如果你对执行文件编译比较在行，也欢迎将我的代码编译成可执行文件。

本项目是一个业余项目，如果存在bug，或者有一些好的点子，可以给我提issue，有时间的话，会更新。也欢迎共创。

## 快速开始
本项目没有UI，只能配置好环境后，执行python脚本。
1. 安装python环境
自行下载python，我用的是python-3.12。或者使用conda安装虚拟环境。
2. 安装依赖
```shell
git clone https://github.com/jeffRao/duplicate_image_detection
cd duplicate_image_detection
pip install -r requirements.txt
```
3. 执行脚本
直接执行根目录下的`main.py`即可。
有两种方式执行，在开发环境，直接执行。执行时修改输入输出目录即可。
- 直接命令行形式执行
```shell
python main.py --input_dir=/path/to/input/dir --output_dir=/path/to/output/dir  // 默认复制图片到新目录
python main.py --input_dir=/path/to/input/dir --output_dir=/path/to/output/dir --process_mode=move  // 移动图片到新目录
```

- 开发模式执行
如果你是在ide中运行项目，你可以修改`main.py`中的`if __name__ == '__main__':`下的代码，然后直接在ide中运行`main.py`文件。
例如：
```python
if __name__ == '__main__':
    main(input_dir='/path/to/input/dir', output_dir='/path/to/output/dir', process_type='move')
```

## 细节说明
- `process_type`支持移动和复制两种格式，默认是复制。如果想保留原始文件，可以使用复制模式，否则可以使用移动模式。
- 项目执行后，会在`output_dir`目录下生成一个`processed`和`remove`两个文件夹，`processed`文件夹里面是处理后的图片，`remove`文件夹里面是重复的删除的图片。
- 文件读取时，按照图片的创建时间排序的。
- 图片名称是按照一定的规则设置的，相似的图片会放在相近的位置。
- 图片特征提取支持 `convnext`，`mobilenet`，`squeezenet` 共5中模型，工程中提供了`mobilenet_v3_large`和`mobilenet_v3_small`两个权重文件。
  如果需要使用其他模型，请自行下载。
  [ConvNeXt](https://github.com/facebookresearch/ConvNeXt)
  [squeezenet](https://github.com/forresti/SqueezeNet)
- 如果需要修改使用的模型，则调整`image_process`下面的如下代码参数。
  ```python
  # 将第二个参数调整为其他值，具体的，可以参照constant中的变量枚举
  vectors = cnn_encoding(image_file, constant.MOBILENET_LARGE_MODEL)
  ```
- 图片相似度计算使用的是余弦相似度，目前判断重复图片，使用的阈值为0.95，判断相似图片，使用的阈值为0.7。如果你想调整阈值，请查看`image_detect.py`文件中的相关代码。
