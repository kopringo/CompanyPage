import os
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

def allowed_file(filename):
    """Sprawdza czy plik ma dozwolone rozszerzenie"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def create_thumbnail(image_path, thumbnail_path, size=(150, 150)):
    """Tworzy miniaturkę zdjęcia"""
    try:
        img = Image.open(image_path)
        img.thumbnail(size)
        img.save(thumbnail_path)
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")

def setup_upload_directories(realization_id):
    """Tworzy strukturę katalogów dla nowej realizacji"""
    realization_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], realization_id)
    os.makedirs(realization_dir, exist_ok=True)
    os.makedirs(os.path.join(realization_dir, 'oryginalne'), exist_ok=True)
    os.makedirs(os.path.join(realization_dir, 'miniatury'), exist_ok=True)
    return realization_dir

def process_photo(photo, realization_dir):
    """Przetwarza przesłane zdjęcie - zapisuje oryginał i tworzy miniaturkę"""
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        original_photo_path = os.path.join(realization_dir, 'oryginalne', filename)
        photo.save(original_photo_path)
        thumbnail_path = os.path.join(realization_dir, 'miniatury', filename)
        create_thumbnail(original_photo_path, thumbnail_path)
        return filename
    return None