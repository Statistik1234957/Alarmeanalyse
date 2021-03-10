# Alarmeanalyse
Code for Alarm Analysis


Verwendete Packages: (Manche müssten schon mitgeliefert werden und müssen nicht explizit installiert werden)

collections 
logging
os
glob
xml
pandas 
numpy 
datetime 
json
requests
time
sqlalchemy 

Auzuführende Datei: get_data_into_log_file.py

In der Config Datei stehen Informationen bzgl des Aufenhaltorts der CSV Dateien ,sowie Datenbank und APi Informationen

database.py, get_bearer_token.py , get_state_api.py , get_state_db.py: Alles Dateien, die noch nicht aufgefrufen werden, Prinzipiell die generellen Konstrukte für eine dynamische Anbindung.

Code Aufbau : Siehe Confluence

Links: 

https://grob-net4industry.atlassian.net/browse/CLOUD-3631

https://grob-net4industry.atlassian.net/wiki/spaces/G4ANALYZE/pages/2566422553/Alarme+Analyse+der+Stoplog+und+Rec-Dateien
