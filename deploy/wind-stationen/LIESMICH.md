# Wind am Brauneck – Testseite zum Hochladen

Fertige, statische Testseite. Keine Datenbank, kein PHP, kein Build-Schritt.

## Hochladen
Beide Dateien unverändert in denselben Ordner auf dem Webspace legen (z. B. `/wind-test/`):

- `index.html` – die Seite (enthält die vorberechneten Strömungsfelder, ca. 2,8 MB)
- `karte_tex.jpg` – Geländetextur (muss neben `index.html` liegen, Name nicht ändern)

Danach die Ordner-URL im Browser öffnen. Am PC erscheint die Querformat-Ansicht, auf dem Handy hochkant automatisch die Handy-Ansicht.

## Externe Abrufe (wichtig für Datenschutz)
- three.js r128 von cdnjs.cloudflare.com
- Schriften von fonts.googleapis.com

Für den Testbetrieb in Ordnung. Für den Echtbetrieb beides lokal ablegen (DSGVO, Google Fonts).

## Stand
- Station Berg: echte 15-Min.-Werte vom 04.11.2026, die anderen drei Stationen: Beispielwerte.
- Live-Daten von Holfuy kommen später über ein WordPress-Plugin (API-Key nur serverseitig).
- Gelände: Bayerische Vermessungsverwaltung, www.geodaten.bayern.de (CC BY 4.0).

Quelle: Repo dhcps/lgf-homepage, Ordner deploy/wind-stationen/ (Entwicklungsstand: entwurf/wind-stationen-3d/).
