use adw::prelude::*;
use app::AppMsg;
use glib::DateTime;
use gtk::glib;
use relm4::util::widget_plus::WidgetPlus;
use relm4::{adw, factory, gtk, send};

use super::app;

#[derive(Debug, Clone)]
pub(crate) struct List {
    pub name: String,
    pub expiration: DateTime,

    pub editing: bool,
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
            set_child = Some(&gtk::Box) {
                set_orientation: gtk::Orientation::Vertical,
                append = &adw::ActionRow {
                    set_title: watch!(&self.name),
                    add_suffix: date_label = &gtk::Label {
                        set_label: watch!(
                            &self.expiration.format("%x").unwrap()
                        ),
                    },
                    add_suffix = &gtk::ToggleButton {
                        set_icon_name: "document-edit-symbolic",
                        set_has_frame: false,
                        set_valign: gtk::Align::Center,
                        set_active: watch!(self.editing),
                        connect_toggled(
                            sender,
                            key,
                            name,
                            date
                        ) => move |button| {
                            if button.is_active() {
                                send!(sender, AppMsg::Edit(key.downgrade()));
                            } else {
                                send!(
                                    sender,
                                    AppMsg::EndEdit(
                                        key.downgrade(),
                                        List {
                                            name: name.text().to_string(),
                                            expiration: date.date(),
                                            editing: false,
                                        },
                                    )
                                );
                            }
                        },
                    },
                },
                append = &gtk::Revealer {
                    set_reveal_child: watch!(self.editing),

                    set_child = Some(&gtk::Box) {
                        set_orientation: gtk::Orientation::Vertical,
                        set_margin_all: 12,
                        set_spacing: 6,
                        append = &gtk::Label {
                            set_text: "Name",
                            add_css_class: "heading",
                            set_justify: gtk::Justification::Left,
                            set_xalign: 0.,
                        },
                        append: name = &gtk::Entry {
                            set_text: watch!(&self.name),
                        },
                        append = &gtk::Label {
                            set_text: "Expiration",
                            add_css_class: "heading",
                            set_justify: gtk::Justification::Left,
                            set_xalign: 0.,
                        },
                        append: date = &gtk::Calendar {
                            select_day: watch!(&self.expiration),
                        },
                        append = &gtk::Button {
                            set_label: "Delete",
                            add_css_class: "destructive-action",
                            set_halign: gtk::Align::End,
                            connect_clicked(sender, key) => move |_| {
                                send!(
                                    sender,
                                    app::AppMsg::DelList(key.downgrade())
                                );
                            }
                        },
                    },
                }
            }
        }
    }

    fn post_init(&self, widgets: &Self::Widgets) {
        self.update_date_label(&date_label);
    }

    fn post_view(&self, widgets: &Self::Widgets) {
        self.update_date_label(&widgets.date_label);
    }

    fn position(&self, _key: &factory::DynamicIndex) {}
}

impl List {
    fn update_date_label(&self, date_label: &gtk::Label) {
        if expired(&self.expiration) {
            date_label.remove_css_class("nearly-out-of-date");
            date_label.add_css_class("out-of-date");
        } else if nearly_expired(&self.expiration) {
            date_label.remove_css_class("out-of-date");
            date_label.add_css_class("nearly-out-of-date")
        } else {
            date_label.remove_css_class("out-of-date");
            date_label.remove_css_class("nearly-out-of-date");
        }
    }
}

fn expired(date: &glib::DateTime) -> bool {
    *date < floor_time(&glib::DateTime::now_local().unwrap())
}

// 1 week to expiry date.
fn nearly_expired(date: &glib::DateTime) -> bool {
    *date
        < floor_time(&glib::DateTime::now_local().unwrap())
            .add_weeks(1)
            .unwrap()
}

// Set time to zero and leave date.
fn floor_time(date: &glib::DateTime) -> glib::DateTime {
    glib::DateTime::new(
        &date.timezone(),
        date.year(),
        date.month(),
        date.day_of_month(),
        0,  // hour
        0,  // minute
        0., // seconds
    )
    .unwrap()
}
