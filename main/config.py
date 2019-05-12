import os
# 项目所在目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 图片存放的Page链接
MEDIA_URL = os.environ.get("MEDIA_URL")
# 图片存储位置
MEDIA_DIR = os.environ.get("MEDIA_DIR")
