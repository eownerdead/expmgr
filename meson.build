project('expmgr', version: '0.0.1')

gnome = import('gnome')
python = import('python')

base_id = 'com.example.expmgr'

dependency('glib-2.0')
dependency('gio-2.0')
dependency('gtk4')

glib_compile_resources = find_program('glib-compile-resources', required: true)

prefix = get_option('prefix')
bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
pkgdatadir = datadir / meson.project_name()
pythondir = python.find_installation('python3').get_install_dir()
localedir = join_paths(prefix, get_option('localedir'))

install_subdir(meson.project_name(), install_dir: pythondir)
subdir('bin')
subdir('data')
subdir('po')
