## [中文说明](https://github.com/AberSheeran/upload/blob/master/README.md) | English

This is the Image host Web site program built using Sanic.
It stores the picture to the specified git repository.

## How to use

You must has `pipenv` and `git` in your computer. And then use commands

1. `git clone https://github.com/AberSheeran/upload.git`
2. `cd upload`
3. `pipenv sync`

Then, you need to modify the configuration in `main/config`

```python
# This must be the path to the git repository you use to store the picture
# If you're not sure about the absolute path, you just need to be like this.
# But the repository name needs to be changed to your own.
MEDIA_DIR = os.path.join(os.path.dirname(BASE_DIR), "image")

# This is the URL you can access to your git page
MEDIA_URL = "https://image.abersheeran.com/"
```

Finally, execute the command `pipenv run python3 manage.py start`. You can add `-d` for running it in background.
