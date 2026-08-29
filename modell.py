"""Datenklassen des Studienfortschritts-Dashboards."""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Modulstatus(Enum):
    """Mögliche Bearbeitungsstände eines Moduls."""

    OFFEN = "offen"
    IN_BEARBEITUNG = "in Bearbeitung"
    BESTANDEN = "bestanden"


class Zeitplanstatus(Enum):
    """Zeigt, ob der ECTS-Fortschritt zum Zeitplan passt."""

    IM_PLAN = "im Plan"
    AUFHOLBEDARF = "Aufholbedarf"


@dataclass
class Pruefungsleistung:
    """Enthält die optionale Note eines Moduls."""

    note: float | None = None


@dataclass
class Modul:
    """Beschreibt ein Modul mit ECTS, Status und Prüfungsleistung."""

    name: str
    ects: int
    status: Modulstatus = Modulstatus.OFFEN
    pruefungsleistung: Pruefungsleistung = field(
        default_factory=Pruefungsleistung
    )


@dataclass
class Semester:
    """Gruppiert die Module eines Fachsemesters."""

    nummer: int
    module: list[Modul] = field(default_factory=list)


@dataclass
class Studiengang:
    """Enthält Ziele, Termine und Semester des Studiengangs."""

    name: str
    erforderliche_ects: int
    studienbeginn: date
    zieltermin: date
    notenziel: float
    semester: list[Semester] = field(default_factory=list)

    def alle_module(self) -> list[Modul]:
        """Gibt die Module aller Semester als eine Liste zurück."""
        module = []
        for semester in self.semester:
            for modul in semester.module:
                module.append(modul)
        return module
