project('expmgr', version: '0.0.1')

gnome = import('gnome')
python = import('python')
i18n = import('i18n')


app_id = 'com.example.expmgr'

dependency('glib-2.0')
dependency('gio-2.0')
dependency('gtk4')

glib_compile_resources = find_program('glib-compile-resources', required: true)
desktop_file_validate = find_program('desktop-file-validate', required: false)

prefix = get_option('prefix')
bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
pkgdatadir = datadir / meson.project_name()

pythondir = python.find_installation('python3').get_install_dir()
localedir = join_paths(prefix, get_option('localedir'))
iconsdir = datadir / 'icons'

install_subdir(meson.project_name(), install_dir: pythondir)
subdir('bin')
subdir('data')
subdir('po')
