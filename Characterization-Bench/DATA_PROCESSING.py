# =============================================================================
# EXPERIMENTAL CONDITIONS
# =============================================================================

name = ''
nb = 1

lbd = 973e-9 #wavelength in m
I = 150 #intensity in mA
T = 25 #temperature in °C

ff_x_err = 30e-3 #uncertainty (u.a)
ff_y_err = 10e-1 #uncertainty(°)

nf_x_err = 30e-3 #uncertainty (u.a)
nf_y_err = 20e-2 #uncertainty(nm)

    #aff_err:
        #0: False
        #1: True
aff_err = 0

    #modelisation
        #0: Gaussian
        #1: Petermann II
modelisation = 1

    #mode:
        #0: Wavelength Spectrum
        #1: Light-Current-Voltage Characteristics
        #2: Far Field
        #3: Near Field
        #4: from Far Field to Near Field
        #5: from Near Field to Far Field
mode = 4

# =============================================================================
# MODULES
# =============================================================================

import os
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, peak_widths
import scipy.integrate as integrate

# =============================================================================
# FILES
# =============================================================================

def Files(nb):
    files_WS = []
    files_LIV = []
    files_FF = []
    files_NF = []

    for i in range(nb):
        files_WS.append(str("0_data/wavelength_spectrum%i.txt" %i))
        files_LIV.append(str("0_data/LIV%i.txt" %i))
        files_FF.append(str("0_data/far_field_fast_axis%i.txt" %i))
        files_FF.append(str("0_data/far_field_slow_axis%i.txt" %i))
        files_NF.append(str("0_data/near_field%i.csv" %i))

    return files_WS, files_LIV, files_FF, files_NF

    #Spectrum
Directory_WS = str("Wavelength Spectrum")
title_WS = str("%s Wavelength Spectrum {I=%imA, T=%i°C}" %(name, I, T))
file_WS = str("%s/Wavelength Spectrum.txt" %Directory_WS)
URL_WS = str("%s/Wavelength Spectrum.png" %Directory_WS)

    #Light-Current-Voltage Characteristics
Directory_LIV = str("Light-Current-Voltage Characteristics")
title_LIV = str("%s Light-Current-Voltage Characteristics {T=%i°C}" %(name, T))
file_LIV = str("%s/Light-Current-Voltage Characteristics.txt" %Directory_LIV)
URL_LIV = str("%s/Light-Current-Voltage Characteristics.png" %Directory_LIV)

    #Far Field
Directory_FF = str("Far Field")
title_FF = str("%s Far Field {I=%imA, T=%i°C}" %(name, I, T))
file_FF = str("%s/Far Field.txt" %Directory_FF)
URL_FF = str("%s/Far Field" %Directory_FF)

    #Near Field
Directory_NF = str("Near Field")
title_NF = str("%s Near Field {I=%imA, T=%i°C}" %(name, I, T))
file_NF = str("%s/Near Field.txt" %Directory_NF)
URL_NF = str("%s/Near Field" %Directory_NF)

    #From Far Field to Near Field
Directory_FFtoNF = str("From Far Field to Near Field")
title_FFtoNF = str("%s From Far Field to Near Field {I=%imA, T=%i°C}" %(name, I, T))
file_FFtoNF = str("%s/From Far Field to Near Field.txt" %Directory_FFtoNF)
URL_FFtoNF = str("%s/From Far Field to Near Field" %Directory_FFtoNF)

    #From Near Field to Far Field
Directory_NFtoFF = str("From Near Field to Far Field")
title_NFtoFF = str("%s From Near Field to Far Field {I=%imA, T=%i°C}" %(name, I, T))
file_NFtoFF = str("%s/From Near Field to Far Field.txt" %Directory_NFtoFF)
URL_NFtoFF = str("%s/From Near Field to Far Field" %Directory_NFtoFF)

# =============================================================================
# COMMON FUNCTION
# =============================================================================

err = [aff_err, ff_x_err, ff_y_err, nf_x_err, nf_y_err]

def Centre(data, index_maximum):
    '''centre the data around zero'''
    maximum = data[index_maximum]
    data_centre = []
    for i in range(len(data)):
        data_centre.append(data[i] - maximum)
    return data_centre

def Normalize(data):
    '''normalize the data between 0 and 1'''
    #data must be as np.array
    maximum = data.max()
    minimum = data.min()
    data_new = []
    for i in range(len(data)):
        data_new.append((data[i]-minimum)/(maximum-minimum))
    return np.array(data_new, dtype=float)

def GaussFunction(x, a, b, c):
    '''Gauss function'''
    return a*np.exp(-(x-b)**2/(2*c**2))

def FitGaussian(index, data):
    '''scipy module which can fit data'''
    #data must be as np.array
    mean = sum(index * data) / sum(data)
    sigma = np.sqrt(sum(data * (index - mean) ** 2) / sum(data))
    popt, pcov = curve_fit(GaussFunction, index, data, p0 = [1, mean, sigma])
    return popt, pcov, [mean, sigma]

def FWHM(data):
    '''scipy module which determine peaks and width'''
    peaks, _ = find_peaks(data)
        #width at 50%
    results_50 = peak_widths(data, peaks, rel_height=(1/2))
        #width at 13.5%
    results_13 = peak_widths(data, peaks, rel_height=(1-(1/np.exp(2))))
    return(peaks, results_50, results_13)

def SearchMax (data, len_file):
    '''find maximums values and indexes of those maximums'''
    #data must be as np.array
    max = data.max()
    max_indexes = np.where(data == max)
    maximum = data[max_indexes[0], max_indexes[1]][0]

    # along the maximum ligne
    index_ligne = np.arange(len(data[max_indexes[0]][0]))
    data_ligne = data[max_indexes[0]][0]

    # along the maximum column
    index_column = np.arange(len_file)
    data_column = []
    for i in range(len_file):
        data_column.append(data[i][max_indexes[1]][0])

    return data_ligne, data_column, index_ligne, index_column, maximum, max_indexes

# =============================================================================
# WAVELENGTH SPECTRUM
# =============================================================================

def OpenFileWS(chemin, mode):
    X = []
    Y = []
    file = open(chemin, mode)
    for data in file:
        data_replace = data.replace(",", ".")
        data_separate = data_replace.split("\t")
        X.append(float(data_separate[0]))
        Y.append(float(data_separate[1].strip()))
    return(X, Y)

def LoadDataWS(files):
    data = []
    for element in files:
        open_file = OpenFileWS(element,"r")
        data.append([open_file[0], open_file[1]])
    return(data)

def FindPeaksWS(data):
    maximum = []
    for i in range(len(data)):
        peaks, _ = find_peaks(data[i][1])
        maximum.append([])
        m = []
        while (len(maximum[i]) < 2):
            for nb in peaks:
                m.append(data[i][1][nb])
                mf = np.array(m, dtype=float)
                max = mf.max()
                max_indexes = np.where(mf == max)
            maximum[i].append(data[i][0][peaks[max_indexes[0][0]]])
            peaks = np.delete(peaks, max_indexes[0][0])
    return(maximum)

def NormalizeWS(data):
    data_new = []

    for i in range(nb):
        data_array = np.array(data[i][1])
        data_new.append([])
        for element in data_array :
            data_new[i].append(element-data_array.max())
    return(data_new)

def PlotWS(data, title, URL, nb):
    normalize_level = NormalizeWS(data)
    for i in range(nb):
        color = (random.random(), random.random(), random.random())
        peaks = FindPeaksWS(data)
        plt.plot(data[i][0], normalize_level[i], label='peak: %.2f' %peaks[i][0], color=color)
    plt.title(title)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Level (dB)")
    plt.legend()
    plt.savefig(URL, dpi=150)

###
if mode==0:
    if not os.path.exists(Directory_WS):
        os.mkdir(Directory_WS)
    data_WS = LoadDataWS(Files(nb)[mode])
    PlotWS(data_WS, title_WS, URL_WS, nb)
###

# =============================================================================
# LIGHT-CURRENT-VOLTAGE CHARACTERISTICS
# =============================================================================

def OpenFileLIV(chemin, mode):
    X = []
    Y1 = []
    Y2 = []
    file = open(chemin, mode)
    for data in file:
        data_replace = data.replace(",", ".")
        data_separate = data_replace.split("\t")
        X.append(float(data_separate[0]))
        Y1.append(float(data_separate[1]))
        Y2.append(float(data_separate[2].strip()))
    return(X, Y1, Y2)

def LoadDataLIV(files):
    data = []
    for element in files:
        data.append([OpenFileLIV(element,"r")[0], OpenFileLIV(element,"r")[1], OpenFileLIV(element,"r")[2]])
    return(data)

def PlotLIV(data, title, URL, nb):
    fig, axs = plt.subplots(2)
    fig.suptitle(title)

    for i in range(nb):
        color = (random.random(), random.random(), random.random())
        axs[0].plot(data[i][0], data[i][1], color=color)
        axs[1].plot(data[i][0], data[i][1], color=color)

    axs[0].set_ylabel("Output Power (mW)")
    axs[1].set_xlabel("Forward Current (mA)")
    axs[1].set_ylabel("Forward Voltage (V)")

    plt.savefig(URL, dpi=150)

###
if mode==1:
    if not os.path.exists(Directory_LIV):
        os.mkdir(Directory_LIV)
    data_LIV = LoadDataLIV(Files(nb)[mode])
    PlotLIV(data_LIV, title_LIV, URL_LIV, nb)
###

# =============================================================================
# FAR FIELD ANALYSIS
# =============================================================================

def OpenFileFF(chemin):
    '''open and read document for Far Field'''
    X = [] #theta
    Y = [] #I
    file = open(chemin, 'r')
    for data in file:
        data_replace = data.replace(",", ".")
        data_separate = data_replace.split("\t")
        X.append(float(data_separate[0])) #firt column
        Y.append(float(data_separate[3].strip())) #third column : THIS VALUE MIGHT CHANGE
    file.close()
    return X, Y

def LoadDataFF(files):
    '''generate a list of all data for Far Field'''
    data = []
    for element in files: #Fast Axis then Slow Axis
        data.append([OpenFileFF(element)[0], OpenFileFF(element)[1]])
    #data = [[first document : [fast axis, slow axis]], [second document[...], ...]]
    return data

def PlotFF(data, title, name, err, nb):
    '''plot Far Field analysis : fast axis and slow axis on the same plot'''
        #value at 50%
    # resultat_FA = FWHM(GaussFunction(np.array(data[i][0], dtype=float), *FitGaussian(np.array(data[i][0], dtype=float)[0], np.array(data[i][1], dtype=float))))[1][0][0]
    # resultat_SA = FWHM(GaussFunction(np.array(data[i+1][0], dtype=float), *FitGaussian(np.array(data[i+1][0], dtype=float)[0], np.array(data[i+1][1], dtype=float))))[1][0][0]

    x0_min = np.array(data[0][0],dtype=float).min()
    x0_max = np.array(data[0][0],dtype=float).max()
    x1_min = np.array(data[1][0],dtype=float).min()
    x1_max = np.array(data[1][0],dtype=float).max()
    y0_min = np.array(data[0][1],dtype=float).min()
    y0_max = np.array(data[0][1],dtype=float).max()
    y1_min = np.array(data[1][1],dtype=float).min()
    y1_max = np.array(data[1][1],dtype=float).max()

    for i in range(0, 2*nb, 2):

        if nb > 1:
            color_0 = (random.random(), random.random(), random.random())
            color_1 = color_0
        else:
            color_0 = 'blue'
            color_1 = 'red'

            #Fast Axis
        x0 = np.array(data[i][0],dtype=float)
        if (x0.min() < x0_min): x0_min = x0.min()
        if (x0.max() > x0_max): x0_max = x0.max()
        y0 = np.array(data[i][1], dtype=float)
        x0_centre = Centre(x0, np.where(y0 == y0.max())[0])
        y0_normalize = Normalize(y0)
        if (y0_normalize.min() < y0_min): y0_min = y0_normalize.min()
        if (y0_normalize.max() > y0_max): y0_max = y0_normalize.max()
        plt.plot(x0_centre, y0_normalize, linestyle = ':', color=color_0, label='Fast Axis')
        if err[0]:
            plt.errorbar(x0_centre, y0_normalize, err[1], err[2])

            #fitted Fast Axis
        x0_fit = np.array(data[i][0],dtype=float)
        y0_fit = GaussFunction(x0_fit, *FitGaussian(x0_fit, data[i][1])[0])
        x0_centre_fit = Centre(x0_fit, np.where(y0_fit == y0_fit.max())[0])
        y0_fit_normalize = Normalize(y0_fit)
        plt.plot(x0_centre_fit, y0_fit_normalize, linestyle = '-', color=color_0)
        # plt.text(0, 0.05, 'Fast Axis FWHM: %.2f' %(resultat_FA), backgroundcolor='k', color='w')

            #Slow Axis
        x1 = np.array(data[i+1][0],dtype=float)
        if (x1.min() < x1_min): x1_min = x1.min()
        if (x1.max() < x1_max): x1_max = x1.max()
        y1 = np.array(data[i+1][1], dtype=float)
        x1_centre = Centre(x1, np.where(y1 == y1.max())[0])
        y1_normalize = Normalize(y1)
        if (y1_normalize.min() < y1_min): y1_min = y1_normalize.min()
        if (y1_normalize.max() > y1_max): y1_max = y1_normalize.max()
        plt.plot(x1, y1_normalize, linestyle = ':', color=color_1, label='Slow Axis')
        if err[0]:
            plt.errorbar(x1_centre, y1_normalize, err[1], err[2])

            #fitted Slow Axis
        x1_fit = np.array(data[i+1][0],dtype=float)
        y1_fit = GaussFunction(x1_fit, *FitGaussian(x1_fit, data[i+1][1])[0])
        x1_centre_fit = Centre(x1_fit, np.where(y1_fit == y1_fit.max())[0])
        y1_fit_normalize = Normalize(y1_fit)
        plt.plot(x1_centre_fit, y1_fit_normalize, linestyle = '-', color=color_1)
        # plt.text(0, 0, 'Slow Axis FWHM: %.2f'%(resultat_SA), backgroundcolor='k', color='w')

    plt.title('Fast Axis : x axis, Slow Axis : y axis')
    plt.legend(title=': data\n- fit')
    plt.xlim([min(x0_min, x1_min), max(x0_max, x1_max)])
    plt.ylim([min(y0_min, y1_min), max(y0_max, y1_max)])
    plt.xlabel('Beam Divergence (°)')
    plt.ylabel('Normalize Intensity (a.u)')

    if err[0]:
        plt.savefig(name+' error bar.png', dpi=150)
    else:
        plt.savefig(name+'.png', dpi=150)

def PrintFF(file, data, title, nb):
    file = open(file,"w")
    file.writelines(title)

    for i in range(0, 2*nb, 2):
        resultat_FA = FWHM(GaussFunction(np.array(data[i][0], dtype=float), *FitGaussian(np.array(data[i][0], dtype=float), np.array(data[i][1], dtype=float))[0]))[1][0][0]
        resultat_SA = FWHM(GaussFunction(np.array(data[i+1][0], dtype=float), *FitGaussian(np.array(data[i+1][0], dtype=float), np.array(data[i+1][1], dtype=float))[0]))[1][0][0]
        file.writelines('\n\nFast Axis FWHM: %.2f°' %(resultat_FA))
        file.writelines('\nSlow Axis FWHM: %.2f°' %(resultat_SA))

        fit_parameters = FitGaussian(np.array(data[i][0], dtype=float), np.array(data[i][1], dtype=float))
        file.writelines('\n\nGaussian fit parameters (Fast Axis) [a, b, c]: %s' %(fit_parameters[0]))

        fit_parameters = FitGaussian(np.array(data[i+1][0], dtype=float), np.array(data[i+1][1], dtype=float))
        file.writelines('\nGaussian fit parameters (Slow Axis) [a, b, c]: %s' %(fit_parameters[0]))

    file.close()

###
if mode==2:
    if not os.path.exists(Directory_FF):
        os.mkdir(Directory_FF)
    data_FF = LoadDataFF(Files(nb)[mode])
    PlotFF(data_FF, title_FF, URL_FF, err, nb)
    PrintFF(file_FF, data_FF, title_FF, nb)
###

# =============================================================================
# NEAR FIELD ANALYSIS
# =============================================================================

def OpenFileNF (chemin, mode):
    '''open and read document for Near Field'''
        #HOW TO DO ?
            #Software used BeamMic : https://www.ophiropt.com/laser--measurement/software-download
            #data acquisition
            #then extractct it in 2D ASCII format (.csv)
    len_file = 0
    data_separate = []
    data_clear = []
    file = open(chemin, mode)
    for data in file:
        data_separate.append(data.split(";"))
        len_file += 1
    for element in data_separate:
        data_clear.append(element[:-1])
        data_done = np.array(data_clear, dtype=float)
    file.close()
    return data_done, len_file

def Conversion (data, mode):
    '''Camera conversion process'''
    #CAMERA : SP503U-1550
    #data is int indexes
        # Conversion pixel into mm
    active_area_ligne = 6.3e-3 # m
    effective_pixels_ligne = 640 # pixels
    active_area_column = 4.7e-3 # m
    effective_pixels_column = 480 # pixels
    conversion_ligne = active_area_ligne/effective_pixels_ligne
    conversion_column = active_area_column/effective_pixels_column

        #data exctrated from BeamMic is ten to the fourth meter IN THIS CASE
            # It is easy to check : read the unit and the power of ten of D4_sigma
        #one half is for the centered data

    if (mode=="ligne"):
        ligne = data*conversion_ligne*1e4*(1/2)
        return ligne
    elif (mode=="column"):
        column = data*conversion_column*1e4*(1/2)
        return column

def ConversionCentre (data, index_maximum, mode):
    '''centre + conversion process'''
    if (mode=="ligne"):
        ligne_convert = Conversion(data, mode)
        ligne = Centre(ligne_convert, index_maximum)
        return ligne
    elif (mode=="column"):
        column_convert = Conversion(data, mode)
        column = Centre(column_convert, index_maximum)
        return column

def LoadDataNF(file):
    '''generate a list of all data for Near Field'''
    i = 0
    data, len_data, all_data, index, maximum, max_indexes, conversion, conversion_centre, fit_gauss, peaks, FWHM_data = [], [], [], [], [], [], [], [], [], [], []
    for element in file:

        open_file = OpenFileNF(element,"r")
        data.append(open_file[0])
        len_data.append(open_file[1])

        search_max = SearchMax(data[i], len_data[i])
        all_data.append([search_max[0], search_max[1]])
        index.append([search_max[2], search_max[3]])
        maximum.append(search_max[4])
        max_indexes.append(search_max[5])

        conversion.append([Conversion(index[i][0], "ligne"),
                           Conversion(index[i][1], "column")])

        fit_gauss.append([FitGaussian(conversion[i][0], all_data[i][0])[0],
                          FitGaussian(conversion[i][1], all_data[i][1])[0]])

        #maximum values
        peaks.append([FWHM(GaussFunction(conversion[i][0], *fit_gauss[i][0]))[0],
                      FWHM(GaussFunction(conversion[i][1], *fit_gauss[i][1]))[0]])

        #13.5% values
            #1: 50%
            #2: 13.5%
        FWHM_data.append([Conversion(FWHM(GaussFunction(conversion[i][0], *fit_gauss[i][0]))[2][0][0], "ligne"),
                          Conversion(FWHM(GaussFunction(conversion[i][1], *fit_gauss[i][1]))[2][0][0], "column")])


        conversion_centre.append([ConversionCentre(index[i][0],
                                                   FWHM(GaussFunction(conversion[i][0],
                                                                      *fit_gauss[i][0]))[0][0],
                                                   "ligne"),
                                  ConversionCentre(index[i][1],
                                                   FWHM(GaussFunction(conversion[i][1],
                                                                      *fit_gauss[i][1]))[0][0],
                                                   "column")])

        i += 1

    return (data, len_data, all_data, index, maximum,
           conversion, conversion_centre, fit_gauss,
           peaks, FWHM_data)

def PlotNF(name, title, data, err, nb):
    '''plot Near Field analysis : fast axis and slow axis on two disctinct plot'''

    x0_min = Normalize(np.array(data[6][0][0],dtype=float)).min()
    x0_max = Normalize(np.array(data[6][0][0],dtype=float)).max()
    x1_min = Normalize(np.array(data[6][0][1],dtype=float)).min()
    x1_max = Normalize(np.array(data[6][0][1],dtype=float)).max()
    y0_min = Normalize(np.array(data[2][0][0],dtype=float)).min()
    y0_max = Normalize(np.array(data[2][0][0],dtype=float)).max()
    y1_min = Normalize(np.array(data[2][0][1],dtype=float)).min()
    y1_max = Normalize(np.array(data[2][0][1],dtype=float)).max()

    for i in range(nb):

        if nb > 1:
            color_0 = (random.random(), random.random(), random.random())
            color_1 = color_0
        else:
            color_0 = 'blue'
            color_1 = 'red'

        # resultat_FA = data[9][i][0]
        # resultat_SA = data[9][i][1]

            #Fast Axis
        x0 = np.array(data[6][i][0],dtype=float)
        if (x0.min() < x0_min): x0_min = x0.min()
        if (x0.max() > x0_max): x0_max = x0.max()
        y0 = np.array(data[2][i][0], dtype=float)
        y0_normalize = Normalize(y0)
        if (y0_normalize.min() < y0_min): y0_min = y0_normalize.min()
        if (y0_normalize.max() > y0_max): y0_max = y0_normalize.max()
        plt.plot(x0, y0_normalize, linestyle = ':', color=color_0, label='Fast Axis')
        if err[0]:
            plt.errorbar(x0, y0_normalize, err[3], err[4])

            #fitted Fast Axis
        x0_fit = np.array(data[6][i][0],dtype=float)
        y0_fit = GaussFunction(data[5][i][0], *data[7][i][0])
        y0_fit_normalize = Normalize(y0_fit)
        plt.plot(x0_fit, y0_fit_normalize, linestyle = '-', color=color_0)
        # plt.text(2.5, 0, '1/e^2: %.2f µm' %(resultat_FA), backgroundcolor='k', color='w')

            #Slow Axis
        x1 = np.array(data[6][i][1],dtype=float)
        if (x1.min() < x1_min): x1_min = x1.min()
        if (x1.max() < x1_max): x1_max = x1.max()
        y1 = np.array(data[2][i][1], dtype=float)
        y1_normalize = Normalize(y1)
        if (y1_normalize.min() < y1_min): y1_min = y1_normalize.min()
        if (y1_normalize.max() > y1_max): y1_max = y1_normalize.max()
        plt.plot(x1, y1_normalize, linestyle = ':', color=color_1, label='Slow Axis')
        if err[0]:
            plt.errorbar(x1, y1_normalize, err[3], err[4])

            #fitted Slow Axis
        x1_fit = np.array(data[6][i][1],dtype=float)
        y1_fit = GaussFunction(data[5][i][1], *data[7][i][1])
        y1_fit_normalize = Normalize(y1_fit)
        plt.plot(x1_fit, y1_fit_normalize, linestyle = '-', color=color_1)
        # plt.text(2.5, 0, '1/e^2: %.2f µm' %(resultat_SA), backgroundcolor='k', color='w')

    plt.title('Fast Axis : x axis, Slow Axis : y axis')
    plt.legend(title=': data\n- fit')
    plt.xlim([min(x0_min, x1_min), max(x0_max, x1_max)])
    plt.ylim([min(y0_min, y1_min), max(y0_max, y1_max)])
    plt.xlabel('Latteral Position (µm)')
    plt.ylabel('Normalize Light Intensity (a.u)')

    if err[0]:
        plt.savefig(name+' error bar.png', dpi=150)
    else:
        plt.savefig(name+'.png', dpi=150)

def PrintNF(file, data, title, nb):
    file = open(file,"w")
    file.writelines(title)

    for i in range(nb):
        resultat_FA = data[9][i][1]
        resultat_SA = data[9][i][0]
        file.writelines('\n\nFast Axis 1/e^2: %.2fµm' %(resultat_FA))
        file.writelines('\nSlow Axis 1/e^2: %.2fµm' %(resultat_SA))

        fit_parameters_fa = FitGaussian(data[6][i][1], Normalize(np.array(data[2][i][1], dtype=float)))
        param = [fit_parameters_fa[2][0], 2*fit_parameters_fa[2][1]]
        file.writelines('\n\nNormal distribution fit parameters (Fast Axis) [mean, sigma]: %s' %(param))

        fit_parameters_sa = FitGaussian(data[6][i][0], Normalize(np.array(data[2][i][0], dtype=float)))
        param = [fit_parameters_sa[2][0], 2*fit_parameters_sa[2][1]]
        file.writelines('\nNormal distribution fit parameters (Slow Axis) [mean, sigma]: %s' %(param))

    file.close()

###
if mode==3:
    if not os.path.exists(Directory_NF):
        os.mkdir(Directory_NF)
    data_NF = LoadDataNF(Files(nb)[mode])
    PlotNF(URL_NF, title_NF, data_NF, err, nb)
    PrintNF(file_NF, data_NF, title_NF, nb)
###

# =============================================================================
# THEORY
# =============================================================================

def f0(a, x):
    #I(theta)*sin(theta)*cos(theta)
    return a*np.sin(x)*np.cos(x)

def f1(a, x):
    #I(theta)*sin^3(theta)*cos(theta)
    return a*((np.sin(x))**3)*np.cos(x)

def Gaussian(data, lbd, axis):
    theta_FF = FWHM(GaussFunction(np.array(data[0], dtype=float), *FitGaussian(np.array(data[0], dtype=float), np.array(data[1], dtype=float))[0]))[1][0][0]
    omega_0_gauss = lbd/(np.pi*(theta_FF*(np.pi/180)))
    print(omega_0_gauss)
    if axis==0:
        return omega_0_gauss
    else:
        return 10*omega_0_gauss

def Petermann(data, lbd, axis):
    theta_r = []
    for theta_d in data[0]:
        theta_r.append(theta_d*(np.pi/180)) #degree into radian conversion coef

    y0 = f0(data[1], theta_r)
    I0 = sum(integrate.cumtrapz(y0, theta_r))

    y1 = f1(data[1], theta_r)
    I1 = sum(integrate.cumtrapz(y1, theta_r))

    petermann = (lbd/2*np.pi)*np.sqrt((2*I0)/I1)
    if axis==0:
        print((1/4)*petermann)
        return (1/2)*petermann
    else:
        print((1/4)*petermann)
        return (1/2)*petermann

def BeamRadius(MFD, z, lbd):
    z_R = (np.pi/lbd)*(MFD/2)**2 #Rayleigh range
    omega = (MFD/2)*np.sqrt(1+((z/z_R)**2)) #Beam radius at distance z
    return omega

def IntensityR(data, lbd, list_r, modelisation, axis):
    if modelisation == 0:
        MFD = Gaussian(data, lbd, axis)
    if modelisation == 1:
        MFD = Petermann(data, lbd, axis)
    omega = 0.5*BeamRadius(MFD, 0, lbd)
    I = []
        #[r] = µm
        #[omega] = m
    for r in list_r:
        I.append((2/(np.pi*omega**2))*np.exp(-2*(r*1e-6/omega)**2))
    return I

def IntensityT(omega_0, lbd, list_t):
    #[omega_0] = µm
    theta_0 = lbd/(np.pi*omega_0*1e-6)
    I=[]
    for t in list_t:
        t = t*(np.pi/180)
        I.append(np.exp(-2*((np.sin(t))**2)/((np.sin(theta_0))**2)))
    return I

def PlotFFtoNF(dataFF, dataNF, lbd, name, title, nf_fa, nf_sa, ff_fa, ff_sa, err, nb, modelisation):
    '''plot Near Field analysis : fast axis and slow axis on two disctinct plot'''

    x0_min = Normalize(np.array(dataNF[6][0][0],dtype=float)).min()
    x0_max = Normalize(np.array(dataNF[6][0][0],dtype=float)).max()
    x1_min = Normalize(np.array(dataNF[6][0][1],dtype=float)).min()
    x1_max = Normalize(np.array(dataNF[6][0][1],dtype=float)).max()
    y0_min = Normalize(np.array(dataNF[2][0][0],dtype=float)).min()
    y0_max = Normalize(np.array(dataNF[2][0][0],dtype=float)).max()
    y1_min = Normalize(np.array(dataNF[2][0][1],dtype=float)).min()
    y1_max = Normalize(np.array(dataNF[2][0][1],dtype=float)).max()

    i_ff = 0
    for i_nf in range(nb):

        for i in range(nb):

            if nb > 1:
                color_0 = (random.random(), random.random(), random.random())
                color_1 = color_0
            else:
                color_0 = 'blue'
                color_1 = 'red'

        # resultat_FA = dataNF[9][i_nf][nf_fa]
        # resultat_SA = dataNF[9][i_nf][nf_sa]
        # resultat_FA_theory = Petermann(dataFF[i_ff+ff_fa], lbd)*1e6
        # resultat_SA_theory = Petermann(dataFF[i_ff+ff_sa], lbd)*1e6

        fig, axs = plt.subplots(2, 1, figsize=(8, 6))
        if modelisation == 0:
            titlef = title+' Gauss modelisation'
        else:
           titlef = title+' PetermannII modelisation'
        fig.suptitle(titlef)

            #Fast Axis
        x0 = np.array(dataNF[6][i_nf][nf_fa], dtype=float)
        if (x0.min() < x0_min): x0_min = x0.min()
        if (x0.max() > x0_max): x0_max = x0.max()
        y0 = np.array(dataNF[2][i_nf][nf_fa], dtype=float)
        y0_normalize = Normalize(y0)
        if (y0_normalize.min() < y0_min): y0_min = y0_normalize.min()
        if (y0_normalize.max() > y0_max): y0_max = y0_normalize.max()
        axs[0].plot(x0, y0_normalize, linestyle = ':', color=color_0)
        if err[0]:
            axs[0].errorbar(x0, y0_normalize, err[3], err[4])

            #fitted Fast Axis
        x0_fit = np.array(dataNF[6][i_nf][nf_fa], dtype=float)
        y0_fit = GaussFunction(dataNF[5][i_nf][nf_fa], *dataNF[7][i_nf][nf_fa])
        y0_fit_normalize = Normalize(y0_fit)
        axs[0].plot(x0_fit, y0_fit_normalize, linestyle = '-', color=color_0)
        # axs[0].text(2.0, 0.2, '1/e^2: %.2f µm' %(resultat_FA), backgroundcolor='k', color='w')

            #theory Fast Axis
        x0_theory = np.array(dataNF[6][i_nf][nf_fa], dtype=float)
        y0_theory = np.array(IntensityR(dataFF[i_ff+ff_fa], lbd, dataNF[6][i_nf][nf_fa], modelisation, 0), dtype=float)
        y0_theory_normalize = Normalize(y0_theory)
        axs[0].plot(x0_theory, y0_theory_normalize, linestyle = '-.', color=color_0)
        # axs[0].text(2.0, 0.0, '1/e^2 theory: %.2f µm' %(resultat_FA_theory), backgroundcolor='k', color='w')

            #Slow Axis
        x1 = np.array(dataNF[6][i_nf][nf_sa], dtype=float)
        if (x1.min() < x1_min): x1_min = x1.min()
        if (x1.max() < x1_max): x1_max = x1.max()
        y1 = np.array(dataNF[2][i_nf][nf_sa], dtype=float)
        y1_normalize = Normalize(y1)
        if (y1_normalize.min() < y1_min): y1_min = y1_normalize.min()
        if (y1_normalize.max() > y1_max): y1_max = y1_normalize.max()
        axs[1].plot(x1, y1_normalize, linestyle = ':', color=color_1)
        if err[0]:
            axs[1].errorbar(x1, y1_normalize, err[3], err[4])

            #fitted Slow Axis
        x1_fit = np.array(dataNF[6][i_nf][nf_sa], dtype=float)
        y1_fit = GaussFunction(dataNF[5][i_nf][nf_sa], *dataNF[7][i_nf][nf_sa])
        y1_fit_normalize = Normalize(y1_fit)
        axs[1].plot(x1_fit, y1_fit_normalize, linestyle = '-', color=color_1)
        # axs[1].text(2.0, 0.2, '1/e^2: %.2f µm' %(resultat_SA), backgroundcolor='k', color='w')

            #theory Slow Axis
        x1_theory = np.array(dataNF[6][i_nf][nf_sa], dtype=float)
        y1_theory = np.array(IntensityR(dataFF[i_ff+ff_sa], lbd, dataNF[6][i_nf][nf_sa], modelisation, 1), dtype=float)
        y1_theory_normalize = Normalize(y1_theory)
        axs[1].plot(x1_theory, y1_theory_normalize, linestyle = '-.', color=color_1)
        # axs[1].text(2.0, 0.0, '1/e^2 theory: %.2f µm' %(resultat_SA_theory), backgroundcolor='k', color='w')

        i_ff += 2

    axs[0].set_title('Fast Axis : y  axis')
    axs[0].legend(title=':data\n: fit\n-. modelisation')
    axs[0].set_xlim([min(x0_min, x1_min), max(x0_max, x1_max)])
    axs[0].set_ylim([min(y0_min, y1_min), max(y0_max, y1_max)])
    axs[1].set_title('Slow Axis : x axis')
    axs[1].legend(title=':data\n: fit\n-. modelisation')
    axs[1].set_xlim([min(x0_min, x1_min), max(x0_max, x1_max)])
    axs[1].set_ylim([min(y0_min, y1_min), max(y0_max, y1_max)])

    fig.text(0.5, 0.04, 'Latteral Position (µm)', ha='center', va='center')
    fig.text(0.06, 0.5, 'Normalize Light Intensity (a.u)', ha='center', va='center', rotation='vertical')

    if modelisation == 0:
        namef = name+' Gauss'
    else:
        namef = name+' PetermannII'
    if err[0]:
        plt.savefig(namef+' error bar.png', dpi=150)
    else:
        plt.savefig(namef+'.png', dpi=150)

def PlotNFtoFF(dataFF, dataNF, lbd, name, title, nf_fa, nf_sa, ff_fa, ff_sa, err, nb):
    '''plot Far Field analysis : fast axis and slow axis on the same plot'''

        #value at 50%
    # resultat_FA = FWHM(GaussFunction(np.array(dataFF[i+ff_fa][0], dtype=float), *FitGaussian(np.array(dataFF[i+ff_fa][0], dtype=float)[0], np.array(dataFF[i+ff_fa][1], dtype=float))))[1][0][0]
    # resultat_SA = FWHM(GaussFunction(np.array(dataFF[i+ff_sa][0], dtype=float), *FitGaussian(np.array(dataFF[i+ff_sa][0], dtype=float)[0], np.array(dataFF[i+ff_sa][1], dtype=float))))[1][0][0]
    # resultat_FA_theory = FWHM(IntensityT(dataNF[9][i][nf_fa], lbd, dataFF[i+ff_fa][0]))[1][0][0]
    # resultat_SA_theory = FWHM(IntensityT(dataNF[9][i][nf_sa], lbd, dataFF[i+ff_sa][0]))[1][0][0]

    fig, axs = plt.subplots(2, 1, figsize=(8, 6))
    fig.suptitle(title)

    x0_min = np.array(dataFF[0][0],dtype=float).min()
    x0_max = np.array(dataFF[0][0],dtype=float).max()
    x1_min = np.array(dataFF[1][0],dtype=float).min()
    x1_max = np.array(dataFF[1][0],dtype=float).max()
    y0_min = np.array(dataFF[0][1],dtype=float).min()
    y0_max = np.array(dataFF[0][1],dtype=float).max()
    y1_min = np.array(dataFF[1][1],dtype=float).min()
    y1_max = np.array(dataFF[1][1],dtype=float).max()

    i_ff = 0
    for i_nf in range(nb):

        for i in range(nb):

            if nb > 1:
                color_0 = (random.random(), random.random(), random.random())
                color_1 = color_0
            else:
                color_0 = 'blue'
                color_1 = 'red'

            #Fast Axis
        x0 = np.array(dataFF[i_ff+ff_fa][0],dtype=float)
        if (x0.min() < x0_min): x0_min = x0.min()
        if (x0.max() > x0_max): x0_max = x0.max()
        y0 = np.array(dataFF[i_ff+ff_fa][1], dtype=float)
        y0_normalize = Normalize(y0)
        x0_centre = Centre(x0, np.where(y0 == y0.max())[0])
        if (y0_normalize.min() < y0_min): y0_min = y0_normalize.min()
        if (y0_normalize.max() > y0_max): y0_max = y0_normalize.max()
        axs[0].plot(x0_centre, y0_normalize, linestyle = ':', color=color_0)
        if err[0]:
            axs[0].errorbar(x0_centre, y0_normalize, err[1], err[2])

            #fitted Fast Axis
        x0_fit = np.array(dataFF[i_ff+ff_fa][0],dtype=float)
        y0_fit = GaussFunction(x0_fit, *FitGaussian(x0_fit, dataFF[i_ff+ff_fa][1])[0])
        x0_centre_fit = Centre(x0_fit, np.where(y0_fit == y0_fit.max())[0])
        y0_fit_normalize = Normalize(y0_fit)
        axs[0].plot(x0_centre_fit, y0_fit_normalize, linestyle = '-', color=color_0)
        # axs[0].text(dataFF[i_ff][0][0]-3, 1-0.0, 'Fast Axis FWHM: %.2f' %(resultat_FA), backgroundcolor='k', color='w')

            #theory Fast Axis
        x0_theory = np.array(dataFF[i_ff+ff_fa][0], dtype=float)
        y0_theory = np.array(IntensityT(dataNF[9][i_nf][nf_fa], lbd, dataFF[i_ff+ff_fa][0]), dtype=float)
        x0_centre_theory = Centre(x0_theory, np.where(y0_theory == y0_theory.max())[0])
        y0_theory_normalize = Normalize(y0_theory)
        axs[0].plot(x0_centre_theory, y0_theory_normalize, linestyle = '-.', color=color_0)
        # axs[0].text(dataFF[i_ff][0][0]-3, 1-0.15, 'Fast Axis FWHM theory: %.2f' %(resultat_FA_theory), backgroundcolor='k', color='w')

            #Slow Axis
        x1 = np.array(dataFF[i_ff+ff_sa][0],dtype=float)
        if (x1.min() < x1_min): x1_min = x1.min()
        if (x1.max() < x1_max): x1_max = x1.max()
        y1 = np.array(dataFF[i_ff+ff_sa][1], dtype=float)
        x1_centre = Centre(x1, np.where(y1 == y1.max())[0])
        y1_normalize = Normalize(y1)
        if (y1_normalize.min() < y1_min): y1_min = y1_normalize.min()
        if (y1_normalize.max() > y1_max): y1_max = y1_normalize.max()
        axs[1].plot(x1, y1_normalize, linestyle = ':', color=color_1)
        if err[0]:
            axs[1].errorbar(x1_centre, y1_normalize, err[1], err[2])

            #fitted Slow Axis
        x1_fit = np.array(dataFF[i_ff+ff_sa][0],dtype=float)
        y1_fit = GaussFunction(x1_fit, *FitGaussian(x1_fit, dataFF[i_ff+ff_sa][1])[0])
        x1_centre_fit = Centre(x1_fit, np.where(y1_fit == y1_fit.max())[0])
        y1_fit_normalize = Normalize(y1_fit)
        axs[1].plot(x1_centre_fit, y1_fit_normalize, linestyle = '-', color=color_1)
        # axs[1].text(dataFF[i_ff][0][0]-3, 1-0.07, 'Slow Axis FWHM: %.2f'%(resultat_SA), backgroundcolor='k', color='w')

            #theory Slow Axis
        x1_theory = np.array(dataFF[i_ff+ff_sa][0],dtype=float)
        y1_theory = np.array(IntensityT(dataNF[9][i_nf][nf_sa], lbd, dataFF[i_ff+ff_sa][0]), dtype=float)
        x1_centre_theory = Centre(x1_theory, np.where(y1_theory == y1_theory.max())[0])
        y1_theory_normalize = Normalize(y1_theory)
        axs[1].plot(x1_centre_theory, y1_theory_normalize, linestyle = '-.', color=color_1)
        # axs[1].text(dataFF[i_ff][0][0]-3, 1-0.22, 'Slow Axis FWHM theory: %.2f'%(resultat_SA_theory), backgroundcolor='k', color='w')

        i_ff += 2

    axs[0].set_title('Fast Axis : x axis')
    axs[0].legend(title=':data\n: fit\n-. theory')
    axs[0].set_xlim([min(x0_min, x1_min), max(x0_max, x1_max)])
    axs[0].set_ylim([min(y0_min, y1_min), max(y0_max, y1_max)])
    axs[1].set_title('Slow Axis : y axis')
    axs[1].legend(title=':data\n: fit\n-. theory')
    axs[1].set_xlim([min(x0_min, x1_min), max(x0_max, x1_max)])
    axs[1].set_ylim([min(y0_min, y1_min), max(y0_max, y1_max)])

    fig.text(0.5, 0.04, 'Beam Divergence (°)', ha='center', va='center')
    fig.text(0.06, 0.5, 'Normalize Intensity (a.u)', ha='center', va='center', rotation='vertical')

    if err[0]:
        plt.savefig(name+' error bar.png', dpi=150)
    else:
        plt.savefig(name+'.png', dpi=150)

def PrintFFtoNF(file, dataFF, dataNF, title, nf_fa, nf_sa, ff_fa, ff_sa, nb):
    file = open(file,"w")
    file.writelines(title)

    i_ff = 0
    for i_nf in range(nb):

        resultat_FA = dataNF[9][i_nf][nf_fa]
        resultat_SA = dataNF[9][i_nf][nf_sa]
        resultat_FA_theory = Petermann(dataFF[i_ff+ff_fa], lbd, 0)*1e6
        resultat_SA_theory = Petermann(dataFF[i_ff+ff_sa], lbd, 1)*1e6
        err_FA = abs(resultat_FA-resultat_FA_theory)/resultat_FA_theory
        err_SA = abs(resultat_SA-resultat_SA_theory)/resultat_SA_theory
        file.writelines('\n\nFast Axis 1/e^2: %.2fµm' %(resultat_FA))
        file.writelines('\nFast Axis 1/e^2 PetermannII: %.2fµm' %(resultat_FA_theory))
        file.writelines('\nRelative error: %.2f' %(err_FA*100))
        file.writelines('\nSlow Axis 1/e^2: %.2fµm' %(resultat_SA))
        file.writelines('\nSlow Axis 1/e^2 PetermannII: %.2fµm' %(resultat_SA_theory))
        file.writelines('\nRelative error: %.2f' %(err_SA*100))

        fit_parameters = FitGaussian(np.array(dataFF[i_ff+ff_fa][0], dtype=float), np.array(dataFF[i_ff+ff_fa][1], dtype=float))
        file.writelines('\n\nGaussian fit parameters (Fast Axis) [a, b, c]: %s' %(fit_parameters[0]))

        fit_parameters = FitGaussian(np.array(dataFF[i_ff+ff_sa][0], dtype=float), np.array(dataFF[i_ff+ff_sa][1], dtype=float))
        file.writelines('\nGaussian fit parameters (Slow Axis) [a, b, c]: %s' %(fit_parameters[0]))

        i_ff += 2

    file.close()

def PrintNFtoFF(file, dataFF, dataNF, title, nf_fa, nf_sa, ff_fa, ff_sa, nb):
    file = open(file,"w")
    file.writelines(title)

    i_ff = 0
    for i_nf in range(nb):

        resultat_FA = FWHM(GaussFunction(np.array(dataFF[i_ff+ff_fa][0], dtype=float), *FitGaussian(np.array(dataFF[i_ff+ff_fa][0], dtype=float), np.array(dataFF[i_ff+ff_fa][1], dtype=float))[0]))[1][0][0]
        resultat_SA = FWHM(GaussFunction(np.array(dataFF[i_ff+ff_sa][0], dtype=float), *FitGaussian(np.array(dataFF[i_ff+ff_sa][0], dtype=float), np.array(dataFF[i_ff+ff_sa][1], dtype=float))[0]))[1][0][0]
        resultat_FA_theory = FWHM(IntensityT(dataNF[9][i_nf][nf_fa], lbd, dataFF[i_ff+ff_fa][0]))[1][0][0]
        resultat_SA_theory = FWHM(IntensityT(dataNF[9][i_nf][nf_sa], lbd, dataFF[i_ff+ff_sa][0]))[1][0][0]
        err_FA = abs(resultat_FA-resultat_FA_theory)/resultat_FA_theory
        err_SA = abs(resultat_SA-resultat_SA_theory)/resultat_SA_theory
        file.writelines('\n\nFast Axis FWHM: %.2f°' %(resultat_FA))
        file.writelines('\nFast Axis FWHM theory: %.2f°' %(resultat_FA_theory))
        file.writelines('\nRelative error: %.2f' %(err_FA*100))
        file.writelines('\nSlow Axis FWHM: %.2f°' %(resultat_SA))
        file.writelines('\nSlow Axis FWHM theory: %.2f°' %(resultat_SA_theory))
        file.writelines('\nRelative error: %.2f' %(err_SA*100))

        fit_parameters_fa = FitGaussian(dataNF[6][i_nf][nf_fa], Normalize(np.array(dataNF[2][i_nf][nf_fa], dtype=float)))[2]
        file.writelines('\n\nGaussian fit parameters (Fast Axis) [mean, sigma]: %s' %(fit_parameters_fa))

        fit_parameters_sa = FitGaussian(dataNF[6][i_nf][nf_sa], Normalize(np.array(dataNF[2][i_nf][nf_sa], dtype=float)))[2]
        file.writelines('\n\nGaussian fit parameters (Slow Axis) [mean, sigma]: %s' %(fit_parameters_sa))

        i_ff += 2

    file.close()

nf_fa = 0 #THIS VALUE MIGHT CHANGE
nf_sa = 1
ff_fa = 1 #THIS VALUE MIGHT CHANGE
ff_sa = 0

###
if mode==4:
    if not os.path.exists(Directory_FFtoNF):
        os.mkdir(Directory_FFtoNF)
    data_FF = LoadDataFF(Files(nb)[2])
    data_NF = LoadDataNF(Files(nb)[3])
    PlotFFtoNF(data_FF, data_NF, lbd, URL_FFtoNF, title_FFtoNF, nf_fa, nf_sa, ff_fa, ff_sa, err, nb, modelisation)
    PrintFFtoNF(file_FFtoNF, data_FF, data_NF, title_FFtoNF, nf_fa, nf_sa, ff_fa, ff_sa, nb)
###

###
if mode==5:
    if not os.path.exists(Directory_NFtoFF):
        os.mkdir(Directory_NFtoFF)
    data_FF = LoadDataFF(Files(nb)[2])
    data_NF = LoadDataNF(Files(nb)[3])
    PlotNFtoFF(data_FF, data_NF, lbd, URL_NFtoFF, title_NFtoFF, nf_fa, nf_sa, ff_fa, ff_sa, err, nb)
    PrintNFtoFF(file_NFtoFF, data_FF, data_NF, title_NFtoFF, nf_fa, nf_sa, ff_fa, ff_sa, nb)
###
