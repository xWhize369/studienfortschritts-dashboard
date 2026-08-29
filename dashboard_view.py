"""Grafische Darstellung des Dashboards mit Tkinter."""

import tkinter as tk
from tkinter import ttk

from dashboard_controller import DashboardController
from dashboard_daten import DashboardDaten
from modell import Zeitplanstatus


class DashboardView:
    """Zeigt Kennzahlen und Module in einem Tkinter-Fenster."""

    def __init__(self, controller: DashboardController):
        self.controller = controller
        self.fenster = tk.Tk()
        self.fenster.title("Studienfortschritts-Dashboard")
        self.fenster.geometry("1000x650")
        self.fenster.minsize(900, 560)

        self._erstelle_stile()
        self._erstelle_oberflaeche()

    def _erstelle_stile(self) -> None:
        """Legt die Schriftarten für das Dashboard fest."""
        stil = ttk.Style()
        stil.configure("Titel.TLabel", font=("Arial", 24, "bold"))
        stil.configure("Karte.TLabelframe.Label", font=("Arial", 14, "bold"))
        stil.configure("Wert.TLabel", font=("Arial", 12))
        stil.configure(
            "Status.TLabel", font=("Arial", 12, "bold"), foreground="#0B6EBD"
        )
        stil.configure(
            "Gut.TLabel", font=("Arial", 12, "bold"), foreground="#2E7D32"
        )
        stil.configure(
            "Hinweis.TLabel", font=("Arial", 12, "bold"), foreground="#C25A00"
        )
        stil.configure("Treeview", font=("Arial", 11), rowheight=28)
        stil.configure("Treeview.Heading", font=("Arial", 11, "bold"))

    def _erstelle_oberflaeche(self) -> None:
        """Erstellt die Karten, die Modultabelle und den Button."""
        hauptbereich = ttk.Frame(self.fenster, padding=20)
        hauptbereich.pack(fill="both", expand=True)

        self.titel = ttk.Label(hauptbereich, style="Titel.TLabel")
        self.titel.grid(row=0, column=0, columnspan=3, pady=(0, 18))

        for spalte in range(3):
            hauptbereich.columnconfigure(spalte, weight=1)
        hauptbereich.rowconfigure(2, weight=1)

        fortschritt_karte = ttk.LabelFrame(
            hauptbereich, text="Studienfortschritt", style="Karte.TLabelframe"
        )
        fortschritt_karte.grid(
            row=1, column=0, sticky="nsew", padx=(0, 8), pady=(0, 16)
        )
        self.ects_text = ttk.Label(fortschritt_karte, style="Wert.TLabel")
        self.ects_text.pack(anchor="w", padx=15, pady=(16, 8))
        self.fortschrittsbalken = ttk.Progressbar(
            fortschritt_karte, maximum=100
        )
        self.fortschrittsbalken.pack(fill="x", padx=15, pady=6)
        self.prozent_text = ttk.Label(fortschritt_karte, style="Status.TLabel")
        self.prozent_text.pack(anchor="w", padx=15, pady=(6, 16))

        noten_karte = ttk.LabelFrame(
            hauptbereich, text="Notenziel", style="Karte.TLabelframe"
        )
        noten_karte.grid(
            row=1, column=1, sticky="nsew", padx=8, pady=(0, 16)
        )
        self.note_text = ttk.Label(noten_karte, style="Wert.TLabel")
        self.note_text.pack(anchor="w", padx=15, pady=(16, 8))
        self.notenziel_text = ttk.Label(noten_karte, style="Wert.TLabel")
        self.notenziel_text.pack(anchor="w", padx=15, pady=8)
        self.notenstatus_text = ttk.Label(noten_karte, style="Status.TLabel")
        self.notenstatus_text.pack(anchor="w", padx=15, pady=(8, 16))

        zeit_karte = ttk.LabelFrame(
            hauptbereich, text="Zeitplan", style="Karte.TLabelframe"
        )
        zeit_karte.grid(
            row=1, column=2, sticky="nsew", padx=(8, 0), pady=(0, 16)
        )
        self.zieltermin_text = ttk.Label(zeit_karte, style="Wert.TLabel")
        self.zieltermin_text.pack(anchor="w", padx=15, pady=(16, 12))
        self.zeitstatus_text = ttk.Label(zeit_karte, style="Status.TLabel")
        self.zeitstatus_text.pack(anchor="w", padx=15, pady=(12, 16))

        tabellenbereich = ttk.LabelFrame(hauptbereich, text="Module")
        tabellenbereich.grid(row=2, column=0, columnspan=3, sticky="nsew")
        tabellenbereich.columnconfigure(0, weight=1)
        tabellenbereich.rowconfigure(0, weight=1)

        spalten = ("modul", "ects", "status", "note")
        self.modultabelle = ttk.Treeview(
            tabellenbereich, columns=spalten, show="headings"
        )
        self.modultabelle.heading("modul", text="Modul")
        self.modultabelle.heading("ects", text="ECTS")
        self.modultabelle.heading("status", text="Status")
        self.modultabelle.heading("note", text="Note")
        self.modultabelle.column("modul", width=470)
        self.modultabelle.column("ects", width=80, anchor="center")
        self.modultabelle.column("status", width=180, anchor="center")
        self.modultabelle.column("note", width=80, anchor="center")
        self.modultabelle.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        scrollleiste = ttk.Scrollbar(
            tabellenbereich, orient="vertical", command=self.modultabelle.yview
        )
        scrollleiste.grid(row=0, column=1, sticky="ns", pady=10)
        self.modultabelle.configure(yscrollcommand=scrollleiste.set)

        ttk.Button(
            hauptbereich, text="Daten neu laden", command=self.aktualisieren
        ).grid(row=3, column=2, sticky="e", pady=(12, 0))

    def aktualisieren(self) -> None:
        """Lädt die aktuellen Werte über den Controller neu."""
        daten = self.controller.lade_dashboard_daten()
        self._zeige_daten(daten)

    def _zeige_daten(self, daten: DashboardDaten) -> None:
        self.titel.config(
            text=f"Studienfortschritts-Dashboard - {daten.studiengang_name}"
        )
        self.ects_text.config(
            text=f"{daten.erreichte_ects} von {daten.erforderliche_ects} ECTS"
        )
        self.fortschrittsbalken["value"] = daten.fortschritt_prozent
        self.prozent_text.config(
            text=f"{daten.fortschritt_prozent:.1f} % erreicht".replace(".", ",")
        )

        if daten.notendurchschnitt is None:
            note = "noch keine Note"
        else:
            note = f"{daten.notendurchschnitt:.2f}".replace(".", ",")
        self.note_text.config(text=f"Aktueller Durchschnitt: {note}")
        ziel = f"{daten.notenziel:.1f}".replace(".", ",")
        self.notenziel_text.config(text=f"Ziel: {ziel} oder besser")
        if daten.notenziel_erreicht:
            notenstatus = "Ziel erreicht"
            notenstil = "Gut.TLabel"
        else:
            notenstatus = "Ziel nicht erreicht"
            notenstil = "Hinweis.TLabel"
        self.notenstatus_text.config(text=notenstatus, style=notenstil)

        self.zieltermin_text.config(
            text=f"Zieltermin: {daten.zieltermin.strftime('%d.%m.%Y')}"
        )
        if daten.zeitplanstatus == Zeitplanstatus.IM_PLAN:
            zeitstil = "Gut.TLabel"
        else:
            zeitstil = "Hinweis.TLabel"
        self.zeitstatus_text.config(
            text=f"Status: {daten.zeitplanstatus.value}", style=zeitstil
        )

        for eintrag in self.modultabelle.get_children():
            self.modultabelle.delete(eintrag)

        for modul in daten.module:
            note = modul.pruefungsleistung.note
            note_text = "-" if note is None else str(note).replace(".", ",")
            self.modultabelle.insert(
                "",
                "end",
                values=(modul.name, modul.ects, modul.status.value, note_text),
            )

    def anzeigen(self) -> None:
        """Zeigt das Fenster und startet die Ereignisschleife."""
        self.aktualisieren()
        self.fenster.mainloop()
