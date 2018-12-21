# upload

This is the Image host Web site program built using Sanic. 
It stores the picture to the specified git repository (like [AberSheeran/image](https://github.com/AberSheeran/image))

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
Media_DIR = os.path.join(os.path.dirname(BASE_DIR), "image")

# If the path `Media_DIR` does not exist,
# the command `git clone {Media_Rep}` is automatically executed before Sanic starts.
# It will clone your Git repository in the same directory as this project.
Media_Rep = "https://github.com/AberSheeran/image.git"

# This is the URL you can access to your git page
Media_URL = "https://image.abersheeran.com/"
```

Finally, execute the command `pipenv run python3 manage.py start`. You can add `-d` for running it in background.
