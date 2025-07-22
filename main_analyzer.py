#!/usr/bin/env python3
"""
Main Analyzer Controller
Zentrale Steuerung für alle Code-Analyse-Tools
"""
import os
import sys
import subprocess
from typing import Dict, List

# ANSI Color Codes für farbige Ausgabe
class Colors:
    # Text Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Background Colors
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    
    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    
    # Reset
    RESET = '\033[0m'
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Färbt Text ein"""
        return f"{color}{text}{Colors.RESET}"

def print_header():
    """Zeigt den Hauptheader an"""
    print(Colors.colorize("=" * 80, Colors.CYAN))
    print(Colors.colorize("CODE ANALYZER SUITE", Colors.BOLD + Colors.CYAN))
    print(Colors.colorize("Professionelle Code-Analyse-Tools", Colors.CYAN))
    print(Colors.colorize("=" * 80, Colors.CYAN))
    print()

def print_menu():
    """Zeigt das Hauptmenü an"""
    menu_items = [
        ("1", "File Length Analyzer", "Analysiert Dateilängen (HTML, CSS, JS, TS)", "analyze_file_length.py"),
        ("2", "JSDoc Coverage Analyzer", "Prüft JSDoc-Dokumentation in JS/TS", "analyze_jsdoc_coverage.py"),
        ("3", "Method Length Analyzer", "Analysiert Methodenlängen in JS/TS", "analyze_method_length_simple.py"),
        ("4", "Console.log Remover", "Entfernt console.log Statements", "remove_console_logs.py"),
        ("5", "Alle Analyzer ausführen", "Führt alle Analyzer nacheinander aus", "all"),
        ("0", "Beenden", "Programm verlassen", "exit")
    ]
    
    print(Colors.colorize("VERFÜGBARE ANALYZER:", Colors.BOLD + Colors.YELLOW))
    print()
    
    for number, title, description, _ in menu_items:
        print(f"{Colors.colorize(number, Colors.BOLD + Colors.GREEN)} - {Colors.colorize(title, Colors.BOLD + Colors.WHITE)}")
        print(f"    {Colors.colorize(description, Colors.BLUE)}")
        print()
    
    print(Colors.colorize("TIPP:", Colors.BOLD + Colors.CYAN))
    print(Colors.colorize("• Einzelauswahl: z.B. '1' oder '3'", Colors.CYAN))
    print(Colors.colorize("• Mehrfachauswahl: z.B. '1,2,4' (mit Komma getrennt)", Colors.CYAN))
    print(Colors.colorize("• Alle ausführen: '5'", Colors.CYAN))
    print()

def get_analyzer_info() -> Dict[str, Dict]:
    """Gibt Informationen über alle verfügbaren Analyzer zurück"""
    return {
        "1": {
            "name": "File Length Analyzer",
            "script": "analyze_file_length.py",
            "description": "Analysiert Dateilängen und findet Dateien > 400 Zeilen",
            "icon": "[FILE]"
        },
        "2": {
            "name": "JSDoc Coverage Analyzer", 
            "script": "analyze_jsdoc_coverage.py",
            "description": "Prüft JSDoc-Dokumentation in JavaScript/TypeScript",
            "icon": "[DOC]"
        },
        "3": {
            "name": "Method Length Analyzer",
            "script": "analyze_method_length_simple.py", 
            "description": "Analysiert Methodenlängen in JavaScript/TypeScript",
            "icon": "[METHOD]"
        },
        "4": {
            "name": "Console.log Remover",
            "script": "remove_console_logs.py",
            "description": "Entfernt console.log Statements aus JS/TS Dateien",
            "icon": "[CLEAN]"
        }
    }

def run_analyzer(script_name: str) -> bool:
    """Führt einen spezifischen Analyzer aus"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    
    if not os.path.exists(script_path):
        print(Colors.colorize(f"FEHLER: Script {script_name} nicht gefunden!", Colors.RED))
        return False
    
    try:
        print(Colors.colorize(f"Starte {script_name}...", Colors.GREEN))
        print(Colors.colorize("-" * 60, Colors.YELLOW))
        
        # Script ausführen
        result = subprocess.run([sys.executable, script_path], 
                              cwd=script_dir,
                              capture_output=False,
                              text=True)
        
        print(Colors.colorize("-" * 60, Colors.YELLOW))
        
        if result.returncode == 0:
            print(Colors.colorize(f"{script_name} erfolgreich abgeschlossen!", Colors.GREEN))
        else:
            print(Colors.colorize(f"{script_name} mit Fehlern beendet (Exit Code: {result.returncode})", Colors.YELLOW))
        
        return result.returncode == 0
        
    except Exception as e:
        print(Colors.colorize(f"FEHLER beim Ausführen von {script_name}: {e}", Colors.RED))
        return False

def run_multiple_analyzers(choices: List[str]) -> None:
    """Führt mehrere ausgewählte Analyzer nacheinander aus"""
    analyzers = get_analyzer_info()
    
    print(Colors.colorize(f"MEHRFACHAUSWAHL: {len(choices)} ANALYZER WERDEN AUSGEFÜHRT", Colors.BOLD + Colors.MAGENTA))
    print(Colors.colorize("=" * 60, Colors.MAGENTA))
    print()
    
    # Zeige alle ausgewählten Analyzer an
    for choice in choices:
        info = analyzers[choice]
        print(f"{Colors.colorize(choice, Colors.BOLD + Colors.GREEN)} - {Colors.colorize(info['name'], Colors.CYAN)}")
    print()
    
    results = []
    
    for i, choice in enumerate(choices, 1):
        info = analyzers[choice]
        
        print(Colors.colorize(f"[{i}/{len(choices)}] {info['icon']} {info['name']}", Colors.BOLD + Colors.CYAN))
        print(Colors.colorize(f"{info['description']}", Colors.BLUE))
        print()
        
        success = run_analyzer(info['script'])
        results.append((info['name'], success))
        
        # Trennlinie zwischen Analyzern (außer beim letzten)
        if i < len(choices):
            print()
            print(Colors.colorize("=" * 60, Colors.YELLOW))
            print()
    
    # Zusammenfassung
    print()
    print(Colors.colorize("ZUSAMMENFASSUNG MEHRFACHAUSWAHL", Colors.BOLD + Colors.MAGENTA))
    print(Colors.colorize("=" * 60, Colors.MAGENTA))
    
    for name, success in results:
        status = "Erfolgreich" if success else "Fehler"
        color = Colors.GREEN if success else Colors.RED
        print(f"{Colors.colorize(status, color)} - {name}")
    
    print()
def run_all_analyzers() -> None:
    analyzers = get_analyzer_info()
    
    print(Colors.colorize("ALLE ANALYZER WERDEN AUSGEFÜHRT", Colors.BOLD + Colors.MAGENTA))
    print(Colors.colorize("=" * 50, Colors.MAGENTA))
    print()
    
    results = []
    
    for key, info in analyzers.items():
        print(Colors.colorize(f"{info['icon']} {info['name']}", Colors.BOLD + Colors.CYAN))
        print(Colors.colorize(f"{info['description']}", Colors.BLUE))
        print()
        
        success = run_analyzer(info['script'])
        results.append((info['name'], success))
        
        print()
        print(Colors.colorize("=" * 50, Colors.YELLOW))
        print()
    
    # Zusammenfassung
    print(Colors.colorize("ZUSAMMENFASSUNG ALLER ANALYZER", Colors.BOLD + Colors.MAGENTA))
    print(Colors.colorize("=" * 50, Colors.MAGENTA))
    
    for name, success in results:
        status = "Erfolgreich" if success else "Fehler"
        color = Colors.GREEN if success else Colors.RED
        print(f"{Colors.colorize(status, color)} - {name}")
    
    print()

def get_user_choice() -> str:
    """Fragt den Benutzer nach seiner Auswahl"""
    while True:
        try:
            choice = input(Colors.colorize("Ihre Auswahl (0-5 oder mehrere mit Komma): ", Colors.BOLD + Colors.YELLOW)).strip()
            
            # Einzelauswahl
            if choice in ['0', '1', '2', '3', '4', '5']:
                return choice
            
            # Mehrfachauswahl prüfen
            if ',' in choice:
                choices = [c.strip() for c in choice.split(',')]
                valid_choices = ['1', '2', '3', '4']
                
                # Prüfen ob alle Auswahlen gültig sind
                if all(c in valid_choices for c in choices):
                    # Duplikate entfernen und sortieren
                    unique_choices = sorted(list(set(choices)))
                    return ','.join(unique_choices)
                else:
                    print(Colors.colorize("Ungültige Mehrfachauswahl! Nur 1,2,3,4 erlaubt (keine 0 oder 5).", Colors.RED))
            else:
                print(Colors.colorize("Ungültige Eingabe! Bitte wählen Sie 0-5 oder mehrere mit Komma.", Colors.RED))
                
        except KeyboardInterrupt:
            print(Colors.colorize("\n\nAuf Wiedersehen!", Colors.YELLOW))
            sys.exit(0)
        except EOFError:
            print(Colors.colorize("\n\nAuf Wiedersehen!", Colors.YELLOW))
            sys.exit(0)

def confirm_action(analyzer_name: str) -> bool:
    """Fragt nach Bestätigung für die Ausführung"""
    print(Colors.colorize(f"Sie sind dabei, '{analyzer_name}' auszuführen.", Colors.YELLOW))
    
    # Spezielle Warnung für Console.log Remover
    if "Console.log Remover" in analyzer_name:
        print(Colors.colorize("WARNUNG: Dieser Analyzer VERÄNDERT Ihre Dateien!", Colors.RED))
        print(Colors.colorize("   Stellen Sie sicher, dass Sie Backups haben.", Colors.RED))
    
    while True:
        try:
            response = input(Colors.colorize("Fortfahren? (j/J für Ja, n/N für Nein): ", Colors.BOLD + Colors.CYAN)).strip().lower()
            
            if response in ['j', 'ja', 'y', 'yes']:
                return True
            elif response in ['n', 'nein', 'no']:
                return False
            else:
                print(Colors.colorize("Bitte antworten Sie mit 'j' oder 'n'.", Colors.RED))
                
        except (KeyboardInterrupt, EOFError):
            return False

def main():
    """Hauptfunktion"""
    try:
        while True:
            # Bildschirm leeren (funktioniert auf Windows und Unix)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print_header()
            print_menu()
            
            choice = get_user_choice()
            
            if choice == '0':
                print(Colors.colorize("\nAuf Wiedersehen!", Colors.YELLOW))
                break
                
            elif choice == '5':
                print()
                if confirm_action("ALLE ANALYZER"):
                    print()
                    run_all_analyzers()
                else:
                    print(Colors.colorize("Vorgang abgebrochen.", Colors.YELLOW))
                    
            elif ',' in choice:
                # Mehrfachauswahl
                choices = choice.split(',')
                analyzers = get_analyzer_info()
                
                # Namen der ausgewählten Analyzer sammeln
                analyzer_names = [analyzers[c]['name'] for c in choices]
                action_text = f"MEHRFACHAUSWAHL: {', '.join(analyzer_names)}"
                
                print()
                if confirm_action(action_text):
                    print()
                    run_multiple_analyzers(choices)
                else:
                    print(Colors.colorize("Vorgang abgebrochen.", Colors.YELLOW))
                    
            else:
                # Einzelauswahl
                analyzers = get_analyzer_info()
                analyzer_info = analyzers[choice]
                
                print()
                if confirm_action(analyzer_info['name']):
                    print()
                    run_analyzer(analyzer_info['script'])
                else:
                    print(Colors.colorize("Vorgang abgebrochen.", Colors.YELLOW))
            
            # Warten auf Benutzereingabe
            print()
            input(Colors.colorize("Drücken Sie Enter, um fortzufahren...", Colors.BOLD + Colors.GREEN))
    
    except KeyboardInterrupt:
        print(Colors.colorize("\n\nProgramm durch Benutzer beendet.", Colors.YELLOW))
    except Exception as e:
        print(Colors.colorize(f"\nUnerwarteter Fehler: {e}", Colors.RED))

if __name__ == "__main__":
    main()
