"""Speichert und lädt den Studiengang als JSON-Datei."""

import json
from datetime import date
from pathlib import Path

from modell import (
    Modul,
    Modulstatus,
    Pruefungsleistung,
    Semester,
    Studiengang,
)


class JsonStudiengangRepository:
    """Kapselt den Zugriff auf die lokale JSON-Datei."""

    def __init__(self, dateipfad: str | Path):
        self._dateipfad = Path(dateipfad)

    def laden(self) -> Studiengang:
        """Lädt den vollständigen Studiengang aus der JSON-Datei."""
        with self._dateipfad.open(encoding="utf-8") as datei:
            daten = json.load(datei)

        semester_liste = []
        for semester_daten in daten["semester"]:
            module = []
            for modul_daten in semester_daten["module"]:
                pruefung = Pruefungsleistung(modul_daten["note"])
                modul = Modul(
                    name=modul_daten["name"],
                    ects=modul_daten["ects"],
                    status=Modulstatus(modul_daten["status"]),
                    pruefungsleistung=pruefung,
                )
                module.append(modul)
            # Für die Aggregation werden Module zuerst erstellt und dann zugeordnet.
            semester_liste.append(Semester(semester_daten["nummer"], module))

        return Studiengang(
            name=daten["name"],
            erforderliche_ects=daten["erforderliche_ects"],
            studienbeginn=date.fromisoformat(daten["studienbeginn"]),
            zieltermin=date.fromisoformat(daten["zieltermin"]),
            notenziel=daten["notenziel"],
            semester=semester_liste,
        )

    def speichern(self, studiengang: Studiengang) -> None:
        """Schreibt den vollständigen Studiengang in die JSON-Datei."""
        semester_liste = []
        for semester in studiengang.semester:
            module = []
            for modul in semester.module:
                module.append(
                    {
                        "name": modul.name,
                        "ects": modul.ects,
                        "status": modul.status.value,
                        "note": modul.pruefungsleistung.note,
                    }
                )
            semester_liste.append(
                {"nummer": semester.nummer, "module": module}
            )

        daten = {
            "name": studiengang.name,
            "erforderliche_ects": studiengang.erforderliche_ects,
            "studienbeginn": studiengang.studienbeginn.isoformat(),
            "zieltermin": studiengang.zieltermin.isoformat(),
            "notenziel": studiengang.notenziel,
            "semester": semester_liste,
        }

        with self._dateipfad.open("w", encoding="utf-8") as datei:
            json.dump(daten, datei, ensure_ascii=False, indent=2)
