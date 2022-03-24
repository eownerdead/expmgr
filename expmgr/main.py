import sys
import typing as T
from gettext import gettext as _

from gi.repository import Adw, Gio, Gtk

from expmgr.main_win import MainWin  # noqa: E402


class App(Adw.Application):
    def __init__(self, app_id: str, ver: str) -> None:
        super().__init__(application_id=app_id)

        self.app_id = app_id
        self.ver = ver

        self.connect('activate', self.on_activate)
        self.connect('shutdown', self.on_shutdown)

        about = Gio.SimpleAction.new('about', None)
        about.connect('activate', self.on_about)
        self.add_action(about)

        quit_ = Gio.SimpleAction.new('quit', None)
        quit_.connect('activate', lambda action, data: self.quit())
        self.add_action(quit_)

        self.set_accels_for_action('win.add_list', ['<Primary><Shift>n'])
        self.set_accels_for_action('win.add_item', ['<Primary>n'])
        self.set_accels_for_action('win.open_menu', ['F10'])
        self.set_accels_for_action(
            'win.show-help-overlay', ['<Primary>question'])
        self.set_accels_for_action('app.quit', ['<Primary>q'])

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
            logo_icon_name=self.app_id,
        )
        dialog.present()


def main(app_id: str, ver: str) -> int:
    return App(app_id, ver).run(sys.argv)
