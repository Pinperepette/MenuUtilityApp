#!/usr/bin/env python
import subprocess
import rumps
import os

def esegui_comandi(comando_verifica, comando_modifica):
    processo_verifica = subprocess.Popen(comando_verifica, shell=True, stdout=subprocess.PIPE)
    output_verifica = processo_verifica.communicate()[0]
    condizione = output_verifica.strip() != b"1"
    comando = f"{comando_modifica} -bool {'true' if condizione else 'false'} ; killall Finder"
    subprocess.run(["sh", "-c", comando])


def mostra_nascondi_files(sender):
    comando_verifica = "defaults read com.apple.finder AppleShowAllFiles"
    comando_modifica = "defaults write com.apple.finder AppleShowAllFiles"
    esegui_comandi(comando_verifica, comando_modifica)

def mostra_nascondi_files_extensions(sender):
    comando_verifica = "defaults read NSGlobalDomain AppleShowAllExtensions"
    comando_modifica = "defaults write NSGlobalDomain AppleShowAllExtensions"
    esegui_comandi(comando_verifica, comando_modifica)

def mostra_nascondi_icona_disco_rigido(sender):
    comando_verifica = "defaults read com.apple.finder ShowHardDrivesOnDesktop"
    comando_modifica = "defaults write com.apple.finder ShowHardDrivesOnDesktop"
    esegui_comandi(comando_verifica, comando_modifica)

def crea_spazio_dock(sender):
    comando_spazio = 'defaults write com.apple.dock persistent-apps -array-add \'{"tile-type"="spacer-tile";}\'; killall Dock'
    subprocess.run(["sh", "-c", comando_spazio])

class UtilityApp(rumps.App):
    def __init__(self):
        super(UtilityApp, self).__init__("Utility", icon=os.path.join(os.getcwd(), "icon.png"))
        self.menu = [
            rumps.MenuItem("Toggle Finder Visibility", callback=mostra_nascondi_files),
            rumps.MenuItem("Toggle File Extensions", callback=mostra_nascondi_files_extensions),
            rumps.MenuItem("Toggle icon Hard disks", callback=mostra_nascondi_icona_disco_rigido),
            rumps.MenuItem("Create Dock Spacer", callback=crea_spazio_dock)
        ]

if __name__ == "__main__":
    app = UtilityApp()
    app.run()
