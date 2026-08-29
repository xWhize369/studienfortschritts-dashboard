"""Tests für Speicherung und strukturierte Datenübergabe."""

import tempfile
import unittest
from datetime import date
from pathlib import Path

from dashboard_controller import DashboardController
from dashboard_daten import DashboardDaten
from fortschritts_service import FortschrittsService
from json_studiengang_repository import JsonStudiengangRepository
from modell import Modul, Modulstatus, Semester, Studiengang


class RepositoryUndControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_ordner = tempfile.TemporaryDirectory()
        dateipfad = Path(self.temp_ordner.name) / "test.json"
        self.repository = JsonStudiengangRepository(dateipfad)
        self.studiengang = Studiengang(
            "Teststudiengang",
            180,
            date(2025, 3, 1),
            date(2028, 3, 31),
            1.5,
            [Semester(1, [Modul("Testmodul", 10, Modulstatus.OFFEN)])],
        )
        self.controller = DashboardController(
            FortschrittsService(), self.repository
        )
        self.controller.speichere_daten(self.studiengang)

    def tearDown(self) -> None:
        self.temp_ordner.cleanup()

    def test_speichern_und_laden(self) -> None:
        geladen = self.repository.laden()
        self.assertEqual(geladen.name, "Teststudiengang")
        self.assertEqual(geladen.alle_module()[0].name, "Testmodul")

    def test_controller_liefert_dashboard_daten(self) -> None:
        daten = self.controller.lade_dashboard_daten()
        self.assertIsInstance(daten, DashboardDaten)
        self.assertEqual(daten.erforderliche_ects, 180)


if __name__ == "__main__":
    unittest.main()
