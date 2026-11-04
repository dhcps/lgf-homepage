# LGF Homepage

Entwurf einer neuen Homepage für die [Lenggrieser Gleitschirmflieger e.V.](https://www.lenggrieser-gleitschirmflieger.de/) und ein WordPress-Plugin, das die Daten der vereinseigenen Holfuy-Windstationen modern darstellt.

## Inhalt

- `entwurf/index.html`: klickbarer Entwurf der Startseite mit Wetterbereich. Einfach im Browser öffnen. Windwerte von Brauneck Berg sind echt (04.11.2026), die anderen Stationen Beispieldaten. News-Texte stammen von der aktuellen Vereinsseite.
- `entwurf/img/`: Vereinsfotos, fürs Web verkleinert.

## Designrichtung

Ruhig und fotografisch, angelehnt an den Dribbble-Shot „Velora Wellness Landing Page“: großes gerundetes Hero-Foto mit Glas-Navigation, Serifen-Überschriften (Instrument Serif), Manrope als Fließtext, Pill-Buttons in Schirm-Lime, weiche Karten ohne Rahmen. Alles lässt sich mit Elementor-Standardbausteinen nachbauen (Container mit Hintergrundbild und Radius, Überschrift, Button, Beitragsliste/Loop-Grid, Galerie).

## Holfuy-Stationen

| ID   | Station              |
|------|----------------------|
| 1343 | Brauneck Berg (Nord-/Südstart) |
| 1516 | Brauneck Garland     |
| 1202 | Brauneck Landeplatz  |
| 1810 | Blomberg             |

## Datenzugang

Die bisherigen Holfuy-Widgets sind iFrames von `widget.holfuy.com`. Sie lassen sich nur in Sprache, Einheit und Modus einstellen, nicht im Design.

Für eigene Anzeigen nutzen wir die [Holfuy API](https://api.holfuy.com):

- Live: `https://api.holfuy.com/live/?s=1343,1516,1202,1810&pw=KEY&m=JSON&su=km/h&tu=C&loc&daily`
  - `avg=0` aktuell, `avg=1` Viertelstundenmittel, `avg=2` Stundenmittel
- Archiv: `https://api.holfuy.com/archive/` für die Verlaufsgrafik

Den Schlüssel (`pw`) können nur Stations-Admins im Holfuy-Konto erzeugen. **Der Schlüssel kommt nie ins Repo** und wird später in den WordPress-Einstellungen des Plugins hinterlegt.

## Plan

**Grundsatz:** Die Seite bleibt WordPress. News und Artikel schreiben die Autoren weiter wie gewohnt im WordPress-Editor, das neue Design und die Windanzeigen ändern daran nichts.

1. Entwurf der Homepage abstimmen (dieses Repo, `entwurf/`).
2. WordPress-Plugin `lgf-wind`:
   - holt die Daten serverseitig (Schlüssel bleibt geheim) und speichert sie ca. 60 s zwischen, damit nicht jeder Seitenaufruf Holfuy belastet,
   - stellt sie über einen eigenen REST-Endpunkt bereit,
   - zeigt sie als Elementor-Widget und als Shortcode `[lgf_wind station="1343"]` an (Kompass mit Startsektor, Mittelwind, Böen, Verlauf).
3. Neues Design als Elementor-Vorlagen bzw. Theme-Anpassung auf die echte Seite übertragen.
