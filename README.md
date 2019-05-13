## 中文说明 | [English](https://github.com/AberSheeran/upload/blob/master/README-En.md)

这是一个使用Sanic构建的图床Web程序。
它会将图片存储在你指定的Git仓库，并且从服务器删除它（以此减轻服务器压力）。例如 [AberSheeran/image](https://github.com/AberSheeran/image)

## 使用简介

### 原始方法

你的系统里必须已经安装了`pipenv`与`git`，如果没有，请去安装，然后使用以下命令

1. `git clone https://github.com/AberSheeran/upload.git`
2. `cd upload`
3. `pipenv sync`

接下来，你需要修改`main/config`里面的三个配置

```python
# 这必须是你用以存储图片的git仓库的路径
MEDIA_DIR = os.path.join(os.path.dirname(BASE_DIR), "image")

# 这是能访问到你的仓库内容的根url
# 例如 `https://image.abersheeran.com`
MEDIA_URL = "https://image.abersheeran.com/"
```

最后，你只要执行`pipenv run python3 manage.py start`就可以启动你的图床网站，可以使用`-d`在后台启动它(在Windows系统上不能后台启动)

### Docker

如果你拥有docker，那么事情就很简单了。修改`Dockerfile`中的`MEDIA_URL`为自己的url，然后执行如下命令

```bash
docker build -t upload .
docker run -v  ~/Documents/Github/image:/app/image -p 5000:80 -d upload
```

注意要把`~/Documents/Github/image`换成你自己的image仓库路径。
