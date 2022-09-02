
import os.path, sys, os
from functools import partial
from ua.models.EchoesResultsModel import EchoesResultsModel

class MultipleFrequenciesModel():
    def __init__(self, results_model: EchoesResultsModel):

        self.results_model = results_model
        self.cond = None
        self.files = {}
        self.fbase = None
        self.fname = ""

        self.f_min_sweep = None
        self.f_max_sweep = None

        self.f_min_broadband = None
        self.f_max_broadband = None
        self.step_broadband = 2

    def set_condition(self, cond):
        self.cond = cond

    def set_files(self, files):
        self.files = files

    def set_fbase(self, fbase):
        self.fbase = fbase
    
    def set_fname(self, fname):
        self.fname = fname


