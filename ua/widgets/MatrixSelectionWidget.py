#!/usr/bin/env python


import os, os.path, sys, platform, copy
from PyQt5 import uic, QtWidgets,QtCore
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox, QErrorMessage, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, Qt

import pyqtgraph as pg
from pyqtgraph import QtCore, mkPen, mkColor, hsvColor, ViewBox
from um.widgets.CustomWidgets import HorizontalSpacerItem, VerticalSpacerItem, FlatButton
import numpy as np

from um.widgets.PltWidget import SimpleDisplayWidget
from functools import partial

class MatrixSelectionWidget(QWidget):
    

    up_down_signal = pyqtSignal(str)
    panelClosedSignal = pyqtSignal()
    point_clicked_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.initialized = False
        self.t = None
        self.spectrum = None
        self.setWindowTitle('Data point selection matrix')
  
        self.make_widget()
        self.create_plots()
        self.style_widgets()

    def create_plots(self):
        self.plot_win = self.win.fig.win
        self.main_plot = pg.PlotDataItem([], [],
                        antialias=True, pen=None, symbolBrush=(255,0,100), symbolPen=None, symbolSize = 7, clickable=True)
        self.maximums = pg.PlotDataItem([], [],
                        antialias=True, pen=None, symbolBrush=(0,100,255), symbolPen=None, symbolSize = 7, clickable=True)
 
        
        self.main_plot.sigPointsClicked.connect(self.point_clicked)
        self.maximums.sigPointsClicked.connect(self.point_clicked)
   
        self.plot_win.addItem(self.main_plot)
    
        self.plot_win.addItem(self.maximums)

        

        # next lines are needed to create the legend items for the plot even though these plots are not the ones used
        # may change how this is done later
        
        self.plot_win.create_plots([],[],[],[],'Frequency')
        self.plot_win.set_colors( { 
                        'data_color': '#eeeeee',\
                        'rois_color': (0,255,100), \
                        })
        self.set_color((255,255,255,150), 2)

    def point_clicked(self, item, pt):
        print('pt ' + str(pt))
        point = [pt[0].pos().x(),pt[0].pos().y()]
        self.point_clicked_signal.emit(point)


    def update_view(self, xData, yData):
        
        if xData is not None and yData is not None:
            self.main_plot.setData(xData, yData)
    def update_maximums(self, xData, yData):
        
        if xData is not None and yData is not None:
            self.maximums.setData(xData, yData)

    def get_cursor_pos(self):
        return self.win.fig.win.get_cursor_pos()


    def set_selected_frequency (self, text):
        self. win.setText(text , 1)

    def set_color (self, color, ind):
        self. win. setColor (color , ind)

    def set_name (self, text):
        self. win.setText(text , 0)

    def set_result (self, text):
        self. win.setText(text , 2)
         
    def make_widget(self):
        my_widget = self
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.setContentsMargins(8, 5, 0, 0)

        self.label = QtWidgets.QLabel("Data point selection matrix")
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label.setStyleSheet('''font-size: 18pt;''')
        _layout.addWidget(self.label)
   
        params = "Arrow Plot", f'Condition', f'Frequency'
        self.win = SimpleDisplayWidget(params, update_cursor_on= False)
        self.win.update_diff_on = False
        
        _layout.addWidget(self.win)

        self.output_ebx = QtWidgets.QLineEdit('')

        my_widget.setLayout(_layout)
        

    def closeEvent(self, QCloseEvent, *event):
        self.panelClosedSignal.emit()
        super().closeEvent(QCloseEvent, *event)
        

    def keyPressEvent(self, e):
        event = None
        if e.key() == Qt.Key_Up:
            event = 'up'
        if e.key() == Qt.Key_Down:
            event = 'down'
        if event is not None:
            self.up_down_signal.emit(event)
        else:
            super().keyPressEvent(e)


    def style_widgets(self):
        
        self.setStyleSheet("""
            #scope_waveform_widget FlatButton {
                min-width: 70;
                max-width: 70;
            }
            #scope_waveform_widget QLabel {
                min-width: 110;
                max-width: 110;
            }
            #controls_sidebar QLineEdit {
                min-width: 120;
                max-width: 120;
            }
            #controls_sidebar QLabel {
                min-width: 110;
                max-width: 110;
            }
            
        """)
 

    def raise_widget(self):
        self.show()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()  




