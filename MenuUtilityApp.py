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

class FinderMenu(rumps.MenuItem):
    def __init__(self):
        super(FinderMenu, self).__init__("Finder")
        self.add(rumps.MenuItem("Toggle Finder Visibility", callback=self.toggle_finder_visibility))
        self.add(rumps.MenuItem("Toggle File Extensions", callback=self.toggle_file_extensions))

    def toggle_finder_visibility(self, sender):
        verify_command = "defaults read com.apple.finder AppleShowAllFiles"
        modify_command = "defaults write com.apple.finder AppleShowAllFiles"
        execute_commands(verify_command, modify_command)

    def toggle_file_extensions(self, sender):
        verify_command = "defaults read NSGlobalDomain AppleShowAllExtensions"
        modify_command = "defaults write NSGlobalDomain AppleShowAllExtensions"
        execute_commands(verify_command, modify_command)

class DockMenu(rumps.MenuItem):
    def __init__(self):
        super(DockMenu, self).__init__("Dock")
        self.add(rumps.MenuItem("Create Dock Spacer", callback=self.create_dock_spacer))

    def create_dock_spacer(self, sender):
        spacer_command = 'defaults write com.apple.dock persistent-apps -array-add \'{"tile-type"="spacer-tile";}\'; killall Dock'
        subprocess.run(["sh", "-c", spacer_command])

class DesktopMenu(rumps.MenuItem):
    def __init__(self):
        super(DesktopMenu, self).__init__("Desktop")
        self.add(rumps.MenuItem("Toggle Hard Drive Icon", callback=self.toggle_hard_drive_icon_on_desktop))
        self.add(rumps.MenuItem("Stage Manager", callback=self.toggle_stage_manager))
        self.add(rumps.MenuItem("Capture Screenshot", callback=self.capture_screenshot))
        self.add(rumps.MenuItem("Capture Selected Area", callback=self.capture_selected_area))

    def capture_screenshot(self, sender):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        screenshot_filename = os.path.join(desktop_path, "screenshot.png")
        subprocess.run(["screencapture", screenshot_filename])

    def capture_selected_area(self, sender):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        screenshot_filename = os.path.join(desktop_path, "selected_area_screenshot.png")
        subprocess.run(["screencapture", "-i", screenshot_filename])

    def toggle_hard_drive_icon_on_desktop(self, sender):
        verify_command = "defaults read com.apple.finder ShowExternalHardDrivesOnDesktop"
        modify_command = "defaults write com.apple.finder ShowExternalHardDrivesOnDesktop"
        execute_commands(verify_command, modify_command)

    def toggle_stage_manager(self, sender):
        current_value = subprocess.check_output(['defaults', 'read', 'com.apple.WindowManager', 'GloballyEnabled']).strip()
        new_value = 'true' if current_value == b'0' else 'false'
        subprocess.run(['defaults', 'write', 'com.apple.WindowManager', 'GloballyEnabled', '-bool', new_value])


class UtilityApp(rumps.App):
    def __init__(self):
        super(UtilityApp, self).__init__("Utility", icon=os.path.join(os.getcwd(), "icon.png"))
        self.menu = [
            FinderMenu(),
            rumps.separator,
            DockMenu(),
            rumps.separator,
            DesktopMenu(),
            rumps.separator
        ]

if __name__ == "__main__":
    app = UtilityApp()
    app.run()

