import os
from flask import Flask

from config import Config
from views import register_views
from auth import load_passwords
from models import save_realizations_data_to_cache, get_homepage_text

def create_app():
    """Tworzy i konfiguruje aplikację Flask"""
    app = Flask(__name__)
    
    # Konfiguracja aplikacji
    Config.init_app(app)
    
    # Rejestracja widoków (endpoints)
    register_views(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Wczytaj hasła z pliku
    with app.app_context():
        load_passwords()
        
        # Inicjalizuj cache
        print("Inicjalizacja cache realizacji...")
        save_realizations_data_to_cache()
        print("Inicjalizacja cache tekstów strony głównej...")
        get_homepage_text()
    
    print(f"Aplikacja uruchomiona!")
    print(f"Katalog realizacji: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
    print(f"Katalog konfiguracji: {os.path.abspath(app.config['CONFIG_FOLDER'])}")
    
    app.run(debug=app.config.get('DEBUG', True), host='0.0.0.0')