subdir('icons')
subdir('resources')

desktop_conf = configuration_data()
desktop_conf.set('ICON', app_id)
desktop_file = i18n.merge_file(
    type: 'desktop',
    input: configure_file(
        input: app_id + '.desktop.in.in',
        output: '@BASENAME@',
        configuration: desktop_conf
    ),
    output: app_id + '@0@.desktop',
    po_dir: '../po',
    install: true,
    install_dir: datadir / 'applications'
)

if desktop_file_validate.found()
    test(
        'Validate desktop file',
        desktop_file_validate,
        args: [desktop_file]
    )
endif
