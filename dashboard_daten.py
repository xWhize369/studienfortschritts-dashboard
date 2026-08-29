"""Strukturierte Datenübergabe vom Controller an die View."""

from dataclasses import dataclass
from datetime import date

from modell import Modul, Zeitplanstatus


@dataclass
class DashboardDaten:
    """Enthält genau die Werte, welche die View anzeigen soll."""

    studiengang_name: str
    erreichte_ects: int
    erforderliche_ects: int
    fortschritt_prozent: float
    notendurchschnitt: float | None
    notenziel: float
    notenziel_erreicht: bool
    zieltermin: date
    zeitplanstatus: Zeitplanstatus
    module: list[Modul]
