from gi.repository import Gtk


@Gtk.Template(resource_path='/com/example/expmgr/ui/shortcuts_win.ui'
              )  # type: ignore
class ShortcutsWin(Gtk.ShortcutsWindow):
    __gtype_name__ = 'ShortcutsWin'
