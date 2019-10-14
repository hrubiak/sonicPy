arb_waveforms = {'g_wavelet':{
                        'name': 'Gaussian wavelet',
                        'reference':'',
                        'comment':'',
                        'params':{ 
                        't_min':      {'symbol':u't<sub>0</sub>',
                                     'desc':u'Time min',
                                     'unit':u's',
                                     'default':-90e-9}, 
                        't_max':      {'symbol':u't<sub>max</sub>',
                                     'desc':u'Time max',
                                     'unit':u's',
                                     'default':90e-9}, 
                        'pts': {'symbol':"n",
                                     'desc':u'Number of points in waveform',
                                     'unit':u'',
                                     'default':1000}, 
                        'center_f': {'symbol':u'f<sub>0</sub>/dT',
                                     'desc':u'Center frequency',
                                     'unit':u'Hz',
                                     'default':45e6}, 
                        'sigma': {'symbol':u'σ',
                                     'desc':u"Half-width-half-max of the signal in the frequency domain",
                                     'unit':u'Hz',
                                     'default':20e6}
                        }}
}