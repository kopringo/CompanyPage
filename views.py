import os
import json
import uuid
import shutil
from flask import render_template, request, redirect, url_for, send_from_directory, abort, current_app, Blueprint

from auth import requires_auth
from models import (get_realizations_data, save_realizations_data_to_cache, 
                   get_homepage_text, save_homepage_text, 
                   get_website_settings, save_website_settings,
                   get_carousel_images, save_carousel_images_to_cache)
from utils import (allowed_file, create_thumbnail, setup_upload_directories, 
                 process_photo, process_carousel_photo, delete_carousel_photo,
                 process_company_logo)

# Reguła blokująca dostęp do katalogu config
def block_config_access(path):
    abort(403)  # Forbidden

# Strona główna
def index():
    realizations = get_realizations_data()
    homepage_text = get_homepage_text()
    website_settings = get_website_settings()
    carousel_images = get_carousel_images()
    return render_template('index.tpl', 
                          realizations=realizations, 
                          homepage_text=homepage_text,
                          settings=website_settings,
                          carousel_images=carousel_images)

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
        if 'section' in request.form:
            section = request.form['section']
            
            # Obsługa tekstów strony głównej
            if section == 'homepage_text':
                text1 = request.form['text1']
                text2 = request.form['text2']
                text3 = request.form['text3']
                save_homepage_text({"text1": text1, "text2": text2, "text3": text3})
                return redirect(url_for('manage_panel', tab='content-settings'))
            
            # Obsługa ogólnych ustawień strony
            elif section == 'general_settings':
                # Pobierz aktualne ustawienia, aby zachować wszystkie pola
                current_settings = get_website_settings()
                
                # Sprawdź czy przesłano nowe logo
                company_logo = current_settings.get('company_logo', '')
                if 'company_logo' in request.files and request.files['company_logo'].filename:
                    logo_file = request.files['company_logo']
                    processed_logo = process_company_logo(logo_file)
                    if processed_logo:
                        company_logo = processed_logo
                
                # Przygotuj dane do zapisu
                settings = current_settings.copy()
                settings.update({
                    "company_name": request.form['company_name'],
                    "company_logo": company_logo,
                    "main_slogan": request.form['main_slogan'],
                    "company_description": request.form['company_description'],
                    "services_title": request.form['services_title'],
                    "services_description": request.form['services_description'],
                    "services_list": request.form['services_list'],
                    "portfolio_title": request.form['portfolio_title'],
                    "portfolio_description": request.form['portfolio_description'],
                    "address": request.form['address'],
                    "phone": request.form['phone'],
                    "email": request.form['email'],
                    "working_hours": request.form['working_hours'],
                    "nav_home": request.form['nav_home'],
                    "nav_contact": request.form['nav_contact']
                })
                save_website_settings(settings)
                return redirect(url_for('manage_panel', tab='general-settings'))
                
            # Obsługa meta tagów SEO
            elif section == 'meta_settings':
                # Pobierz aktualne ustawienia, aby zachować wszystkie pola
                current_settings = get_website_settings()
                
                # Przygotuj dane do zapisu
                settings = current_settings.copy()
                settings.update({
                    "meta_title": request.form['meta_title'],
                    "meta_description": request.form['meta_description'],
                    "meta_keywords": request.form['meta_keywords'],
                    "meta_author": request.form['meta_author'],
                    "meta_robots": request.form['meta_robots'],
                    "meta_canonical": request.form['meta_canonical'],
                    "og_title": request.form['og_title'],
                    "og_description": request.form['og_description'],
                    "og_image": request.form['og_image']
                })
                save_website_settings(settings)
                return redirect(url_for('manage_panel', tab='meta-settings'))
        
        return redirect(url_for('manage_panel'))
    
    # Get active tab from query parameters or default to general settings
    tab = request.args.get('tab', 'general-settings')
    
    homepage_text = get_homepage_text()
    website_settings = get_website_settings()
    return render_template('manage.html', homepage_text=homepage_text, settings=website_settings, active_tab=tab)

# Panel zarządzania - karuzela
@requires_auth
def manage_carousel():
    website_settings = get_website_settings()
    
    if request.method == 'POST':
        # Obsługa dodawania nowych zdjęć do karuzeli
        if 'action' in request.form and request.form['action'] == 'add':
            photos = request.files.getlist('photos')
            for photo in photos:
                process_carousel_photo(photo)
            save_carousel_images_to_cache()  # Odśwież cache
            
        # Obsługa usuwania zdjęć z karuzeli
        elif 'action' in request.form and request.form['action'] == 'delete':
            if 'filename' in request.form:
                delete_carousel_photo(request.form['filename'])
                save_carousel_images_to_cache()  # Odśwież cache
                
        return redirect(url_for('manage_carousel'))
    
    carousel_images = get_carousel_images()
    return render_template('manage_carousel.html', carousel_images=carousel_images, settings=website_settings)

# Lista realizacji w panelu zarządzania
@requires_auth
def manage_realizations():
    realizations = get_realizations_data()
    website_settings = get_website_settings()
    return render_template('manage_realizations.html', realizations=realizations, settings=website_settings)

# Dodawanie nowej realizacji
@requires_auth
def add_realization():
    website_settings = get_website_settings()
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
    
    return render_template('add_realization.html', settings=website_settings)

# Edycja realizacji
@requires_auth
def edit_realization(realization_id):
    realizations = get_realizations_data()
    website_settings = get_website_settings()
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
    
    return render_template('edit_realization.html', realization=realization, settings=website_settings)

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

# Dostęp do zdjęć karuzeli
def carousel_photo(filename):
    return send_from_directory(current_app.config['CAROUSEL_FOLDER'], filename)

# Dostęp do plików w katalogu public_data (dla logo itp.)
def public_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

def register_views(app):
    """Rejestruje wszystkie widoki (routes) w aplikacji"""
    
    # Reguła blokująca dostęp do katalogu config
    app.add_url_rule('/config/<path:path>', 'block_config_access', block_config_access)
    
    # Strona główna
    app.add_url_rule('/', 'index', index)
    
    # Szczegóły realizacji
    app.add_url_rule('/realization/<realization_id>', 'realization_detail', realization_detail)
    
    # Panel zarządzania - tekst strony głównej i ustawienia
    app.add_url_rule('/manage', 'manage_panel', manage_panel, methods=['GET', 'POST'])
    
    # Panel zarządzania - karuzela
    app.add_url_rule('/manage/carousel', 'manage_carousel', manage_carousel, methods=['GET', 'POST'])
    
    # Lista realizacji w panelu zarządzania
    app.add_url_rule('/manage/realizations', 'manage_realizations', manage_realizations)
    
    # Dodawanie nowej realizacji
    app.add_url_rule('/manage/realizations/add', 'add_realization', add_realization, methods=['GET', 'POST'])
    
    # Edycja realizacji
    app.add_url_rule('/manage/realizations/edit/<realization_id>', 'edit_realization', edit_realization, methods=['GET', 'POST'])
    
    # Usuwanie realizacji
    app.add_url_rule('/manage/realizations/delete/<realization_id>', 'delete_realization', delete_realization)
    
    # Dostęp do plików miniatur
    app.add_url_rule('/public_data/<realization_id>/miniatury/<filename>', 'realization_thumbnail', realization_thumbnail)
    
    # Dostęp do oryginalnych plików
    app.add_url_rule('/public_data/<realization_id>/oryginalne/<filename>', 'realization_original_photo', realization_original_photo)
    
    # Dostęp do zdjęć karuzeli
    app.add_url_rule('/public_data/carousel/<filename>', 'carousel_photo', carousel_photo)
    
    # Dostęp do plików w katalogu public_data
    app.add_url_rule('/public_data/<filename>', 'public_file', public_file)