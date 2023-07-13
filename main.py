from flask import Flask, render_template, request
from pathlib import Path
import blog_utils
import openai_utils

app = Flask(__name__)

### Define your paths here

PATH_TO_BLOG_REPO = Path('/Users/sivadeep/Documents/GitHub/blogpost-generator/.git')
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG / "content"
PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)
###

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/blog', methods=['GET', 'POST'])
def create_blog():
    if request.method == 'POST':
        title = request.form['title']
        print(openai_utils.create_prompt(title))
        blog_content = openai_utils.get_blog_from_openai(title)

        # Get the cover image and create the blog
        _, cover_image_save_path = openai_utils.get_cover_image(title, "cover_image.png")
        path_to_new_content = blog_utils.create_new_blog(PATH_TO_CONTENT, title, blog_content, cover_image_save_path)
        blog_utils.write_to_index(PATH_TO_BLOG, path_to_new_content)

        # Update the blog
        blog_utils.update_blog(PATH_TO_BLOG_REPO)

        # Render a template with the submitted title
        return render_template('result.html', title=title)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
