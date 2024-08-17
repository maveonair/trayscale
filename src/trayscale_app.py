import os
import sys
import signal

from typing import Dict
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QIcon, QAction

from trayscale.tailscale import TailscaleClient

base_path = os.path.abspath(os.path.dirname(__file__))
resources_path = os.path.join(base_path, "resources")

online_icon_path = os.path.join(resources_path, "online.png")
offline_icon_path = os.path.join(resources_path, "offline.png")


class SysTray(QObject):
    def __init__(self, app: QApplication) -> None:
        super().__init__(parent=None)

        self.systray = QSystemTrayIcon()
        if not self.systray.isSystemTrayAvailable():
            print("System tray not available for this system")
            return

        self.tailscale_client = TailscaleClient()
        is_online = self.tailscale_client.is_online()
        if is_online:
            icon = QIcon(online_icon_path)
        else:
            icon = QIcon(offline_icon_path)

        self.systray.setIcon(icon)
        self.systray.setVisible(True)
        self._update_tooltip(is_online)

        self._make_menu(is_online)
        self.systray.setContextMenu(self.menu)

    def _update_tooltip(self, is_online: bool):
        if is_online:
            self.systray.setToolTip(f"Trayscale: Connected")
        else:
            self.systray.setToolTip(f"Trayscale: Disconnected")

    def _make_menu(self, is_online: bool) -> None:
        self.menu = QMenu()
        self.item_quit = QAction("Quit")

        self.toggle_connectivity = QAction("Connect")
        self._update_action_button_text(is_online)

        self.menu.addAction(self.toggle_connectivity)
        self.menu.addAction(self.item_quit)

    def _update_action_button_text(self, is_online: bool) -> None:
        if is_online:
            self.toggle_connectivity.setText("Disconnect")
        else:
            self.toggle_connectivity.setText("Connect")

    def change_connectivity(self) -> None:
        is_online = self.tailscale_client.is_online()
        if is_online:
            self.tailscale_client.disconnect()

            icon = QIcon(offline_icon_path)
            self.systray.setIcon(icon)

            self._update_action_button_text(is_online=False)
            self._update_tooltip(is_online=False)

            message = "Connection is down"
        else:
            self.tailscale_client.connect()

            icon = QIcon(online_icon_path)
            self.systray.setIcon(icon)

            self._update_action_button_text(is_online=True)
            self._update_tooltip(is_online=True)

            message = "Connection is up"

        self._show_message(title="Trayscale", message=message)

    def _show_message(self, title: str, message: str) -> None:
        icon = QSystemTrayIcon.MessageIcon.NoIcon
        self.systray.showMessage(title, message, icon, 5000)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Trayscale")

    """Needed to close the app with Ctrl+C"""
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    systray = SysTray(app=app)
    systray.item_quit.triggered.connect(app.quit)
    systray.toggle_connectivity.triggered.connect(systray.change_connectivity)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
