import os
# 项目所在目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 图片存放的Git库
Media_Rep = "https://github.com/AberSheeran/image"
# 图片存放的Page链接
Media_URL = "https://image.abersheeran.com/"
# 图片存储位置
Media_DIR = os.path.join(os.path.dirname(BASE_DIR), "image")
