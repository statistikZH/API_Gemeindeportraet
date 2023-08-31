# API_Gemeindeportraet

Das [Gemeindeporträt vom Kanton Zürich (zh.ch/gemeindeportraet)](https://zh.ch/gemeindeportraet) ist ein umfassendes Indikatorensystem mit den wichtigsten Fakten zu den Zürcher Gemeinden. Es bietet über 300 Indikatoren für einzelne Gemeinden, Regionen oder den ganzen Kanton. In den meisten Fällen sind Datenreihen über einen längeren Zeitraum verfügbar.

## Datenbezug
Die Daten können entweder direkt im Gemeindeporträt abgefragt und heruntergeladen oder über den [Datenkatalog der offenen Behördendaten]( https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/?q=gemeindeportraet) bezogen werden. Allerdings gibt es derzeit keine Möglichkeit, die Daten direkt über eine Gemeindeporträt-API abzurufen.

Für Nutzende, die selbst auf die Daten im Sinne von Abfragen zugreifen möchten und die Daten möglichst aktuell und auch konsistent auf ihrer Website oder in Applikationen einbinden wollen, sind die bestehenden Datenbezüge umständlich:

- Im Gemeindeportrait müssen zunächst Indikatoren ausgewählt und die Daten dann manuell als CSV oder Excel exportiert werden.

- Im Datenkatalog der offenen Behördendaten hat jede Ressource (Indikator) einen Permalink, aber um alle Links für die über 300 Indikatoren des Gemeindeporträts zu erhalten, müssen diese zusammengesucht werden.

## Dieses Repository
Mit diesem Repository zeigen wir Nutzenden, wie sie systematisch auf die Datensätze des Gemeindeportraits zugreifen können und bieten die Möglichkeit, eine Liste aller Indikatoren mit den entsprechenden Download-URLs zu erhalten. 

Auf Basis dieser Liste, die über die Zugangs-URL direkt in Anwendungen geladen werden kann, lassen sich dann z.B. Visualisierungen erstellen. 

Die Logik ist:

1. Abrufen der Liste der Indikatoren mit den Download-URLs.
2. Herausfiltern des Datensatzes, der visualisiert werden soll, anhand der ID, des Themas oder des Indikatornamens.
3. Laden der Daten direkt über die referenzierte Download-URL.


### Datenzugang
Der gesamte Datenkatalog der offenen Behördendaten des Kantons Zürich steht für Abfragen ebenfalls als offene Schnittstelle via JSON-API-Endpoint zur Verfügung:

> https://www.web.statistik.zh.ch/ogd/daten/zhweb.json

Das JSON beschreibt jeden Datensatz und listet die zum Datensatz gehörigen Distributionen (= Ressource = Indikator = CSV). Für jede Distribution gibt es eine **downloadUrl**, die den Permalink zum Datenfile (CSV) darstellt.

Wie das JSON gefiltert und die relevanten Informationen extrahiert werden können, ist im R-Skript [`get_data.R`](https://github.com/statistikZH/API_Gemeindeportraet/blob/main/get_data.R) dokumentiert.

### Beispiel praktische Anwendung
Wie dies in der Praxis angewendet werden kann, wird in diesem [**Observable Notebook**](https://observablehq.com/@statistikzh/gemeindeportrat-data-access) Schritt für Schritt erklärt und unter «3. Daten visualisieren» sogar visualisiert.
