from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from colorthief import ColorThief
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
bootstrap = Bootstrap5(app)


class UploadImageForm(FlaskForm):
    image = FileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField('Upload')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

colors = []
image_url = None
is_extract = False
@app.route('/', methods=['GET', 'POST'])
def home():
    global image_url, colors, is_extract
    form = UploadImageForm()
    if form.validate_on_submit():
        file = form.image.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(file_path)
                color_thief = ColorThief(f'uploads/{filename}')
                # get the dominant color
                dominant_color = rgb_to_hex(color_thief.get_color(quality=1))
                # build a color palette
                palette = color_thief.get_palette(color_count=6)
                colors = [rgb_to_hex(color) for color in palette]
                image_url = file_path
                print(dominant_color)
                print(colors)
                print(image_url)
                is_extract = True
                return redirect(url_for('home'))

                # flash('Image successfully uploaded and displayed below')
                # flash(f'File saved at: {file_path}')
            except Exception as e:
                flash(f'An error occurred while saving the file: {str(e)}')
                return redirect(url_for('home'))

        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')

    return render_template('front_webpage.html', form=form, colors=colors, image_url=image_url, is_extract = is_extract)


if __name__ == "__main__":
    app.run(debug=True)
