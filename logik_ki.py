import sys
import json

class LogicalReasoningEngine:
    """
    Eine einfache, rein logische KI, die Fakten (Axiome) und Regeln
    nutzt, um neue, logisch zwingende Schlussfolgerungen zu ziehen.
    """
    def __init__(self):
        self.facts = set()        # Speichert alle bekannten Fakten
        self.rules = []           # Speichert die Wenn-Dann-Regeln

    def add_fact(self, fact):
        """Fügt einen neuen Fakt hinzu."""
        if fact not in self.facts:
            self.facts.add(fact)
            print(f"[INFO] Fakt hinzugefügt: {fact}")

    def add_rule(self, premises, conclusion):
        """
        Fügt eine Regel hinzu.
        premises: Liste von Bedingungen (z.B. ["Es regnet", "Straße ist nass"])
        conclusion: Schlussfolgerung (z.B. "Es gibt Pfützen")
        """
        self.rules.append((premises, conclusion))
        print(f"[INFO] Regel hinzugefügt: Wenn {premises}, dann {conclusion}")

    def infer(self):
        """
        Der logische Motor: Leitet so lange neue Fakten ab, bis keine
        neuen Schlussfolgerungen mehr möglich sind (Fixpunkt).
        """
        new_facts = set(self.facts)
        changed = True
        iteration = 0

        while changed:
            changed = False
            iteration += 1
            for premises, conclusion in self.rules:
                # Prüfe, ob alle Bedingungen erfüllt sind
                if all(p in new_facts for p in premises):
                    if conclusion not in new_facts:
                        new_facts.add(conclusion)
                        changed = True
                        print(f"[LOGIK] Ableitung {iteration}: Aus {premises} folgt logisch: {conclusion}")

        self.facts = new_facts
        return self.facts

    def query(self, statement):
        """Fragt, ob ein Fakt wahr ist (durch logische Ableitung)."""
        self.infer() # Stelle sicher, dass alle Ableitungen gemacht wurden
        return statement in self.facts

    def save_state(self, filename="wissen.json"):
        """Speichert den aktuellen Wissensstand in eine Datei."""
        data = {
            "facts": list(self.facts),
            "rules": [{"premises": list(p), "conclusion": c} for p, c in self.rules]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[INFO] Wissen gespeichert in {filename}")

    def load_state(self, filename="wissen.json"):
        """Lädt Wissen aus einer Datei."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.facts = set(data.get("facts", []))
            self.rules = [(list(r["premises"]), r["conclusion"]) for r in data.get("rules", [])]
            print(f"[INFO] Wissen aus {filename} geladen.")
        except FileNotFoundError:
            print(f"[WARNUNG] Datei {filename} nicht gefunden. Starte leer.")

# ==========================================
# HAUPTPROGRAMM
# ==========================================
if __name__ == "__main__":
    ki = LogicalReasoningEngine()

    # 1. Axiome definieren (Ohne historischen Kontext, nur logische Grundlagen)
    ki.add_fact("Sokrates ist ein Mensch")
    ki.add_fact("Alle Menschen sind sterblich")
    ki.add_fact("Es regnet")
    
    # 2. Regeln definieren (Wenn-Dann)
    ki.add_rule(["Sokrates ist ein Mensch", "Alle Menschen sind sterblich"], "Sokrates ist sterblich")
    ki.add_rule(["Es regnet"], "Die Straße ist nass")
    ki.add_rule(["Die Straße ist nass"], "Es gibt Pfützen")

    # 3. Spekulative, rein logische Schlussfolgerung testen
    print("\n--- Starte logische Inferenz ---")
    ki.infer()

    print("\n--- Abfragen an die KI ---")
    print(f"Ist Sokrates sterblich? -> {ki.query('Sokrates ist sterblich')}")
    print(f"Gibt es Pfützen? -> {ki.query('Es gibt Pfützen')}")
    print(f"Scheint die Sonne? -> {ki.query('Die Sonne scheint')}")

    # 4. Wissen speichern für später
    ki.save_state()
