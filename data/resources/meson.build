blueprints = custom_target('blueprints',
    input: [
        'ui/main_win.blp',
        'ui/list_row.blp'
    ],
    output: '.',
    command: [
        find_program('blueprint-compiler'),
        'batch-compile',
        '@OUTPUT@',
        '@CURRENT_SOURCE_DIR@',
        '@INPUT@'
    ],
)

resources = gnome.compile_resources(
    'expmgr',
    'expmgr.gresource.xml',
    dependencies: blueprints,
    gresource_bundle: true,
    source_dir: meson.current_build_dir(),
    install: true,
    install_dir: pkgdatadir,
)
