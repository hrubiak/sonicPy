

from ua.models.OverViewModel import Sort_Tuple
from utilities.utilities import *
from utilities.HelperModule import move_window_relative_to_screen_center, get_partial_index, get_partial_value
import numpy as np
from numpy import argmax, isin, nan, greater,less, append, sort, array, argmin


from scipy.signal import argrelextrema

import json, copy
from ua.models.OverViewModel import OverViewModel

class dataPoints():
    def __init__(self, conditions, frequencies, files):
        
        self.conditions = conditions
        self.frequencies = frequencies
        
        self.init_data_points()
        
    def init_data_points(self):
        
        self.data_points={}
        self.selected_point = {}
        
    def get_selected_(self):
        return self.selected_point

    def set_selected(self, freq, cond ):
        pass

class MatrixSelectionModel():
    def __init__(self, overview_model: OverViewModel):
        self.overview_model = None
        self.data_points = None
        self.plot_model = MatrixSelectionPlotModel()

    def clear(self):
        self.__init__()

    def set_OverViewModel(self,  overview_model: OverViewModel):
        self.overview_model = overview_model
        conditions = overview_model.fps_cond
        frequencies = overview_model.fps_Hz
        files = overview_model.file_dict

        self.data_points = dataPoints(conditions, frequencies, files)
        
    def get_arrow_plot(self, cond, wave_type):
        return 1

    def refresh_all_freqs(self, condition,wave_type):
        pass

    def delete_freq(self, condition, wave_type, freq):
        pass

    def delete_cond(self, condition, wave_type, freq):
        pass

    def check_freq(self, condition, wave_type, freq):
        pass

    def check_cond(self, condition, wave_type, freq):
        pass

class MatrixSelectionPlotModel():
    def __init__(self):
        self.data_points = None

    def clear(self):
        self.__init__()
      
    def set_data_points(self, data_points:dataPoints):
        self.data_points = data_points

    def restore_results(self, package):
        pass

    def delete_optima(self, cond, freq):
        del self.optima[freq]

    def get_other_data_points(self, opt):
        optima = self.optima
        xData = []
        yData = []
        for freq in optima:
            pt  = optima[freq].other_opt[opt]
            for p in pt:
                xData.append(1/freq)
                yData.append(p)
        return xData, yData

    def get_selected_data_point(self, opt, ind=0):
        optima = self.optima
        xData = []
        yData = []
        for freq in optima:
            pt  = optima[freq].get_optimum(opt,ind)
            if pt is not None:
                xData.append(1/freq)
                yData.append(pt)
        return xData, yData
   
def interleave_lists(a_list, b_list):
    if isinstance(a_list, np.ndarray):
        a_list = list(a_list)
    if isinstance(b_list, np.ndarray):
        b_list = list(b_list)
    result = []
    while a_list and b_list:
        result.append(a_list.pop(0))
        result.append(a_list.pop(0))
        result.append(b_list.pop(0))
    result.extend(a_list)
    result.extend(b_list)
    return result
    

def read_result_file( filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data

def index_of_nearest(values, value):
    items = []
    for ind, v in enumerate(values):
        diff = abs(v-value)
        item = (diff, v, ind)
        items.append(item)
    def getKey(item):
        return item[0]
    s = sorted(items, key=getKey)
    closest = s[0][1]
    closest_ind = s[0][2]
    return closest_ind

def get_optima(xData,yData, optima_type=None):
    f = None
    if optima_type == 'min':
        f = less
    elif optima_type == 'max':
        f = greater
    if f is not None:
        optima_ind = argrelextrema(yData, f)
        optima_x = xData[optima_ind]
        optima_y = yData[optima_ind]
        return optima_x, optima_y
    return ([],[])

def get_local_optimum(x, xData, yData, optima_type=None):

    if len(xData) and len(yData):
        pind = get_partial_index(xData,x)
        if pind is None:
            return None
        pind1 = int(pind-100)
        pind2 = int(pind +100)
        xr = xData#[pind1:pind2]
        
        yr = yData#[pind1:pind2]
        # for local maxima
        maxima_ind = argrelextrema(yr, greater)
        maxima_x = xr[maxima_ind]
        maxima_y = yr[maxima_ind]

        minima_ind = argrelextrema(yr, less)
        minima_x = xr[minima_ind]
        minima_y = yr[minima_ind]

        if optima_type == 'minimum':
            optima_pind = index_of_nearest(minima_x,x)
            optima_x = minima_x[optima_pind]
            optima_x = array([optima_x])
            optima_y = array([minima_y[optima_pind]])

        if optima_type == 'maximum':
            optima_pind = index_of_nearest(maxima_x,x)
            optima_x = maxima_x[optima_pind]
            optima_x = array([optima_x])
            optima_y = array([maxima_y[optima_pind]])
        
        if optima_type is None:
            optima_ind = sort(append(maxima_ind, minima_ind))
            optima_x = xr[optima_ind]
            optima_y = yr[optima_ind]
            optima_pind = int(round(get_partial_index(optima_x,x)))
            optima_x = optima_x[optima_pind]
            if optima_x in minima_x:
                optima_type='minimum'
            if optima_x in maxima_x:
                optima_type='maximum'
            optima_x = array([optima_x])
            optima_y = array([optima_y[optima_pind]])
        return (optima_x, optima_y), optima_type
