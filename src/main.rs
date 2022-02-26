mod app;
mod list;

fn main() {
    let model = app::AppModel::new();
    let app = relm4::RelmApp::new(model);

    app.run_with_args(&std::env::args().collect::<Vec<_>>());
}
