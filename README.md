# upload

中文 | [English](https://github.com/AberSheeran/upload/blob/master/README-En.md)

这是一个使用Sanic构建的图床Web程序。
它会将图片存储在你指定的Git仓库，并且从服务器删除它（以此减轻服务器压力）。

就像 [AberSheeran/image](https://github.com/AberSheeran/image)

## How to use

你的系统里必须已经安装了`pipenv`与`git`，如果没有，请去安装，然后使用以下命令

1. `git clone https://github.com/AberSheeran/upload.git`
2. `cd upload`
3. `pipenv sync`

接下来，你需要修改`main/config`里面的三个配置

```python
# 这必须是你用以存储图片的git仓库的路径
# 如果你没办法确定绝对路径是在哪，你可以像下面这样使用`os.path`来设置为项目同路径下的image文件夹里
# 当然，你需要修改image为你自己的git仓库名称
Media_DIR = os.path.join(os.path.dirname(BASE_DIR), "image")

# 如果 Media_DIR 路径不存在，
# 在Sanic启动时，会自动执行`git clone {Media_Rep}`
# 这会把你指定的Git仓库下载到与你项目同级的目录下
Media_Rep = "https://github.com/AberSheeran/image.git"

# 这是能访问到你的仓库内容的根url
# 例如 `https://abersheeran.com/image/` 或者 `https://image.abersheeran.com`
Media_URL = "https://image.abersheeran.com/"
```

最后，你只要执行`pipenv run python3 manage.py start`就可以启动你的图床网站，可以使用`-d`在后台启动它(在Windows系统上不能后台启动)
