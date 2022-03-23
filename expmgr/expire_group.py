import typing as T

from gi.repository import GObject, Gtk

from expmgr.list_row import ListRow


@Gtk.Template(resource_path='/com/example/expmgr/ui/expire_group.ui'
              )  # type: ignore
class ExpireGroup(Gtk.Box):
    __gtype_name__ = 'ExpireGroup'

    label = GObject.Property(type=str)  # type: ignore
    list_box = Gtk.Template.Child()

    def __init__(self,
                 label_style: str = None,
                 *args: T.Any,
                 **kwargs: T.Any) -> None:
        super().__init__(*args, **kwargs)

        self.list_box.set_sort_func(lambda a, b: a.expire.compare(b.expire))

        if label_style is not None:
            self.add_css_class(label_style)

        self.update()

    @GObject.Signal()  # type: ignore
    def changed(self) -> None:
        pass

    def update(self) -> None:
        has_child = self.list_box.get_first_child() is not None
        self.set_visible(has_child)

    def append(self, child: ListRow) -> None:
        child.connect('changed', lambda _: self.emit('changed'))
        self.list_box.append(child)

    def remove(self, child: ListRow) -> None:
        self.list_box.remove(child)
        self.update()
