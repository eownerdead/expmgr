import typing as T
from pathlib import Path

import tomlkit
from gi.repository import Adw, GLib, Gtk
from tomlkit.toml_file import TOMLFile

from expmgr.list_row import ListRow

DATA_PATH = Path(GLib.get_user_data_dir()).joinpath('expmgr/data.toml')

data_file = TOMLFile(str(DATA_PATH))


@Gtk.Template(resource_path='/com/example/expmgr/ui/main_win.ui'
              )  # type: ignore
class MainWin(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWin'

    list_box: ListRow = Gtk.Template.Child()

    def __init__(self, *args: T.Any, **kwargs: T.Any) -> None:
        super().__init__(*args, **kwargs)

    @Gtk.Template.Callback()  # type: ignore
    def on_add_clicked(self, w: Gtk.Button) -> None:
        self.close_editing()
        self.add_list_row(name='',
                          expire=GLib.DateTime.new_now_local(),
                          editing=True)

    def on_list_row_edit_clicked(self, w: ListRow) -> None:
        if w.editing:
            w.editing = False
        else:
            self.close_editing()
            w.editing = True

    def on_list_row_delete_clicked(self, w: ListRow) -> None:
        self.list_box.remove(w)

    def load_db(self) -> None:
        for name, v in data_file.read().items():
            expire = GLib.DateTime.new_local(v['expire'].year,
                                             v['expire'].month,
                                             v['expire'].day,
                                             hour=0,
                                             minute=0,
                                             seconds=0)
            self.add_list_row(name, expire)

    def save_db(self) -> None:
        doc = tomlkit.document()

        for i in self.list_box:
            t = tomlkit.inline_table()
            t.append('expire', tomlkit.date(i.expire.format(r'%Y-%m-%d')))
            doc.add(i.name, t)
        doc.add(tomlkit.nl())

        data_file.write(doc)

    def add_list_row(self,
                     name: str,
                     expire: GLib.DateTime,
                     editing: bool = False) -> None:
        lr = ListRow(name=name, expire=expire, editing=editing)
        lr.connect('edit_clicked', self.on_list_row_edit_clicked)
        lr.connect('delete_clicked', self.on_list_row_delete_clicked)
        self.list_box.append(lr)

    # Must be one ListRow being edited.
    def close_editing(self) -> None:
        for i in self.list_box:
            if i.editing:
                i.editing = False
                break
