
__version__ = "0.5.5"

import sys
import os


resources_path = os.path.join(os.path.dirname(__file__), 'resources')
print(resources_path)
calibrants_path = os.path.join(resources_path, 'calibrants')
devices_path = os.path.join(resources_path, 'devices')
icons_path = os.path.join(resources_path, 'icons')
data_path = os.path.join(resources_path, 'data')
style_path = os.path.join(resources_path, 'style')
env_path = os.path.join(resources_path, 'catch1d.env')
autosave_settings_path = os.path.join(resources_path, 'pv','autosave.json')
autosave_data_path = os.path.join(resources_path, 'pv','saved')

from pathlib import Path
home_path = str(Path.home())

import platform
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import pyqtgraph as pg

offline = False


scope_settings_file = os.path.normpath(os.path.join(devices_path,'scope.txt'))
if os.path.exists(scope_settings_file):
    with open(scope_settings_file, 'r') as file:
        # Read the first line into a variable
        scope_model = file.readline().strip()  # .strip() removes any leading/trailing whitespace, including newline characters

        # Read the second line into another variable
        scope_hostname = file.readline().strip()
        # Read the second line into another variable
        scope_offline_line = int(file.readline().strip() )
        scope_offline =  scope_offline_line != 0
else:
    scope_model = 'DPO'
    scope_hostname = '169'
    scope_offline = True
  
afg_settings_file = os.path.normpath(os.path.join(devices_path,'afg.txt'))
if os.path.exists(scope_settings_file):
    with open(afg_settings_file, 'r') as file:
        afg_model = file.readline().strip()  # .strip() removes any leading/trailing whitespace, including newline characters

        # Read the second line into another variable
        afg_hostname = file.readline().strip()
        # Read the second line into another variable
        afg_offline_line = int(file.readline().strip() )
        afg_offline =  afg_offline_line != 0
else:
    
    afg_model = 'AFG'
    afg_hostname = '202'
    afg_offline = True

def main():
    from um.controllers.UltrasoundController import UltrasoundController
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    _platform = platform.system()
    Theme = 1
    app = QtWidgets.QApplication([])
    #app.aboutToQuit.connect(app.deleteLater)
    controller = UltrasoundController(app, _platform, Theme, scope_offline, scope_model, scope_hostname, afg_offline, afg_model, afg_hostname)
    controller.show_window()

    if _platform == "Darwin":    #macOs has a 'special' way of handling preferences menu
        window = controller.display_window
        pact = QtWidgets.QAction('Preferences', app)
        pact.triggered.connect(controller.preferences_module)
        pact.setMenuRole(QtWidgets.QAction.PreferencesRole)
        pmenu = QtWidgets.QMenu('Preferences')
        pmenu.addAction(pact)
        menu = window.menuBar
        menu.addMenu(pmenu)
    
    app.exec_()
   
    #del app
