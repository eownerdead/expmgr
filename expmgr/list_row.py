from gi.repository import GLib, GObject, Gtk


@Gtk.Template(resource_path='/com/example/expmgr/ui/list_row.ui'
              )  # type: ignore
class ListRow(Gtk.ListBoxRow):
    __gtype_name__ = 'ListRow'

    @GObject.Signal()  # type: ignore
    def changed(self) -> None:
        pass

    @GObject.Signal()  # type: ignore
    def edit_clicked(self) -> None:
        pass

    @GObject.Signal()  # type: ignore
    def delete_clicked(self) -> None:
        pass

    expire_calendar = Gtk.Template.Child()

    name = GObject.Property(type=str)  # type: ignore
    entry_name = GObject.Property(type=str)  # type: ignore

    @GObject.Property(type=GLib.DateTime)
    def expire(self) -> GLib.DateTime:
        return self._expire

    @expire.setter  # type: ignore
    def expire(self, v: GLib.DateTime) -> None:
        self._expire = v
        # TODO: Do not padding with zero
        self.expire_label = self.expire.format('%x')

    expire_label = GObject.Property(type=str)  # type: ignore

    @GObject.Property(type=bool, default=False)
    def editing(self) -> bool:
        return self._editing

    @editing.setter  # type: ignore
    def editing(self, v: bool) -> None:
        self._editing = v
        if not self._editing:
            self.changed()
            self.emit('changed')

    @Gtk.Template.Callback()  # type: ignore
    def on_edit_clicked(self, w: Gtk.ToggleButton) -> None:
        if self.editing:
            self.name = self.entry_name
            self.expire = self.expire_calendar.get_date()  # type: ignore
        else:
            self.entry_name = self.name
            self.expire_calendar.select_day(self.expire)

        self.emit('edit_clicked')

    @Gtk.Template.Callback()  # type: ignore
    def on_delete_clicked(self, w: Gtk.Button) -> None:
        self.emit('delete_clicked')
