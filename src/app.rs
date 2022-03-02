use std::fs::{self, File};
use std::io::{self, Read, Write};
use std::path::PathBuf;
use std::str::FromStr;

use adw::prelude::*;
use gtk::glib;
use relm4::factory::{FactoryVecDeque, WeakDynamicIndex};
use relm4::{adw, gtk, send};
use toml_edit as toml;
use toml_edit::value;

use crate::list::List;

#[derive(Debug, Clone)]
pub(crate) enum AppMsg {
    Close,
    AddList,
    DelList(WeakDynamicIndex),
    Edit(WeakDynamicIndex),
    EndEdit(WeakDynamicIndex, List),
}

pub(crate) struct AppModel {
    pub(crate) list: FactoryVecDeque<List>,
}

impl relm4::Model for AppModel {
    type Components = ();
    type Msg = AppMsg;
    type Widgets = AppWidgets;
}

impl relm4::AppUpdate for AppModel {
    fn update(
        &mut self,
        msg: Self::Msg,
        _components: &Self::Components,
        _sender: relm4::Sender<Self::Msg>,
    ) -> bool {
        match msg {
            AppMsg::Close => self.save(),

            AppMsg::AddList => {
                self.list.push_back(List {
                    name: "".to_string(),
                    expiration: glib::DateTime::now_local().unwrap(),
                    editing: true,
                });
            }
            AppMsg::DelList(idx) => {
                let i = idx.upgrade().unwrap().current_index();

                self.list.remove(i);
            }
            AppMsg::Edit(idx) => {
                let i = idx.upgrade().unwrap().current_index();

                if let Some(pos) = self.list.iter().position(|i| i.editing) {
                    self.list.get_mut(pos).unwrap().editing = false;
                }
                self.list.get_mut(i).unwrap().editing = true;
            }
            AppMsg::EndEdit(idx, new) => {
                let i = idx.upgrade().unwrap().current_index();

                *self.list.get_mut(i).unwrap() = new;
                self.list.get_mut(i).unwrap().editing = false;
            }
        }

        true
    }
}

impl AppModel {
    pub fn new() -> Self {
        let mut a = Self { list: relm4::factory::FactoryVecDeque::new() };
        a.load();
        a
    }

    fn load(&mut self) {
        let mut s = String::new();
        match File::open(data_file_path()) {
            Ok(mut f) => {
                f.read_to_string(&mut s).unwrap();
            }
            Err(e) if e.kind() == io::ErrorKind::NotFound => {
                return; // Don't load.
            }
            Err(e) => {
                panic!("{}", e);
            }
        }

        let d = toml::Document::from_str(&s).unwrap();

        for (k, v) in d.iter() {
            self.list.push_back(List {
                name: k.to_string(),
                expiration: toml_to_glib_datetime(
                    v["expiration"].as_datetime().expect("expected datetime"),
                ),
                editing: false,
            })
        }
    }

    fn save(&self) {
        let mut d = toml::Document::new();

        for i in self.list.iter() {
            let expiration = glib_to_toml_datetime(&i.expiration);
            d[&i.name]["expiration"] = value(expiration);
        }

        fs::create_dir_all(data_file_path().parent().unwrap()).unwrap();
        write!(File::create(data_file_path()).unwrap(), "{}", d).unwrap();
    }
}

fn data_file_path() -> PathBuf {
    glib::user_data_dir().join("expmgr/data.toml")
}

// Convert only date.
pub(crate) fn glib_to_toml_datetime(from: &glib::DateTime) -> toml::Datetime {
    toml::Datetime {
        date: Some(toml::Date {
            year: from.year() as u16,
            month: from.month() as u8,
            day: from.day_of_month() as u8,
        }),
        time: None,
        offset: None,
    }
}

// Convert only date.
pub(crate) fn toml_to_glib_datetime(from: &toml::Datetime) -> glib::DateTime {
    let d = from.date.unwrap();

    glib::DateTime::from_local(
        d.year as i32,
        d.month as i32,
        d.day as i32,
        0,
        0,
        0.,
    )
    .unwrap()
}

#[relm4::widget(pub(crate))]
impl relm4::Widgets<AppModel, ()> for AppWidgets {
    view! {
        win = adw::ApplicationWindow {
            set_content: main_box = Some(&gtk::Box) {
                set_orientation: gtk::Orientation::Vertical,
                append = &adw::HeaderBar {
                    set_title_widget = Some(&gtk::Label) {
                        set_label: "ExpMgr",
                    },
                    pack_start = &gtk::Button {
                        set_icon_name: "list-add-symbolic",
                        connect_clicked(sender) => move |_| {
                            send!(sender, AppMsg::AddList);
                        }
                    },
                },
                append = &gtk::ScrolledWindow {
                    set_vexpand: true,
                    set_child = Some(&adw::Clamp) {
                        set_child = Some(&gtk::ListBox) {
                            add_css_class: "content",
                            set_margin_top: 12,
                            set_margin_bottom: 12,
                            set_margin_start: 12,
                            set_margin_end: 12,
                            factory!(model.list),
                        }
                    }
                }
            },
            connect_close_request(sender) => move |_| {
                send!(sender, AppMsg::Close);
                gtk::Inhibit(false)
            }
        }
    }
}
