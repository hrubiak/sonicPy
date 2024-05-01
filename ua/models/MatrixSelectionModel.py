

#from ua.models.OverViewModel import Sort_Tuple
from utilities.utilities import *
from utilities.HelperModule import move_window_relative_to_screen_center, get_partial_index, get_partial_value
import numpy as np
from numpy import argmax, isin, nan, greater,less, append, sort, array, argmin


from scipy.signal import argrelextrema

import json, copy
#from ua.models.OverViewModel import OverViewModel

class dataPoints():
    def __init__(self, multiple_selection = False):
        self.file_matrix = [['']]
        self.file_exists_matrix = [[]]
        self.file_selected_matrix = [[]]
        self.multiple_selection = multiple_selection
    
    def clear(self):
        self.__init__(self.multiple_selection)
        
    def set_data_points(self, conditions, frequencies, file_dict):

        self.conditions = conditions
        self.frequencies = frequencies
        self.file_dict = file_dict
        file_matrix = [['']*len(frequencies)]*len(conditions)
        file_exists_matrix = [[False]*len(frequencies)]*len(conditions)
        file_selected_matrix = copy.deepcopy(file_exists_matrix)
        for fname in file_dict:
            cond = file_dict[fname][0]
            freq = file_dict[fname][1]
            file_matrix[conditions.index(cond)][frequencies.index(freq)] = fname
            if len(fname):
                if os.path.exists(fname):
                    file_exists_matrix[conditions.index(cond)][frequencies.index(freq)]=True
        
        self.file_matrix = file_matrix
        self.file_exists_matrix = np.asarray(file_exists_matrix)
        self.file_selected_matrix = np.asarray(file_selected_matrix)
        
    def get_selected(self):
        return self.file_selected_matrix==True

    def set_selected(self, freq, cond ):
        freq_ind = self.frequencies.index(freq)
        cond_ind = self.conditions.index(cond)
        file_exists = self.file_exists_matrix[cond_ind][freq_ind]
        if file_exists:
            if not self.multiple_selection:
                self.file_selected_matrix[:][:]=False
            self.file_selected_matrix[cond_ind][freq_ind]=True


class MatrixSelectionModel():
    def __init__(self ):
        
        self.data_points = dataPoints()
       
        self.plot_model = MatrixSelectionPlotModel()

    def clear(self):
        self.data_points.clear()

        self.plot_model.clear()


    def set_data(self, fps_cond:dict, fps_Hz:dict, file_dict):
        
        conditions = list( fps_cond.keys())
        frequencies = list( fps_Hz.keys())
        self.data_points.set_data_points(conditions,frequencies, file_dict)
        self.plot_model.clear()
        self.plot_model.set_data_points(self.data_points)

        
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

    def get_other_data_points(self):
        data_points = self.data_points
        xData = []
        yData = []
        frequencies = data_points.frequencies
        conditions = data_points.conditions

        return xData, yData

    def get_selected_data_point(self):
        
        xData = []
        yData = []
        frequencies = self.data_points.frequencies
        conditions = self.data_points.conditions
        selected_point = self.data_points.get_selected()

        
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
