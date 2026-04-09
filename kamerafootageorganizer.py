import shutil
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

### Erstelle Fenster
fenster = tk.Tk()

fenster.title("Footage-Ordner sortieren")

fenster.geometry("500x500")

label = tk.Label(fenster, text="Gib bitte den Dateipfad an, auf dem das Footage liegt, das du sortieren möchtest:")
label.pack()

### Nutzer-Eingabe
pfadeingabe = tk.Entry(fenster, width=80)
pfadeingabe.pack()

### Startet, wenn Eingabe durch Knopfdruck bestätigt:
def durchführen():

    ### Eingabe als quellpfad zwischenspeichern
    quellpfad = pfadeingabe.get()

    ### Fehler Abfangen - Wenn Eingabe leer:
    if not quellpfad:
        messagebox.showerror("Eingabe Leer." , "Bitte Pfad angeben.")
        return

    ### Setze quellpfad als Dateipfad für Ursprung der Automatisierung / Sortierung
    quellordner = Path(quellpfad)

    ### Fehler Abfangen - Wenn Pfad kein Ordner:
    if not quellordner.is_dir() and quellordner.exists():
        messagebox.showerror("Pfad kein Ordner." , "Bitte Pfad für \neinen Ordner angeben.")
        return

    ### Fehler Abfangen - Wenn Pfad nicht existiert:
    if not quellordner.exists():
        messagebox.showerror("Pfad existiert nicht." , "Bitte Pfad angeben.")
        return

    ### Zum Zählen der Dateien, die verschoben werden
    zahl_kamera_fotos = 0
    zahl_bearbeitete_fotos = 0
    zahl_videos = 0
    zahl_sonstige = 0

    ### Definiert Zielordner als Dict
    zielordner = {
        "kamera": quellordner / "Kamerafotos",
        "entrauscht": quellordner / "Kamerafotos" / "Entrauscht",
        "bearbeitet": quellordner / "Bearbeitet",
        "videos": quellordner / "Videos",
        "sonstige": quellordner / "Sonstige"
    }

    ### Erstelle Zielordner, falls nicht vorhanden
    for ord in zielordner.values():
        ord.mkdir(parents=True, exist_ok=True)

    ### Durchlaufe alles im Quellordner
    for i in quellordner.iterdir():     

        ### Überspringe Ordner 
        if i.is_dir():                  
            continue

        ### Durchlaufe Prüfung und Verschiebe Dateien entsprechend ihrer Kriterien; Zähle
        if (i.name.startswith("DSC_") and i.name[4:8].isdigit() and i.name.lower().endswith(".jpg") and len(i.name.lower()) == 12) or (i.name.lower().endswith(".nef")):
            zahl_kamera_fotos += 1
            shutil.move(i, zielordner["kamera"] / i.name)            
        elif "Enhanced" in i.name and i.name.lower().endswith(".dng"):
            zahl_kamera_fotos += 1
            shutil.move(i, zielordner["entrauscht"] / i.name)
        elif i.name.lower().endswith(".jpg") or i.name.lower().endswith(".png") or i.name.lower().endswith(".dng"):     
            zahl_bearbeitete_fotos += 1
            shutil.move(i, zielordner["bearbeitet"] / i.name)     
        elif i.name.lower().endswith(".mov"):
            zahl_videos += 1
            shutil.move(i, zielordner["videos"] / i.name)
        else:
            zahl_sonstige += 1
            shutil.move(i, zielordner["sonstige"] / i.name)   

    ### Löscht leere Zielordner
    for ord in zielordner.values():
        if not any(ord.iterdir()):
            ord.rmdir()
    
    ### Wenn Verschiebung stattfindet:
    if any([zahl_bearbeitete_fotos, zahl_kamera_fotos, zahl_videos, zahl_sonstige]):

        ### Bestätige Verschiebung
        bestaetigung = tk.Label(fenster, text=f"{zahl_kamera_fotos} Dateien wurden in den Ordner 'Kamerafotos' verschoben.\n{zahl_bearbeitete_fotos} Dateien wurden in den Ordner 'Bearbeitet' verschoben.\n"
                            f"{zahl_videos} Dateien wurden in den Ordner 'Videos' verschoben.\n{zahl_sonstige} Dateien wurden in den Ordner 'Sonstige' verschoben.")
        bestaetigung.pack()

### Knopf für Bestätigung der Eingabe => durchfuehren()
sortieren = tk.Button(fenster, text="Eingabe bestätigen", command = durchführen)
sortieren.pack()

### Öffne Fenster
fenster.mainloop()