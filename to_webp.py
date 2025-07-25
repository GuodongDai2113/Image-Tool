"""
此脚本为一个简单的图像处理工具，支持将 PNG 和 JPG 图片转换为 WebP 格式，并根据图片尺寸调整大小。
主要功能包括：
- 单文件模式：用户可输入单个图片文件路径，程序将对其进行处理并输出 WebP 格式的图片。
- 文件夹模式：用户可输入文件夹路径，程序将递归处理文件夹内所有图片，并将其转换为 WebP 格式。

使用方法：
1. 运行脚本后，根据提示选择模式（单文件模式或文件夹模式）。
2. 输入对应的文件或文件夹路径。

注意事项：
- 图片尺寸调整规则：
  - 如果宽度或高度大于等于 4000 像素，则将图像缩小至原来的一半。
  - 如果宽度或高度大于等于 2000 像素，则将图像缩小至原来的 80%。
- 本脚本使用了 `PIL` 库来处理图片，`art` 库来生成艺术字。
"""

import os
from PIL import Image
from art import text2art

class Colors:
    """
    提供颜色打印功能的类。
    包含多种颜色的方法，如红色、绿色、黄色等。
    """

    @staticmethod
    def to_red(string:str):
        """将字符串转换为红色显示。"""
        return '\033[31m'+string+'\033[0m'
    @staticmethod
    def to_green(string:str):
        """将字符串转换为绿色显示。"""
        return '\033[32m'+string+'\033[0m'

    @staticmethod
    def to_yellow(string:str):
        """将字符串转换为黄色显示。"""
        return '\033[33m'+string+'\033[0m'
    @staticmethod
    def to_blue(string:str):
        """将字符串转换为蓝色显示。"""
        return '\033[34m'+string+'\033[0m'
    @staticmethod
    def to_magenta(string:str):
        """将字符串转换为洋红显示。"""
        return '\033[35m'+string+'\033[0m'

def to_webp(image_path:str,webp_path,quality):
    """
    将指定路径的图片转换为 WebP 格式。
    
    参数:
    - image_path: 原始图片路径。
    - webp_path: 转换后的 WebP 图片路径。
    - quality: WebP 图片的质量。
    """
    if not os.path.exists(webp_path):
        try:
            img = Image.open(image_path)
        except IOError as e:
            print(Colors.to_red(f'无法读取图片 {image_path}'))
            print(f"错误详情: {e}")
            return
        if img.mode == 'CMYK':
            img = img.convert('RGB')
        width,height = img.size
        # 如果图片是1:1比例，则压缩为800x800
        if width == height:
            img = img.resize((800, 800))
        elif width >= 4000 or height >= 4000:
            img = img.resize((int(width*0.5),int(height*0.5)))
        elif width >= 2000 or height >= 2000:
            img = img.resize((int(width*0.8),int(height*0.8)))
        img.save(webp_path,'webp',quality=quality)
        print(webp_path)

def to_jpg(webp_path: str, jpg_path: str):
    """
    将指定路径的 WebP 图片转换为 JPG 格式。
    
    参数:
    - webp_path: 原始 WebP 图片路径。
    - jpg_path: 转换后的 JPG 图片路径。
    """
    if not os.path.exists(jpg_path):
        try:
            img = Image.open(webp_path)
        except IOError as e:
            print(Colors.to_red(f'无法读取图片 {webp_path}'))
            print(f"错误详情: {e}")
            return
        img.save(jpg_path, 'jpeg')
        print(jpg_path)

def process_files_in_directory(directory, quality=80, convert_to_jpg=False):
    """
    处理指定目录下的所有图片文件，并将其转换为 WebP 格式。
    如果 convert_to_jpg 为 True，则进一步转换为 JPG 格式。
    
    参数:
    - directory: 需要处理的目录路径。
    - quality: WebP 图片的质量，默认为 80。
    - convert_to_jpg: 是否将 WebP 文件转换为 JPG 文件，默认为 False。
    """
    for root, _, files in os.walk(directory):
        for file in files:
            file_path: str = os.path.join(root, file)
            file_path_split = os.path.splitext(file_path)
            if file_path_split[1].lower() in ['.png', '.jpg', 'jpeg']:
                webp_path = file_path_split[0] + '.webp'
                to_webp(file_path, webp_path, quality)
                if convert_to_jpg:
                    jpg_path = file_path_split[0] + '.jpg'
                    to_jpg(webp_path, jpg_path)

def file_mode(convert_to_jpg=False):
    """
    单文件模式处理流程。
    用户输入单个文件路径，程序处理该文件并输出 WebP 图片。
    如果 convert_to_jpg 为 True，则进一步转换为 JPG 文件。
    """
    while True:
        file_path = input("拖入文件或输入路径:")
        file_path = file_path.replace('"', '')
        if os.path.exists(file_path):
            file_path_split = os.path.splitext(file_path)
            if file_path_split[1].lower() in ['.png', '.jpg', '.jpeg','.webp']:
                webp_path = file_path_split[0] + '.webp'
                to_webp(file_path, webp_path, 80)
                if convert_to_jpg:
                    jpg_path = file_path_split[0] + '.jpg'
                    to_jpg(webp_path, jpg_path)
            else:
                print(Colors.to_red('不是图片'))
        else:
            print(Colors.to_red('文件路径错误'))

def dir_mode(convert_to_jpg=False):
    """
    文件夹模式处理流程。
    用户输入文件夹路径，程序处理该文件夹内所有图片文件并输出 WebP 图片。
    如果 convert_to_jpg 为 True，则进一步转换为 JPG 文件。
    """
    while True:
        dir_path = input("拖入文件夹或输入路径:")
        dir_path = dir_path.replace('"', '').replace("'", '')
        if os.path.isdir(dir_path):
            process_files_in_directory(dir_path, convert_to_jpg=convert_to_jpg)
        else:
            print(Colors.to_red('路径错误'))

def print_author_info():
    """使用art模块绘制“JellyDai”艺术字与联系方式"""
    art_text = text2art("Jelly Dai", font='starwars')
    print('\033[32m')
    print('*'*33 + ' 图像压缩工具 ' + '*'*33)
    print(art_text)
    print('Web:https://jellydai.com')
    print('Email:d@jellydai.com')
    print('Github:https://github.com/GuodongDai2113')
    print('*'*33 + ' 图像压缩工具 ' + '*'*33)
    print('\033[0m')
def print_tool_info():
    """打印工具说明"""
    print('*'*34 + ' 规则说明 ' + '*'*34)
    print('\033[0m')
    print('''如果宽度或高度大于等于 \033[34m4000\033[0m 像素，则将图像缩小至原来的一半。
如果宽度或高度大于等于 \033[34m2000\033[0m 像素，则将图像缩小至原来的 80%。
并将图片转化为 \033[34mWebp\033[0m 格式，由谷歌于2010年推出的新一代图片格式。
单文件模式(\033[34m 只针对一个文件\033[0m )
文件夹模式(\033[34m 文件夹下所有图片、包括子文件夹\033[0m )
        
在windows终端中无法使用拖入，可以使用复制(Ctrl+V)图片或文件夹，
然后在终端中Ctrl+V 粘贴图片路径，然后回车即可。
''')
    print('\033[32m'+'**'*39+'\033[0m')

if __name__ == '__main__':
    print_author_info()
    # print_tool_info()
    while True:
        mode = input('单文件模式 -> 1\n文件夹模式 -> 2\n切换w2j模式 -> 3\n请输入序号：')
        if mode == '1':
            file_mode()
        elif mode == '2':
            dir_mode()
        elif mode == '3':
            print('\033[32m')
            print('当前为webp转jpg模式')
            print('\033[0m')
            while True:
                mode_jpg = input('单文件模式 -> 1\n文件夹模式 -> 2\n请输入序号：')
                if mode_jpg == '1':
                    file_mode(True)
                elif mode_jpg == '2':
                    dir_mode(True)
                else:
                    print(Colors.to_red('序号输入错误'))
        else:
            print(Colors.to_red('序号输入错误'))
