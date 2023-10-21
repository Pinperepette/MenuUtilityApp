#!/usr/bin/env python
import subprocess
import rumps
import os

def execute_commands(verify_command, modify_command):
    verify_process = subprocess.Popen(verify_command, shell=True, stdout=subprocess.PIPE)
    output_verify = verify_process.communicate()[0]
    condition = output_verify.strip() != b"1"
    command = f"{modify_command} -bool {'true' if condition else 'false'} ; killall Finder"
    subprocess.run(["sh", "-c", command])

def toggle_finder_visibility(sender):
    verify_command = "defaults read com.apple.finder AppleShowAllFiles"
    modify_command = "defaults write com.apple.finder AppleShowAllFiles"
    execute_commands(verify_command, modify_command)

def toggle_file_extensions(sender):
    verify_command = "defaults read NSGlobalDomain AppleShowAllExtensions"
    modify_command = "defaults write NSGlobalDomain AppleShowAllExtensions"
    execute_commands(verify_command, modify_command)

def toggle_hard_drive_icon(sender):
    verify_command = "defaults read com.apple.finder ShowHardDrivesOnDesktop"
    modify_command = "defaults write com.apple.finder ShowHardDrivesOnDesktop"
    execute_commands(verify_command, modify_command)

def create_dock_spacer(sender):
    spacer_command = 'defaults write com.apple.dock persistent-apps -array-add \'{"tile-type"="spacer-tile";}\'; killall Dock'
    subprocess.run(["sh", "-c", spacer_command])

class UtilityApp(rumps.App):
    def __init__(self):
        super(UtilityApp, self).__init__("Utility", icon=os.path.join(os.getcwd(), "icon.png"))
        self.menu = [
            rumps.MenuItem("Toggle Finder Visibility", callback=toggle_finder_visibility),
            rumps.MenuItem("Toggle File Extensions", callback=toggle_file_extensions),
            rumps.MenuItem("Toggle Hard Drive Icon", callback=toggle_hard_drive_icon),
            rumps.MenuItem("Create Dock Spacer", callback=create_dock_spacer)
        ]

if __name__ == "__main__":
    app = UtilityApp()
    app.run()
