# Studienfortschritts-Dashboard

Der Prototyp zeigt ECTS-Fortschritt, Notendurchschnitt, Notenziel,
Zeitplanstatus und die vorhandenen Module. Er verwendet nur die
Python-Standardbibliothek.

## Start

1. Python 3.14 installieren.
2. Unter Windows die Datei `dashboard_starten.bat` doppelt anklicken.

Alternativ kann das Programm in diesem Ordner mit `py main.py` gestartet
werden.

## Optional: Tests

Die Tests werden im gleichen Ordner mit folgendem Befehl gestartet:

`py -m unittest discover -s tests -v`

Die angezeigten Studiendaten stehen in `studiengang.json`.
