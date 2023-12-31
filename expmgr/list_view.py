import typing as T
from gettext import gettext as _

import tomlkit
from gi.repository import GLib, Gtk
from tomlkit.toml_file import TOMLFile

from expmgr.expire_group import ExpireGroup
from expmgr.list_row import ListRow

EXPIRE_GROUP_TBL = ['0d', '1d', '2d', '3d', '1w', '2w', '1m', '3m', '6m', '1y']


@Gtk.Template(resource_path='/com/example/expmgr/ui/list_view.ui'
              )  # type: ignore
class ListView(Gtk.ScrolledWindow):
    __gtype_name__ = 'ListView'

    box = Gtk.Template.Child()

    def __init__(self, file: TOMLFile, *args: T.Any, **kwargs: T.Any) -> None:
        super().__init__(*args, **kwargs)

        self.file = file

        self.add_group(_('Expired'), label_style='error')
        for i in EXPIRE_GROUP_TBL:
            self.add_group(name=fmt_expire_group(i))
        self.add_group(name=_('Others'))

        self.load_db()

    def on_add_clicked(self) -> None:
        self.close_editing()
        self.add_list_row(name='',
                          expire=GLib.DateTime.new_now_local(),
                          editing=True)

    def on_group_changed(self, w: ExpireGroup) -> None:
        for lr in w.list_box:
            w.remove(lr)
            self.insert_list_row(lr)
            w.update()

    def on_list_row_edit_clicked(self, w: ListRow) -> None:
        if w.editing:
            w.editing = False
        else:
            self.close_editing()
            w.editing = True

    def on_list_row_delete_clicked(self, w: ListRow) -> None:
        w.get_parent().remove(w)

    def load_db(self) -> None:
        for name, v in self.file.read().items():
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

        self.file.write(doc)

    def add_group(self, name: str, label_style: str = None) -> None:
        g = ExpireGroup(label=name, label_style=label_style)
        g.connect('changed', self.on_group_changed)
        self.box.append(g)

    def add_list_row(self,
                     name: str,
                     expire: GLib.DateTime,
                     editing: bool = False) -> None:
        lr = ListRow(name=name, expire=expire, editing=editing)

        lr.connect('edit_clicked', self.on_list_row_edit_clicked)
        lr.connect('delete_clicked', self.on_list_row_delete_clicked)

        self.insert_list_row(lr)

    # Insert ListRow into the matching expiry group.
    def insert_list_row(self, list_row: ListRow) -> None:
        for i, group in zip(
            ['-1d'] + EXPIRE_GROUP_TBL + [None],  # type: ignore
                self.box):
            if i is None or expires_after(list_row.expire, i):
                group.append(list_row)
                group.update()
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
