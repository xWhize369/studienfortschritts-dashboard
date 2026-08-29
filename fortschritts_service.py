"""Berechnungen für die Kennzahlen des Dashboards."""

from datetime import date

from modell import Modulstatus, Studiengang, Zeitplanstatus


class FortschrittsService:
    """Berechnet alle fachlichen Werte für das Dashboard."""

    def berechne_erreichte_ects(self, studiengang: Studiengang) -> int:
        """Addiert die ECTS aller bestandenen Module."""
        erreichte_ects = 0
        for modul in studiengang.alle_module():
            if modul.status == Modulstatus.BESTANDEN:
                erreichte_ects += modul.ects
        return erreichte_ects

    def berechne_fortschritt(self, studiengang: Studiengang) -> float:
        """Berechnet den erreichten Anteil in Prozent."""
        erreichte_ects = self.berechne_erreichte_ects(studiengang)
        return erreichte_ects / studiengang.erforderliche_ects * 100

    def berechne_notendurchschnitt(
        self, studiengang: Studiengang
    ) -> float | None:
        """Berechnet den ECTS-gewichteten Notendurchschnitt."""
        notensumme = 0.0
        ects_summe = 0

        for modul in studiengang.alle_module():
            note = modul.pruefungsleistung.note
            if note is not None and modul.status == Modulstatus.BESTANDEN:
                notensumme += note * modul.ects
                ects_summe += modul.ects

        if ects_summe == 0:
            return None
        return notensumme / ects_summe

    def ist_notenziel_erreicht(self, studiengang: Studiengang) -> bool:
        """Prüft, ob der Durchschnitt dem Notenziel entspricht."""
        durchschnitt = self.berechne_notendurchschnitt(studiengang)
        if durchschnitt is None:
            return False
        return durchschnitt <= studiengang.notenziel

    def ermittle_zeitplanstatus(
        self, studiengang: Studiengang, stichtag: date
    ) -> Zeitplanstatus:
        """Vergleicht ECTS-Anteil und vergangenen Zeitanteil."""
        gesamtdauer = (studiengang.zieltermin - studiengang.studienbeginn).days
        vergangene_dauer = (stichtag - studiengang.studienbeginn).days

        if vergangene_dauer < 0:
            vergangene_dauer = 0
        if vergangene_dauer > gesamtdauer:
            vergangene_dauer = gesamtdauer

        zeitanteil = vergangene_dauer / gesamtdauer
        ects_anteil = (
            self.berechne_erreichte_ects(studiengang)
            / studiengang.erforderliche_ects
        )

        if ects_anteil >= zeitanteil:
            return Zeitplanstatus.IM_PLAN
        return Zeitplanstatus.AUFHOLBEDARF
