use adw::prelude::*;
use glib::DateTime;
use gtk::glib;
use relm4::{adw, factory, gtk, send};

use super::app;

#[derive(Debug, Clone)]
pub(crate) struct List {
    pub name: String,
    pub expiration: DateTime,
}

#[relm4::factory_prototype(pub(crate))]
impl factory::FactoryPrototype for List {
    type Factory = factory::FactoryVecDeque<Self>;
    type Msg = app::AppMsg;
    type View = gtk::ListBox;
    type Widgets = ListWidgets;

    view! {
        adw::ActionRow {
            set_selectable: false,
            set_title: watch!(&self.name),
            add_suffix = &gtk::Label {
                set_label: watch!(&self.expiration.format("%x").unwrap()),
            },
            add_suffix = &gtk::MenuButton {
                set_popover: popover = Some(&gtk::Popover) {
                    set_child = Some(&gtk::Box) {
                        set_orientation: gtk::Orientation::Vertical,
                        append: name = &gtk::Entry {
                            connect_activate(popover) => move |_| {
                                popover.popdown();
                            }
                        },
                        append: date = &gtk::Calendar {},
                        append = &gtk::Button {
                            set_label: "Delete",
                            connect_clicked(sender, key, popover) => move |_| {
                                // If do not close popover before remove this,
                                // this app will freeze.
                                popover.popdown();

                                send!(
                                    sender,
                                    app::AppMsg::DelList(key.current_index())
                                );
                            }
                        },
                    },

                    connect_closed(sender, key, name, date) => move |_| {
                        send!(
                            sender,
                            app::AppMsg::UpdateList(
                                key.current_index(),
                                List {
                                    name: name.text().to_string(),
                                    expiration: date.date(),
                                }
                            )
                        )
                    }
                }
            }
        }
    }

    fn position(&self, _key: &factory::DynamicIndex) {}
}
