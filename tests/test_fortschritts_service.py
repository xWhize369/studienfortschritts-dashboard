"""Tests für die Berechnungen des FortschrittsService."""

import unittest
from datetime import date

from fortschritts_service import FortschrittsService
from modell import (
    Modul,
    Modulstatus,
    Pruefungsleistung,
    Semester,
    Studiengang,
    Zeitplanstatus,
)


class FortschrittsServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        module = [
            Modul(
                "Modul A",
                30,
                Modulstatus.BESTANDEN,
                Pruefungsleistung(1.0),
            ),
            Modul(
                "Modul B",
                30,
                Modulstatus.BESTANDEN,
                Pruefungsleistung(1.2),
            ),
            Modul("Modul C", 10, Modulstatus.IN_BEARBEITUNG),
        ]
        self.studiengang = Studiengang(
            "Teststudiengang",
            180,
            date(2025, 3, 1),
            date(2028, 3, 31),
            1.5,
            [Semester(1, module)],
        )
        self.service = FortschrittsService()

    def test_erreichte_ects(self) -> None:
        self.assertEqual(
            self.service.berechne_erreichte_ects(self.studiengang), 60
        )

    def test_fortschritt(self) -> None:
        fortschritt = self.service.berechne_fortschritt(self.studiengang)
        self.assertAlmostEqual(fortschritt, 33.3, places=1)

    def test_notendurchschnitt(self) -> None:
        durchschnitt = self.service.berechne_notendurchschnitt(self.studiengang)
        self.assertAlmostEqual(durchschnitt, 1.1)

    def test_notenziel(self) -> None:
        self.assertTrue(
            self.service.ist_notenziel_erreicht(self.studiengang)
        )

    def test_zeitplanstatus(self) -> None:
        status = self.service.ermittle_zeitplanstatus(
            self.studiengang, date(2026, 8, 15)
        )
        self.assertEqual(status, Zeitplanstatus.AUFHOLBEDARF)


if __name__ == "__main__":
    unittest.main()
