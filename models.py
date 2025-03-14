import os
import json
import shutil
from datetime import datetime
from flask import current_app

# Cache w pamięci
realizations_cache = {'data': None, 'timestamp': None}
homepage_text_cache = {'data': None, 'timestamp': None}
website_settings_cache = {'data': None, 'timestamp': None}
carousel_images_cache = {'data': None, 'timestamp': None}

def get_realizations_data():
    """Pobiera dane o realizacjach z plików lub cache'u"""
    now = datetime.now().timestamp()
    cache_timeout = current_app.config.get('CACHE_TIMEOUT', 60)
    
    if realizations_cache['data'] and realizations_cache['timestamp'] and (now - realizations_cache['timestamp'] < cache_timeout):
        return realizations_cache['data']

    realizations = []
    realizations_dir = current_app.config['UPLOAD_FOLDER']
    
    # Sprawdź czy katalog realizacje istnieje
    if not os.path.exists(realizations_dir):
        os.makedirs(realizations_dir, exist_ok=True)
        return realizations
    
    # Debug - wypisuje zawartość katalogu realizacje
    print(f"Katalog realizacje zawiera: {os.listdir(realizations_dir)}")
    
    for realization_id in os.listdir(realizations_dir):
        realization_path = os.path.join(realizations_dir, realization_id)
        # Pomijamy katalog carousel i pliki konfiguracyjne
        if os.path.isdir(realization_path) and realization_id != 'carousel':
            data_file = os.path.join(realization_path, 'data.json')
            if os.path.exists(data_file):
                try:
                    with open(data_file, 'r', encoding='utf-8') as f:
                        realization_data = json.load(f)
                        # Debug - wypisuje zawartość pliku data.json
                        print(f"Wczytano dane realizacji: {realization_data}")
                        realizations.append(realization_data)
                except Exception as e:
                    print(f"Błąd podczas wczytywania pliku {data_file}: {e}")

    # Debug - wypisuje liczbę wczytanych realizacji
    print(f"Liczba wczytanych realizacji: {len(realizations)}")
    
    realizations_cache['data'] = realizations
    realizations_cache['timestamp'] = now
    return realizations

def save_realizations_data_to_cache():
    """Wymusza odświeżenie cache'u realizacji"""
    # Wyczyść cache, aby wymusić odczyt z dysku
    realizations_cache['data'] = None
    realizations_cache['timestamp'] = None
    # Teraz pobierz dane z dysku
    realizations_cache['data'] = get_realizations_data()
    realizations_cache['timestamp'] = datetime.now().timestamp()
    print(f"Cache realizacji zaktualizowany. Liczba realizacji: {len(realizations_cache['data'])}")

def get_homepage_text():
    """Pobiera tekst strony głównej z pliku lub cache'u"""
    now = datetime.now().timestamp()
    cache_timeout = current_app.config.get('CACHE_TIMEOUT', 60)
    
    if homepage_text_cache['data'] and homepage_text_cache['timestamp'] and (now - homepage_text_cache['timestamp'] < cache_timeout):
        return homepage_text_cache['data']

    try:
        with open(current_app.config['HOMEPAGE_TEXT_FILE'], 'r', encoding='utf-8') as f:
            homepage_text_data = json.load(f)
    except FileNotFoundError:
        homepage_text_data = {"text1": "", "text2": "", "text3": ""} # Default empty text
        # Zapisz domyślne dane do pliku
        with open(current_app.config['HOMEPAGE_TEXT_FILE'], 'w', encoding='utf-8') as f:
            json.dump(homepage_text_data, f, ensure_ascii=False, indent=4)
        print(f"Utworzono domyślny plik z tekstami strony głównej: {current_app.config['HOMEPAGE_TEXT_FILE']}")

    homepage_text_cache['data'] = homepage_text_data
    homepage_text_cache['timestamp'] = now
    return homepage_text_data

def save_homepage_text(text_data):
    """Zapisuje tekst strony głównej do pliku i aktualizuje cache"""
    # Upewnij się, że katalog istnieje
    homepage_file = current_app.config['HOMEPAGE_TEXT_FILE']
    homepage_dir = os.path.dirname(homepage_file)
    if not os.path.exists(homepage_dir):
        os.makedirs(homepage_dir, exist_ok=True)
    
    with open(homepage_file, 'w', encoding='utf-8') as f:
        json.dump(text_data, f, ensure_ascii=False, indent=4)
    
    # Zapisujemy dane bezpośrednio do cache - to jest OK, ponieważ właśnie 
    # zapisaliśmy te same dane na dysk
    homepage_text_cache['data'] = text_data
    homepage_text_cache['timestamp'] = datetime.now().timestamp()
    print(f"Cache tekstu strony głównej zaktualizowany.")

def get_website_settings():
    """Pobiera ustawienia strony z pliku lub cache'u"""
    now = datetime.now().timestamp()
    cache_timeout = current_app.config.get('CACHE_TIMEOUT', 60)
    
    if website_settings_cache['data'] and website_settings_cache['timestamp'] and (now - website_settings_cache['timestamp'] < cache_timeout):
        return website_settings_cache['data']

    try:
        with open(current_app.config['WEBSITE_SETTINGS_FILE'], 'r', encoding='utf-8') as f:
            settings_data = json.load(f)
    except FileNotFoundError:
        # Domyślne ustawienia strony
        settings_data = {
            "company_name": "Moja Firma",
            "company_logo": "",
            "main_slogan": "Profesjonalne Realizacje dla Wymagających Klientów",
            "company_description": "Jesteśmy firmą z wieloletnim doświadczeniem, specjalizującą się w realizacji projektów na najwyższym poziomie. Sprawdź nasze portfolio i przekonaj się o jakości naszych usług.",
            "services_title": "Zakres Usług",
            "services_description": "Poznaj szeroki wachlarz usług, które oferujemy naszym klientom",
            "services_list": "Projektowanie architektoniczne\nPrzygotowanie dokumentacji budowlanej\nUzyskiwanie pozwoleń na budowę\nNadzór nad realizacją inwestycji\nKonsultacje i doradztwo\nWizualizacje 3D",
            "portfolio_title": "Nasze Realizacje",
            "portfolio_description": "Wybrane projekty z naszego portfolio, które odzwierciedlają jakość naszej pracy",
            "address": "Aleja Grunwaldzka 2C, 82-300 Elbląg",
            "phone": "+48 501 415 542",
            "email": "kontakt@architekt.elblag.pl",
            "working_hours": "Pn-Pt: 9:00-17:00",
            "nav_home": "Home",
            "nav_contact": "Kontakt",
            "meta_title": "Realizacje",
            "meta_description": "",
            "meta_keywords": "",
            "meta_author": "",
            "meta_robots": "index, follow",
            "meta_canonical": "",
            "og_title": "",
            "og_description": "",
            "og_image": ""
        }
        # Zapisz domyślne dane do pliku
        with open(current_app.config['WEBSITE_SETTINGS_FILE'], 'w', encoding='utf-8') as f:
            json.dump(settings_data, f, ensure_ascii=False, indent=4)
        print(f"Utworzono domyślny plik z ustawieniami strony: {current_app.config['WEBSITE_SETTINGS_FILE']}")

    website_settings_cache['data'] = settings_data
    website_settings_cache['timestamp'] = now
    return settings_data

def save_website_settings(settings_data):
    """Zapisuje ustawienia strony do pliku i aktualizuje cache"""
    with open(current_app.config['WEBSITE_SETTINGS_FILE'], 'w', encoding='utf-8') as f:
        json.dump(settings_data, f, ensure_ascii=False, indent=4)
    
    website_settings_cache['data'] = settings_data
    website_settings_cache['timestamp'] = datetime.now().timestamp()
    print(f"Cache ustawień strony zaktualizowany.")

def get_carousel_images():
    """Pobiera listę zdjęć w karuzeli"""
    now = datetime.now().timestamp()
    cache_timeout = current_app.config.get('CACHE_TIMEOUT', 60)
    
    if carousel_images_cache['data'] and carousel_images_cache['timestamp'] and (now - carousel_images_cache['timestamp'] < cache_timeout):
        return carousel_images_cache['data']

    carousel_dir = current_app.config['CAROUSEL_FOLDER']
    carousel_images = []
    
    if os.path.exists(carousel_dir):
        for filename in os.listdir(carousel_dir):
            file_path = os.path.join(carousel_dir, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(tuple(current_app.config['ALLOWED_EXTENSIONS'])):
                carousel_images.append(filename)
    
    # Jeśli brak obrazków w karuzeli, dodaj domyślne z realizacji
    if not carousel_images:
        setup_default_carousel_images()
        # Pobierz ponownie po utworzeniu domyślnych
        carousel_images = []
        if os.path.exists(carousel_dir):
            for filename in os.listdir(carousel_dir):
                file_path = os.path.join(carousel_dir, filename)
                if os.path.isfile(file_path) and filename.lower().endswith(tuple(current_app.config['ALLOWED_EXTENSIONS'])):
                    carousel_images.append(filename)
    
    carousel_images_cache['data'] = carousel_images
    carousel_images_cache['timestamp'] = now
    return carousel_images

def setup_default_carousel_images():
    """Tworzy domyślne obrazki karuzeli z określonych URL-i Unsplash"""
    import requests
    import uuid
    
    carousel_dir = current_app.config['CAROUSEL_FOLDER']
    if not os.path.exists(carousel_dir):
        os.makedirs(carousel_dir, exist_ok=True)
    
    # Lista domyślnych obrazków z Unsplash
    default_images = [
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab",
        "https://images.unsplash.com/photo-1497366754035-f200968a6e72",
        "https://images.unsplash.com/photo-1497366811353-6870744d04b2",
        "https://images.unsplash.com/photo-1504307651254-35680f356dfd"
    ]
    
    count = 0
    
    # Pobieranie obrazków z Unsplash
    for i, img_url in enumerate(default_images):
        try:
            # Dodaj parametry jakości do URL
            full_url = f"{img_url}?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80"
            
            # Pobierz obrazek
            response = requests.get(full_url, stream=True)
            if response.status_code == 200:
                # Generuj unikalną nazwę pliku
                filename = f"carousel_{i+1}_{uuid.uuid4().hex[:8]}.jpg"
                file_path = os.path.join(carousel_dir, filename)
                
                # Zapisz obrazek
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                
                count += 1
                print(f"Pobrano obrazek {i+1} z Unsplash: {filename}")
            else:
                print(f"Nie udało się pobrać obrazka {i+1} z Unsplash. Status: {response.status_code}")
        except Exception as e:
            print(f"Błąd podczas pobierania obrazka {i+1} z Unsplash: {e}")
    
    if count == 0:
        print("Nie udało się pobrać żadnych obrazków dla karuzeli!")
    else:
        print(f"Utworzono {count} domyślnych zdjęć karuzeli.")
        
def save_carousel_images_to_cache():
    """Wymusza odświeżenie cache'u zdjęć karuzeli"""
    carousel_images_cache['data'] = None
    carousel_images_cache['timestamp'] = None
    carousel_images_cache['data'] = get_carousel_images()
    carousel_images_cache['timestamp'] = datetime.now().timestamp()
    print("Cache zdjęć karuzeli zaktualizowany.")