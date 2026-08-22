import speech_recognition as sr
import pyttsx3
import sys

class SprachLogikKI:
    def __init__(self):
        # Sprachausgabe initialisieren
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)  # Sprechgeschwindigkeit

        # Mikrofon initialisieren
        self.mic = sr.Microphone()
        self.recognizer = sr.Recognizer()

        # Logik-Daten
        self.fakten = set()
        self.regeln = []

    def sprechen(self, text):
        print(f"KI: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def zuhoeren(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("KI hört zu... (Sprechen Sie jetzt)")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language="de-DE")
                print(f"Sie: {text}")
                return text.lower()
            except sr.UnknownValueError:
                self.sprechen("Ich habe Sie leider nicht verstanden. Bitte wiederholen Sie.")
                return None
            except sr.RequestError:
                self.sprechen("Ich habe gerade keine Verbindung zum Spracherkennungsdienst.")
                return None
            except sr.WaitTimeoutError:
                self.sprechen("Ich habe nichts gehört. Sagen Sie etwas, oder sagen Sie 'Beenden'.")
                return None

    def add_fakt(self, subjekt, praedikat):
        self.fakten.add((praedikat, subjekt))
        self.sprechen(f"Verstanden. {subjekt} ist jetzt {praedikat}.")

    def add_regel(self, bedingungen, schlussfolgerung):
        self.regeln.append((bedingungen, schlussfolgerung))
        self.sprechen("Regel gespeichert.")

    def infer(self):
        neue_fakten = set(self.fakten)
        veraendert = True
        while veraendert:
            veraendert = False
            for bedingungen, schlussfolgerung in self.regeln:
                # Alle Subjekte aus den Fakten holen
                subjekte = {s for _, s in self.fakten}
                for subjekt in subjekte:
                    alle_erfuellt = True
                    for p, s in bedingungen:
                        if s == "X":
                            if (p, subjekt) not in self.fakten:
                                alle_erfuellt = False
                                break
                        else:
                            if (p, s) not in self.fakten:
                                alle_erfuellt = False
                                break
                    
                    if alle_erfuellt:
                        neues_p, neues_s = schlussfolgerung
                        if neues_s == "X":
                            neues_s = subjekt
                        if (neues_p, neues_s) not in neue_fakten:
                            neue_fakten.add((neues_p, neues_s))
                            veraendert = True
                            self.sprechen(f"Logisch abgeleitet: {neues_s} ist {neues_p}")
        self.fakten = neue_fakten

    def query(self, subjekt, praedikat):
        self.infer()
        return (praedikat, subjekt) in self.fakten

    def run(self):
        self.sprechen("Logik-KI gestartet. Sie können mir Fakten nennen, Regeln beibringen oder Fragen stellen.")
        
        while True:
            befehl = self.zuhoeren()
            if not befehl:
                continue

            if "beenden" in befehl or "stop" in befel:
                self.sprechen("Programm wird beendet.")
                break
            
            # Befehlsparser (einfach gehalten)
            elif "fakt" in befehl:
                # Beispiel: "Fakt: Sokrates ist ein Mensch"
                teile = befehl.replace("fakt", "").split(" ist ")
                if len(teile) == 2:
                    subjekt = teile[0].strip()
                    praedikat = teile[1].strip()
                    self.add_fakt(subjekt, praedikat)
                else:
                    self.sprechen("Bitte sagen Sie: Fakt: [Subjekt] ist [Eigenschaft]")

            elif "regel" in befehl:
                # Beispiel: "Regel: Wenn X ein Mensch ist, dann ist X sterblich"
                self.sprechen("Regeln sind in dieser Testversion noch komplexer. Bitte nutzen Sie den Python-Code für Regeln oder sagen Sie Fakt.")
                self.sprechen("Beispiel für einen Fakt: Fakt: X ist ein Mensch")

            elif "ist" in befehl:
                # Beispiel: "Ist Sokrates sterblich?"
                teile = befehl.replace("ist", "").split()
                if len(teile) >= 2:
                    subjekt = teile[0].strip()
                    praedikat = " ".join(teile[1:]).strip()
                    if self.query(subjekt, praedikat):
                        self.sprechen(f"Ja, {subjekt} ist {praedikat}.")
                    else:
                        self.sprechen(f"Nein, nach meinem Wissen ist {subjekt} nicht {praedikat}.")

            else:
                self.sprechen("Ich habe das nicht verstanden. Sagen Sie 'Fakt', 'Ist' oder 'Beenden'.")

if __name__ == "__main__":
    ki = SprachLogikKI()
    ki.run()
