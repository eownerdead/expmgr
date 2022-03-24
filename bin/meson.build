conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('PYTHONDIR', pythondir)
conf.set('APP_ID', app_id)
conf.set('VERSION', meson.project_version())
conf.set('LOCALEDIR', join_paths(prefix, localedir))
conf.set('PKGDATADIR', pkgdatadir)

configure_file(
    input: 'expmgr.in',
    output: 'expmgr',
    configuration: conf,
    install: true,
    install_dir: bindir,
)
