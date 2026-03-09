from bottle import static_file
from data.config import Config


def server_static(filename):
    return static_file(filename, root=Config.config.static_files_directory)


def server_script_component(filename):
    return static_file(filename, root=Config.config.static_files_directory+'/scripts/components')


def server_script(filename):
    return static_file(filename, root=Config.config.static_files_directory+'/scripts')


def index():
    return server_static('frontpage.htm')


def login():
    return server_static('login.htm')


def restricted_area():
    return server_static("restricted.htm")


def admin_area():
    return server_static("adminpage.htm")
