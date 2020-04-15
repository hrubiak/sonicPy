
import os.path, sys
from PyQt5 import QtWidgets
import copy
from PyQt5.QtCore import QThread, pyqtSignal
import time
from um.models.ScopeModel import Scope
from um.models.DPO5104 import Scope_DPO5104
import json
from um.widgets.scope_widget import scopeWidget

from um.widgets.panel import Panel
from functools import partial
from um.widgets.UtilityWidgets import save_file_dialog, open_file_dialog, open_files_dialog
from um.controllers.pv_controller import pvController
from utilities.utilities import *


class ScopeController(pvController):
    callbackSignal = pyqtSignal(dict)  
    stoppedSignal = pyqtSignal()
    dataUpdatedSignal = pyqtSignal(dict)
    dataBGUpdatedSignal = pyqtSignal(dict)
    runStateSignal = pyqtSignal(bool)

    def __init__(self, parent, isMain = False, offline = False):
        visa_hostname='143' 
        model = Scope_DPO5104(parent, visa_hostname=visa_hostname, offline = offline)
        super().__init__(parent, model, isMain) 
        
        self.panel_items =[ 'instrument',
                            'channel',
                            'vertical_scale',
                            'acquisition_type',
                            'num_av',
                            'num_acq',
                            'run_state',
                            'stop_after_num_av_preset']
        self.init_panel("Scope", self.panel_items)
        self.make_connections()
        #self.waveform_data = None
        #self.waveform_bg_data = None
        if isMain:
            self.show_widget()
        
    def channel_changed_callback(self, channel):
        panel_items =['channel_state',
                        'vertical_scale']
        for item in panel_items:
            self.model.pvs[item].get()
        
    def exit(self):
        self.model.exit()

    def make_connections(self):
        self.model.pvs['waveform'].value_changed_signal.connect(self.waveform_updated_signal_callback)
      
        self.model.pvs['channel'].value_changed_signal.connect(self.channel_changed_callback)
        self.model.pvs['run_state'].value_changed_signal.connect(self.run_state_callback)
        
    def run_state_callback(self, tag, data):
        state = data[0]
        #print('run state callback' + str(state))
        self.runStateSignal.emit(state)
        if state:
            self.get_waveform()
        else:
            self.stoppedSignal.emit()

   

    def bg_waveform_updated_signal_callback(self, pv_name, data):
        data = data[0]
        #self.waveform_bg_data = data
        self.dataBGUpdatedSignal.emit(data)

    def waveform_updated_signal_callback(self, pv_name, data):
        data = data[0]
        #self.waveform_data = data
        self.dataUpdatedSignal.emit(data)
        if self.model.pvs['run_state']._val:
            time.sleep(0.01)
            self.get_waveform()
            


    def get_waveform(self):
        if self.model.connected:
            self.model.pvs['waveform'].get()
        
        
    
    def show_widget(self):
        self.panel.raise_widget()