import os
import json
from datetime import datetime
from flask import current_app

# Cache w pamięci
realizations_cache = {'data': None, 'timestamp': None}
homepage_text_cache = {'data': None, 'timestamp': None}

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
        if os.path.isdir(realization_path):
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

    # Upewnij się, że katalog config istnieje
    config_dir = current_app.config['CONFIG_FOLDER']
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)

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