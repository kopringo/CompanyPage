from functools import wraps
from flask import request, current_app

def load_passwords():
    """Wczytuje hasła z pliku passwords.txt"""
    passwords_file = current_app.config['PASSWORDS_FILE']
    
    # Jeśli plik z hasłami nie istnieje, utwórz go z domyślnym hasłem
    if not os.path.exists(passwords_file):
        with open(passwords_file, 'w', encoding='utf-8') as f:
            f.write("SuperSilneHaslo123\n")
            print("Utworzono plik z domyślnym hasłem. ZALECANA JEST ZMIANA HASŁA!")
    
    # Wczytaj hasła z pliku
    with open(passwords_file, 'r', encoding='utf-8') as f:
        passwords = [line.strip() for line in f if line.strip()]
    
    # Zapisz hasła w konfiguracji aplikacji
    current_app.config['PASSWORDS'] = passwords
    print(f"Wczytano {len(passwords)} haseł z pliku {passwords_file}")
    return passwords

def check_auth(username, password):
    """Sprawdza poprawność nazwy użytkownika i hasła"""
    return password in current_app.config.get('PASSWORDS', [])

def authenticate():
    """Wysyła odpowiedź 401 i włącza uwierzytelnianie"""
    return ('', 401, {'WWW-Authenticate': 'Basic realm="Panel Zarzadzania Realizacjami"'})

def requires_auth(view_function):
    """Dekorator wymuszający uwierzytelnianie"""
    @wraps(view_function)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return view_function(*args, **kwargs)
    return decorated

# Importy na końcu, aby uniknąć cyklicznych zależności
import os