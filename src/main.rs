mod app;
mod list;

fn main() {
    let model = app::AppModel::new();
    let app = relm4::RelmApp::new(model);

    relm4::set_global_css(include_bytes!("./app.css"));

    app.run_with_args(&std::env::args().collect::<Vec<_>>());
}
