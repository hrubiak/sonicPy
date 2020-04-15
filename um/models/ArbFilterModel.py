import os.path, sys
import numpy as np
from um.models.ScopeModel import Scope
from um.models.tek_fileIO import *
from utilities.utilities import *
import  logging, os, struct, sys
from um.models.PyTektronixScope import TektronixScope
from PyQt5.QtCore import QThread, pyqtSignal
import time
from datetime import datetime

import queue 
from functools import partial
import json
from um.models.pv_model import pvModel


class ArbFilterModel(Scope, pvModel):

    model_value_changed_signal = pyqtSignal(dict)

    def __init__(self, parent):
        
        pvModel.__init__(self, parent)
      
        
        self.instrument = 'ArbFilter'
        self.tasks = {  
                        'waveform_in':     
                                {'desc': 'Waveform in', 'val':None, 
                                'methods':{'set':True, 'get':True}, 
                                'param':{'tag':'waveform_in','type':'dict'}},
                        
                        'edit_state':     
                                {'desc': ';Edit', 'val':False, 
                                'methods':{'set':True, 'get':True}, 
                                'param':{'tag':'edit_state','type':'b'}},
                        'waveform_out':     
                                {'desc': 'Waveform out', 'val':None, 
                                'methods':{'set':True, 'get':True}, 
                                'param':{'tag':'waveform_out','type':'dict'}},
                        'filter_params':     
                                {'desc': 'Filter parameters', 'val':None, 
                                'methods':{'set':True, 'get':True}, 
                                'param':{'tag':'filter_params','type':'dict'}}
                                
                      }       

        
        self.create_pvs(self.tasks)

        self.start()


    
    #####################################################################
    #  Private set/get functions. Should not be used by external calls  #
    #####################################################################    

    def _exit_task(self):
        pass

 
    

    def _get_edit_state(self):
        ans = self.pvs['edit_state']._val
        #print('get ' + str(ans))
        return ans

    def _set_edit_state(self, param):
        #print('set ' + str(param))
        self.pvs['edit_state']._val= param