"""Erzeugt die Objekte und startet das Dashboard."""

from pathlib import Path

from dashboard_controller import DashboardController
from dashboard_view import DashboardView
from fortschritts_service import FortschrittsService
from json_studiengang_repository import JsonStudiengangRepository


class DashboardApp:
    """Erzeugt die Schichten des Programms und verbindet sie."""

    def start(self) -> None:
        """Startet das Dashboard mit der mitgelieferten JSON-Datei."""
        ordner = Path(__file__).parent
        repository = JsonStudiengangRepository(ordner / "studiengang.json")
        service = FortschrittsService()
        controller = DashboardController(service, repository)
        view = DashboardView(controller)
        view.anzeigen()
