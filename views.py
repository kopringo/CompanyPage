import os
import json
import uuid
import shutil
from flask import render_template, request, redirect, url_for, send_from_directory, abort, current_app, Blueprint

from auth import requires_auth
from models import get_realizations_data, save_realizations_data_to_cache, get_homepage_text, save_homepage_text
from utils import allowed_file, create_thumbnail, setup_upload_directories, process_photo

# Reguła blokująca dostęp do katalogu config
def block_config_access(path):
    abort(403)  # Forbidden

# Strona główna
def index():
    realizations = get_realizations_data()
    homepage_text = get_homepage_text()
    return render_template('index.tpl', realizations=realizations, homepage_text=homepage_text)

# Szczegóły realizacji
def realization_detail(realization_id):
    realizations = get_realizations_data()
    realization = next((r for r in realizations if r['id'] == realization_id), None)
    if realization:
        # Zamiast renderować szablon, zwróć JSON z danymi realizacji
        return {
            "realization": {
                "id": realization['id'],
                "shortDescription": realization['short_description'],
                "longDescription": realization['long_description'],
                "photos": realization['photos'],
                "mainPhoto": realization['main_photo']
            }
        }
    else:
        abort(404)  # Realization not found

# Panel zarządzania - tekst strony głównej
@requires_auth
def manage_panel():
    if request.method == 'POST':
        text1 = request.form['text1']
        text2 = request.form['text2']
        text3 = request.form['text3']
        save_homepage_text({"text1": text1, "text2": text2, "text3": text3})
        return redirect(url_for('manage_panel'))
    
    homepage_text = get_homepage_text()
    return render_template('manage.html', homepage_text=homepage_text)

# Lista realizacji w panelu zarządzania
@requires_auth
def manage_realizations():
    realizations = get_realizations_data()
    return render_template('manage_realizations.html', realizations=realizations)

# Dodawanie nowej realizacji
@requires_auth
def add_realization():
    if request.method == 'POST':
        short_description = request.form['short_description']
        long_description = request.form['long_description']
        main_photo_filename = request.form.get('main_photo')
        photos = request.files.getlist('photos')
        
        realization_id = str(uuid.uuid4())
        realization_dir = setup_upload_directories(realization_id)
        
        photo_filenames = []
        for photo in photos:
            filename = process_photo(photo, realization_dir)
            if filename:
                photo_filenames.append(filename)
        
        # Określ główne zdjęcie
        if not main_photo_filename and photo_filenames:
            main_photo_filename = photo_filenames[0]
        
        realization_data = {
            'id': realization_id,
            'short_description': short_description,
            'long_description': long_description,
            'photos': photo_filenames,
            'main_photo': main_photo_filename
        }
        
        # Zapisz dane o realizacji
        with open(os.path.join(realization_dir, 'data.json'), 'w', encoding='utf-8') as f:
            json.dump(realization_data, f, ensure_ascii=False, indent=4)
        
        save_realizations_data_to_cache()  # Odśwież cache
        return redirect(url_for('manage_realizations'))
    
    return render_template('add_realization.html')

# Edycja realizacji
@requires_auth
def edit_realization(realization_id):
    realizations = get_realizations_data()
    realization = next((r for r in realizations if r['id'] == realization_id), None)
    if not realization:
        abort(404)
    
    realization_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], realization_id)
    
    if request.method == 'POST':
        realization['short_description'] = request.form['short_description']
        realization['long_description'] = request.form['long_description']
        main_photo_filename = request.form.get('main_photo')
        realization['main_photo'] = main_photo_filename
        
        photos = request.files.getlist('photos')
        for photo in photos:
            filename = process_photo(photo, realization_dir)
            if filename and filename not in realization['photos']:
                realization['photos'].append(filename)
        
        # Zapisz dane o realizacji
        with open(os.path.join(realization_dir, 'data.json'), 'w', encoding='utf-8') as f:
            json.dump(realization, f, ensure_ascii=False, indent=4)
        
        save_realizations_data_to_cache()  # Odśwież cache
        return redirect(url_for('manage_realizations'))
    
    return render_template('edit_realization.html', realization=realization)

# Usuwanie realizacji
@requires_auth
def delete_realization(realization_id):
    realization_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], realization_id)
    if os.path.exists(realization_dir):
        shutil.rmtree(realization_dir)
    save_realizations_data_to_cache()  # Odśwież cache
    return redirect(url_for('manage_realizations'))

# Dostęp do plików miniatur
def realization_thumbnail(realization_id, filename):
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], realization_id, 'miniatury'), filename)

# Dostęp do oryginalnych plików
def realization_original_photo(realization_id, filename):
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], realization_id, 'oryginalne'), filename)

def register_views(app):
    """Rejestruje wszystkie widoki (routes) w aplikacji"""
    
    # Reguła blokująca dostęp do katalogu config
    app.add_url_rule('/config/<path:path>', 'block_config_access', block_config_access)
    
    # Strona główna
    app.add_url_rule('/', 'index', index)
    
    # Szczegóły realizacji
    app.add_url_rule('/realization/<realization_id>', 'realization_detail', realization_detail)
    
    # Panel zarządzania - tekst strony głównej
    app.add_url_rule('/manage', 'manage_panel', manage_panel, methods=['GET', 'POST'])
    
    # Lista realizacji w panelu zarządzania
    app.add_url_rule('/manage/realizations', 'manage_realizations', manage_realizations)
    
    # Dodawanie nowej realizacji
    app.add_url_rule('/manage/realizations/add', 'add_realization', add_realization, methods=['GET', 'POST'])
    
    # Edycja realizacji
    app.add_url_rule('/manage/realizations/edit/<realization_id>', 'edit_realization', edit_realization, methods=['GET', 'POST'])
    
    # Usuwanie realizacji
    app.add_url_rule('/manage/realizations/delete/<realization_id>', 'delete_realization', delete_realization)
    
    # Dostęp do plików miniatur
    app.add_url_rule('/realizacje/<realization_id>/miniatury/<filename>', 'realization_thumbnail', realization_thumbnail)
    
    # Dostęp do oryginalnych plików
    app.add_url_rule('/realizacje/<realization_id>/oryginalne/<filename>', 'realization_original_photo', realization_original_photo)