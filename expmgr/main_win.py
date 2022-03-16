import typing as T
from gettext import gettext as _
from pathlib import Path

import tomlkit
from gi.repository import Adw, GLib, Gtk
from tomlkit.toml_file import TOMLFile

from expmgr.expire_group import ExpireGroup
from expmgr.list_row import ListRow

DATA_PATH = Path(GLib.get_user_data_dir()).joinpath('expmgr/data.toml')

data_file = TOMLFile(str(DATA_PATH))

EXPIRE_GROUP_TBL = ['0d', '1d', '2d', '3d', '1w', '2w', '1m', '3m', '6m', '1y']


@Gtk.Template(resource_path='/com/example/expmgr/ui/main_win.ui'
              )  # type: ignore
class MainWin(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWin'

    box = Gtk.Template.Child()

    def __init__(self, *args: T.Any, **kwargs: T.Any) -> None:
        super().__init__(*args, **kwargs)

        self.box.append(ExpireGroup(label=_('Expired'), label_style='error'))
        for i in EXPIRE_GROUP_TBL:
            self.box.append(ExpireGroup(label=fmt_expire_group(i)))
        self.box.append(ExpireGroup(label=_('Others')))

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
        w.get_parent().remove(w)

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

        for group in self.box:
            for i in group.list_box:
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

        for i, group in zip(
            ['-1d'] + EXPIRE_GROUP_TBL + [None],  # type: ignore
                self.box):
            if i is None or expires_after(lr.expire, i):
                group.append(lr)
                return

    # Must be one ListRow being edited.
    def close_editing(self) -> None:
        for group in self.box:
            for list_box in group.list_box:
                if list_box.editing:
                    list_box.editing = False
                    return


def expires_after(date: GLib.DateTime, after: str) -> bool:
    now = GLib.DateTime.new_now_local()

    n = int(after[:-1])
    if after.endswith('d'):
        b = now.add_days(n)
    elif after.endswith('w'):
        b = now.add_weeks(n)
    elif after.endswith('m'):
        b = now.add_months(n)
    elif after.endswith('y'):
        b = now.add_years(n)

    return date.compare(b) == -1


def fmt_expire_group(a: str) -> str:
    n = int(a[:-1])

    # TODO: I18n support.
    if a.endswith('d'):
        if n == 0:
            return _('Today')
        elif n == 1:
            return _('Tomorrow')
        else:
            return _(f'{n} days')
    elif a.endswith('w'):
        if n == 1:
            return _('Next week')
        else:
            return _(f'{n} weeks')
    elif a.endswith('m'):
        if n == 1:
            return _('Next month')
        else:
            return _(f'{n} months')
    elif a.endswith('y'):
        if n == 1:
            return _('Next year')
        else:
            return _(f'{n} years')
    raise Exception('Invalid expire group format')
