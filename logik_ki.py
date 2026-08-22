import sys

class LogikKI:
    def __init__(self):
        self.fakten = set()       # Speichert konkrete Fakten, z.B. ("ist_mensch", "Sokrates")
        self.regeln = []          # Speichert Regeln: (Bedingungen, Schlussfolgerung)

    def add_fakt(self, praedikat, subjekt):
        self.fakten.add((praedikat, subjekt))

    def add_regel(self, bedingungen, schlussfolgerung):
        """
        Bedingungen: Liste von Tupeln, z.B. [("ist_mensch", "X")]
        Schlussfolgerung: Tupel, z.B. ("ist_sterblich", "X")
        """
        self.regeln.append((bedingungen, schlussfolgerung))

    def infer(self):
        neue_fakten = set(self.fakten)
        veraendert = True

        while veraendert:
            veraendert = False
            for bedingungen, schlussfolgerung in self.regeln:
                # Wir prüfen, ob es eine Variable gibt, die alle Bedingungen erfüllt
                # Da wir einfach gehalten sind, versuchen wir alle bekannten Subjekte
                for subjekt in {s for _, s in self.fakten}:
                    # Prüfen, ob alle Bedingungen mit diesem Subjekt erfüllt sind
                    alle_erfuellt = True
                    for p, s in bedingungen:
                        # Wenn in der Bedingung "X" steht, ist es eine Variable
                        if s == "X":
                            if (p, subjekt) not in self.fakten:
                                alle_erfuellt = False
                                break
                        else:
                            # Wenn ein konkretes Subjekt in der Bedingung steht
                            if (p, s) not in self.fakten:
                                alle_erfuellt = False
                                break
                    
                    # Wenn alle Bedingungen erfüllt sind, wende die Schlussfolgerung an
                    if alle_erfuellt:
                        neues_praedikat, neues_subjekt = schlussfolgerung
                        if neues_subjekt == "X":
                            neues_subjekt = subjekt # Variable ersetzen
                        
                        if (neues_praedikat, neues_subjekt) not in neue_fakten:
                            neue_fakten.add((neues_praedikat, neues_subjekt))
                            veraendert = True
                            print(f"LOGIK: Abgeleitet -> {neues_subjekt} ist {neues_praedikat}")

        self.fakten = neue_fakten

    def query(self, praedikat, subjekt):
        self.infer()
        return (praedikat, subjekt) in self.fakten


# ==========================================
# TEST
# ==========================================
if __name__ == "__main__":
    ki = LogikKI()

    # 1. Basiswissen (Fakten) eingeben
    ki.add_fakt("ist_mensch", "Sokrates")
    ki.add_fakt("ist_mensch", "Platon")

    # 2. Regeln eingeben (X = Variable)
    # Regel 1: Wenn X ein Mensch ist, dann ist X sterblich.
    ki.add_regel([("ist_mensch", "X")], ("ist_sterblich", "X"))
    
    # Regel 2: Wenn es regnet, wird die Straße nass.
    ki.add_fakt("es_regnet", "wetter")
    ki.add_regel([("es_regnet", "wetter")], ("strasse_ist_nass", "wetter"))

    print("--- Starte Inferenz ---")
    ki.infer()

    print("\n--- Abfragen ---")
    print(f"Ist Sokrates sterblich? -> {ki.query('ist_sterblich', 'Sokrates')}")
    print(f"Ist Platon sterblich? -> {ki.query('ist_sterblich', 'Platon')}")
    print(f"Ist die Straße nass? -> {ki.query('strasse_ist_nass', 'wetter')}")
    print(f"Ist Sokrates ein Gott? -> {ki.query('ist_gott', 'Sokrates')}")
