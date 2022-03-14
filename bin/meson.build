conf = configuration_data()
conf.set('PYTHON', import('python').find_installation('python3').path())
conf.set('PYTHONDIR', pythondir)
conf.set('PKGDATADIR', pkgdatadir)

configure_file(
    input: 'expmgr.in',
    output: 'expmgr',
    configuration: conf,
    install: true,
    install_dir: bindir,
)
