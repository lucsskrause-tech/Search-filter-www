import speech_recognition as sr
import pyttsx3

# Die Logik-Engine
class LogikKI:
    def __init__(self):
        self.fakten = set()
        self.regeln = []
        # Sprachausgabe
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 160)
        except:
            self.engine = None

    def sprechen(self, text):
        print(f"KI: {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass

    def add_fakt(self, subjekt, praedikat):
        self.fakten.add((praedikat, subjekt))
        self.sprechen(f"Verstanden. {subjekt} ist {praedikat}.")

    def infer(self):
        neue_fakten = set(self.fakten)
        veraendert = True
        while veraendert:
            veraendert = False
            for bedingungen, schlussfolgerung in self.regeln:
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
        print("Starte Spracherkennung...")
        self.sprechen("Logik KI gestartet. Ich höre zu.")
        r = sr.Recognizer()
        mic = sr.Microphone()

        while True:
            try:
                with mic as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Höre zu...")
                    audio = r.listen(source, timeout=5)
                
                print("Erkenne Sprache...")
                text = r.recognize_google(audio, language="de-DE")
                print(f"Du sagst: {text}")
                
                if "beenden" in text.lower():
                    self.sprechen("Programm wird beendet. Tschüss!")
                    break
                
                # Befehle verarbeiten
                if "fakt" in text.lower():
                    teile = text.lower().replace("fakt", "").split(" ist ")
                    if len(teile) == 2:
                        self.add_fakt(teile[0].strip(), teile[1].strip())
                    else:
                        self.sprechen("Sag: Fakt: Sokrates ist ein Mensch.")
                
                elif "ist" in text.lower():
                    teile = text.lower().replace("ist", "").split()
                    if len(teile) >= 2:
                        subjekt = teile[0].strip()
                        praedikat = " ".join(teile[1:]).strip()
                        if self.query(subjekt, praedikat):
                            self.sprechen(f"Ja, {subjekt} ist {praedikat}.")
                        else:
                            self.sprechen(f"Nein, {subjekt} ist nicht {praedikat}.")
                else:
                    self.sprechen("Verstehe ich nicht. Sag Fakt oder Ist.")

            except sr.UnknownValueError:
                self.sprechen("Habe ich nicht verstanden. Bitte wiederhole.")
            except sr.RequestError:
                self.sprechen("Keine Verbindung zur Google Spracherkennung.")
            except sr.WaitTimeoutError:
                continue  # Einfach weiterhören

if __name__ == "__main__":
    ki = LogikKI()
    ki.run()
