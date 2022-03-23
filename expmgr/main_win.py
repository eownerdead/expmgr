import typing as T
from gettext import gettext as _
from pathlib import Path

from gi.repository import Adw, Gio, GLib, GObject, Gtk
from tomlkit.toml_file import TOMLFile

from expmgr.list_view import ListView
from expmgr.shortcuts_win import ShortcutsWin

DATA_DIR = Path(GLib.get_user_data_dir()).joinpath('expmgr/')


@Gtk.Template(resource_path='/com/example/expmgr/ui/main_win.ui'
              )  # type: ignore
class MainWin(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWin'

    leaflet = Gtk.Template.Child()
    sidebar = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    new_list_popover = Gtk.Template.Child()
    new_list_name_entry = Gtk.Template.Child()
    menu = Gtk.Template.Child()

    new_list_popover_message_revealing: bool = GObject.Property(
        type=bool, default=False)  # type: ignore
    new_list_popover_message: str = GObject.Property(type=str)  # type: ignore
    new_list_popover_can_add: bool = GObject.Property(
        type=bool, default=False)  # type: ignore

    def __init__(self, *args: T.Any, **kwargs: T.Any) -> None:
        super().__init__(*args, **kwargs)

        self.set_help_overlay(ShortcutsWin())

        add_list = Gio.SimpleAction.new('add_list', None)
        add_list.connect('activate',
                         lambda action, data: self.new_list_popover.popup())
        self.add_action(add_list)

        add_item = Gio.SimpleAction.new('add_item', None)
        add_item.connect('activate', lambda action, data: self.add_item())
        self.add_action(add_item)

        open_menu = Gio.SimpleAction.new('open_menu', None)
        open_menu.connect('activate', lambda action, data: self.menu.popup())
        self.add_action(open_menu)

        for i in DATA_DIR.glob('*.toml'):
            self.add_list(i.stem)

    @Gtk.Template.Callback()  # type: ignore
    def on_stack_notify_visible_child(self, w: Gtk.Stack,
                                      user_data: T.Any) -> None:
        self.leaflet.navigate(Adw.NavigationDirection.FORWARD)

    @Gtk.Template.Callback()  # type: ignore
    def on_add_list_clicked(self, w: Gtk.Button) -> None:
        self.add_new_list(self.new_list_name_entry.get_text())
        self.new_list_popover.popdown()

    @Gtk.Template.Callback()  # type: ignore
    def on_new_list_name_entry_changed(self, w: Gtk.Entry) -> None:
        if not w.get_text():
            self.new_list_popover_can_add = False
            self.new_list_popover_message_showing = False
        elif data_file_path(w.get_text()).exists():
            self.new_list_popover_can_add = False
            self.new_list_popover_message = _(
                'A list with that name already exists.')
            self.new_list_popover_message_revealing = True
        else:
            self.new_list_popover_can_add = True
            self.new_list_popover_message_revealing = False

    @Gtk.Template.Callback()  # type: ignore
    def on_go_previous_clicked(self, w: Gtk.Button) -> None:
        self.leaflet.navigate(Adw.NavigationDirection.BACK)

    @Gtk.Template.Callback()  # type: ignore
    def on_add_item_clicked(self, w: Gtk.Button) -> None:
        self.add_item()

    def on_quit(self, app: Adw.Application) -> None:
        for i in self.stack:
            i.save_db()

    def add_list(self, name: str) -> None:
        f = TOMLFile(str(data_file_path(name)))
        self.stack.add_titled(ListView(file=f), None, name)

    def add_new_list(self, name: str) -> None:
        data_file_path(name).touch()
        self.add_list(name)

    def add_item(self) -> None:
        self.stack.get_visible_child().on_add_clicked()


def data_file_path(name: str) -> Path:
    return DATA_DIR.joinpath(name).with_suffix('.toml')
