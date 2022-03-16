import typing as T

from gi.repository import GObject, Gtk


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
        self.set_visible(False)

    def append(self, child: Gtk.Widget) -> None:
        self.list_box.append(child)
        self.set_visible(True)
