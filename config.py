import os

class Config:
    """Konfiguracja aplikacji"""
    # Katalogi
    UPLOAD_FOLDER = os.path.abspath('public_data')
    CONFIG_FOLDER = os.path.abspath('config')
    CAROUSEL_FOLDER = os.path.join(UPLOAD_FOLDER, 'carousel')
    
    # Pliki konfiguracyjne
    HOMEPAGE_TEXT_FILE = os.path.join(UPLOAD_FOLDER, 'homepage_text.json')
    WEBSITE_SETTINGS_FILE = os.path.join(UPLOAD_FOLDER, 'website_settings.json')
    PASSWORDS_FILE = os.path.join(CONFIG_FOLDER, 'passwords.txt')
    
    # Ustawienia aplikacji
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    CACHE_TIMEOUT = 60  # Cache timeout in seconds
    DEBUG = True
    
    @classmethod
    def init_app(cls, app):
        """Inicjalizacja aplikacji z tym profilem konfiguracyjnym"""
        app.config.from_object(cls)
        
        # Upewnij się, że katalogi istnieją
        if not os.path.exists(cls.UPLOAD_FOLDER):
            os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        
        if not os.path.exists(cls.CONFIG_FOLDER):
            os.makedirs(cls.CONFIG_FOLDER, exist_ok=True)
            
        if not os.path.exists(cls.CAROUSEL_FOLDER):
            os.makedirs(cls.CAROUSEL_FOLDER, exist_ok=True)
            
        return app