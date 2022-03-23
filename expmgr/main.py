import sys
import typing as T
from gettext import gettext as _

from gi.repository import Adw, Gio, Gtk

from expmgr.main_win import MainWin  # noqa: E402


class App(Adw.Application):
    def __init__(self, ver: str) -> None:
        super().__init__()

        self.ver = ver

        self.connect('activate', self.on_activate)
        self.connect('shutdown', self.on_shutdown)

        about = Gio.SimpleAction.new('about', None)
        about.connect('activate', self.on_about)
        self.add_action(about)

    def on_activate(self, app: Adw.Application) -> None:
        self.win = MainWin(application=self)
        self.win.present()

    def on_shutdown(self, app: Adw.Application) -> None:
        self.win.on_quit(app)

    def on_about(self, action: Gio.SimpleAction, data: T.Any) -> None:
        dialog = Gtk.AboutDialog(
            modal=True,
            transient_for=self.win,
            program_name='ExpMgr',
            version=self.ver,
            comments=_('Manage expiry dates'),
        )
        dialog.present()


def main(ver: str) -> int:
    return App(ver).run(sys.argv)
