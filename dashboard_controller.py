"""Verbindet Speicherung, Berechnungen und Darstellung."""

from datetime import date

from dashboard_daten import DashboardDaten
from fortschritts_service import FortschrittsService
from json_studiengang_repository import JsonStudiengangRepository
from modell import Studiengang


class DashboardController:
    """Bereitet die gespeicherten Daten für die View vor."""

    def __init__(
        self,
        service: FortschrittsService,
        repository: JsonStudiengangRepository,
    ):
        self.service = service
        self.repository = repository

    def lade_dashboard_daten(self) -> DashboardDaten:
        """Lädt die Daten und gibt ein festes Datenobjekt zurück."""
        studiengang = self.repository.laden()
        return DashboardDaten(
            studiengang_name=studiengang.name,
            erreichte_ects=self.service.berechne_erreichte_ects(studiengang),
            erforderliche_ects=studiengang.erforderliche_ects,
            fortschritt_prozent=self.service.berechne_fortschritt(studiengang),
            notendurchschnitt=self.service.berechne_notendurchschnitt(
                studiengang
            ),
            notenziel=studiengang.notenziel,
            notenziel_erreicht=self.service.ist_notenziel_erreicht(studiengang),
            zieltermin=studiengang.zieltermin,
            zeitplanstatus=self.service.ermittle_zeitplanstatus(
                studiengang, date.today()
            ),
            module=studiengang.alle_module(),
        )

    def speichere_daten(self, studiengang: Studiengang) -> None:
        """Gibt einen Studiengang an das Repository weiter."""
        self.repository.speichern(studiengang)
