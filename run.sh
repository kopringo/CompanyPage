#!/bin/bash

# Zatrzymaj i usuń istniejący kontener jeśli istnieje
if [ "$(docker ps -aq -f name=atlant-app)" ]; then
    echo "Zatrzymywanie i usuwanie istniejącego kontenera..."
    docker stop atlant-app
    docker rm atlant-app
fi

# Utwórz katalog realizacje jeśli nie istnieje
REALIZATIONS_DIR="$(pwd)/public_data"
if [ ! -d "$REALIZATIONS_DIR" ]; then
    echo "Tworzenie katalogu realizacje: $REALIZATIONS_DIR"
    mkdir -p "$REALIZATIONS_DIR"
fi

# Utwórz katalog config jeśli nie istnieje
CONFIG_DIR="$(pwd)/config"
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Tworzenie katalogu config: $CONFIG_DIR"
    mkdir -p "$CONFIG_DIR"
fi

# Przenieś plik homepage_text.json do katalogu config jeśli istnieje w starym miejscu
if [ -f "$REALIZATIONS_DIR/homepage_text.json" ] && [ ! -f "$CONFIG_DIR/homepage_text.json" ]; then
    echo "Przenoszenie pliku homepage_text.json z katalogu realizacje do katalogu config..."
    cp "$REALIZATIONS_DIR/homepage_text.json" "$CONFIG_DIR/homepage_text.json"
    # Możemy usunąć stary plik, ale zachowajmy go dla bezpieczeństwa
    # rm "$REALIZATIONS_DIR/homepage_text.json"
fi

# Sprawdź czy plik passwords.txt istnieje w katalogu config
if [ ! -f "$CONFIG_DIR/passwords.txt" ]; then
    echo "Tworzenie domyślnego pliku passwords.txt w katalogu config..."
    echo "SuperSilneHaslo123" > "$CONFIG_DIR/passwords.txt"
    echo "UWAGA: Utworzono plik z domyślnym hasłem. Zalecana jest zmiana hasła!"
fi

# Budowanie obrazu
echo "Budowanie obrazu Docker..."
docker build -t atlant-app .

# Uruchamianie kontenera z montowaniem katalogów realizacje i config
echo "Uruchamianie kontenera..."
docker run -d \
    --name atlant-app \
    -p 5000:5000 \
    -v "$REALIZATIONS_DIR:/app/public_data" \
    -v "$CONFIG_DIR:/app/config" \
    --restart unless-stopped \
    atlant-app

# Wyświetl logi kontenera, aby sprawdzić czy wszystko działa
echo "Wyświetlanie logów kontenera (CTRL+C aby przerwać)..."
sleep 2
docker logs -f atlant-app

echo "Aplikacja uruchomiona na http://localhost:5000"
echo "Panel administracyjny dostępny pod adresem http://localhost:5000/manage"