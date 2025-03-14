import os
import uuid
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

def process_carousel_photo(photo):
    """Przetwarza przesłane zdjęcie do karuzeli"""
    if photo and allowed_file(photo.filename):
        carousel_dir = current_app.config['CAROUSEL_FOLDER']
        if not os.path.exists(carousel_dir):
            os.makedirs(carousel_dir, exist_ok=True)
            
        filename = secure_filename(photo.filename)
        # Dodajemy prefiks, aby uniknąć nadpisywania plików
        unique_filename = f"carousel_{uuid.uuid4().hex[:8]}_{filename}"
        photo_path = os.path.join(carousel_dir, unique_filename)
        photo.save(photo_path)
        return unique_filename
    return None

def delete_carousel_photo(filename):
    """Usuwa zdjęcie z karuzeli"""
    carousel_dir = current_app.config['CAROUSEL_FOLDER']
    file_path = os.path.join(carousel_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def process_company_logo(photo):
    """Przetwarza przesłane logo firmy"""
    if photo and allowed_file(photo.filename):
        upload_dir = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)
            
        filename = secure_filename(photo.filename)
        # Stała nazwa dla logo, aby łatwo identyfikować
        logo_filename = f"company_logo_{uuid.uuid4().hex[:8]}_{filename}"
        logo_path = os.path.join(upload_dir, logo_filename)
        
        # Zapisz oryginał
        photo.save(logo_path)
        
        # Przeskaluj logo do wysokości 60px zachowując proporcje
        try:
            img = Image.open(logo_path)
            width, height = img.size
            new_height = 60
            new_width = int(width * (new_height / height))
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img.save(logo_path)
        except Exception as e:
            print(f"Error resizing logo: {e}")
            
        return logo_filename
    return None