# Niezbędnik Studenta
**PPY-studentEssentials** to aplikacja interfejsem graficznym oparta na Pythonie, umożliwiająca zarządzanie informacjami studenckimi — ocenami, planem zajęć, statystykami i kontami użytkowników. Wykorzystuje bibliotekę Gradio jako GUI oraz SQLite jako lokalną bazę danych.

## 📁 Struktura projektu
```grapgql
PPY-studentEssentials/
│
├── core/               # Logika aplikacji
│   ├── __init__.py     # Inicjalizacja bazy danych
│   ├── auth.py         # Rejestracja, logowanie, zmiana hasła
│   ├── database.py     # Połączenie z bazą danych
│   ├── export.py       # Eksport danych do CSV
│   ├── grades.py       # Obsługa ocen
│   ├── hasher.py       # Hashowanie haseł
│   ├── schedule.py     # Obsługa planu zajęć
│   └── team.py         # Obsługa zespołów
│
├── csv/                # Eksportowane pliki CSV
│   └── export1234.csv
│
├── db/                 # Baza danych i inicjalizator
│   ├── database.db     # SQLite DB
│   └── init_db.py      # Tworzenie struktury tabel
│
├── gui/                # Interfejs graficzny
│   ├── backend.py      # Backend GUI z funkcjami logiki
│   └── gui_interface.py# Start aplikacji z Gradio UI
│
└── README.md           # Ten plik
```

## ✅ Funkcje
- 🔏 Panel logowania:
  - Logowanie do konta administratora
  - Logowanie do konta studenta
 
- 👨‍🎓 Panel Studenta:
  - Logowanie (z hashowaniem SHA-256)
  - Przegląd ocen i eksport do CSV
  - Przegląd planu zajęć i eksport
  - Statystyki ocen z podziałem na semestry
  - Zmiana 

- 🛠️ Panel Administratora:
  - Tworzenie kont studentów
  - Dodawanie przedmiotów, zespołów
  - Przypisywanie studentów do zespołów
  - Dodawanie ocen
  - Tworzenie planów zajęć

## 🚀 Uruchomienie aplikacji
1. Zainstaluj wymagane biblioteki (jeśli nie masz):
```bash
pip install gradio
```
2. Uruchom interfejs aplikacji:
```bash
python gui/gui_interface.py
 ```
## 🗝️ Domyślne dane logowania
- Administrator
  - Login: admin
  - Hasło: admin
    
- Studenci Dodawani są ręcznie z poziomu panelu administratora.

## 🛡️ Bezpieczeństwo
- Hasła studentów przechowywane są jako skróty SHA-256.
- System sprawdza poprawność danych wejściowych (np. długość hasła, unikalność loginu).

## 💾 Baza danych
Baza SQLite znajduje się w folderze db/. Struktura tabel tworzona jest automatycznie przy starcie aplikacji (core/__init __.py wywołuje init_db()).

## 📤 Eksport
Oceny, plany i statystyki można eksportować do plików .csv, które zapisywane są w folderze csv/.
