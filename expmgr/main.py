import sys

from gi.repository import Adw

from expmgr.main_win import MainWin  # noqa: E402


class App(Adw.Application):
    def __init__(self) -> None:
        super().__init__()
        self.connect('activate', self.on_activate)
        self.connect('shutdown', self.on_shutdown)

    def on_activate(self, app: Adw.Application) -> None:
        self.win = MainWin(application=self)
        self.win.load_db()
        self.win.present()

    def on_shutdown(self, app: Adw.Application) -> None:
        self.win.save_db()


def main() -> int:
    return App().run(sys.argv)
