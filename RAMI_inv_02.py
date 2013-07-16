#Inversion of RAMI data by EO-LDAS

import numpy as np
import os
import eoldas
from math import *

def calc_inv(f_red, f_nir, saa_true, azim, lad, conf_file, f_result):
        f = open(f_red, 'r')
        tmp_str = f.read()
        f.close()
        list1 = tmp_str.split('\n')
        f = open(f_nir, 'r')
        tmp_str = f.read()
        f.close()
        list2 = tmp_str.split('\n')

        red = np.zeros(len(list1)-1)
        nir = np.zeros(len(list1)-1)
        sza = np.zeros(len(list1)-1)
        saa = np.zeros(len(list1)-1)
        vza = np.zeros(len(list1)-1)
        vaa = np.zeros(len(list1)-1)

        for i in range( 1, len(list1)-1 ):
            red[i] = list1[i].split()[3]
            nir[i] = list2[i].split()[3]
            sza[i] = round(float(list1[i].split()[0]) * 180/pi)
            #saa[i] = list1[i].split()[2]
            saa[i] = saa_true
            vaa[i] = saa_true - round(float(list1[i].split()[2]) * 180/pi)
            vza[i] = round(float(list1[i].split()[1]) * 180/pi)
            if vaa[i] == azim:
                vza[i] = round(-1 * float(list1[i].split()[1]) * 180/pi)

        #print vza[70]
        for i in range(1, 76):
            f_state = '/media/sf_JRC/RAMI/data/'+f_result+str(i)+'.dat'
            f = open(f_state, 'w')
            f.write('#PARAMETERS time mask vza vaa sza saa 650 860 sd-650 sd-860\n')
            f.write(' 1 1 ' + str( vza[i]) +' '+ str(vaa[i]) +' '+ str(sza[i]) +' '+ str(saa[i]) +
            ' '+ str(red[i]) +' '+ str(nir[i]) +' 0.001 0.001')
            f.close()
            cmd = 'eoldas --conf=eoldas_config.conf --conf=' + conf_file + \
            ' --parameter.x.assoc_default.lad=' + str(lad) + \
            ' --parameter.result.filename=/media/sf_JRC/RAMI/output/'+f_result+str(i)+'.params ' + \
            ' --operator.obs.y.result.filename=/media/sf_JRC/RAMI/output/'+f_result+str(i)+'.fwd' + \
            ' --operator.obs.y.state=' + f_state
            print cmd
            self = eoldas.eoldas(cmd)
            print '************************************Solve now!****************************' 
            self.solve(write=True)
            print '************************************Solve was Done!****************************'
            

#f_red = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfop_ROMCREF-HOM03_DIS_ERE_RED_50.mes'
#f_nir = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfop_ROMCREF-HOM03_DIS_ERE_NIR_50.mes'

#LAD     = Leaf Angle Distribution
#                       = 1   <---> Planophile
#                       = 2   <---> Erectophile
#                       = 3   <---> Plagiophile
#                       = 4   <---> Extremophile
#
#                       = 5   <---> Uniforme
#**********Homogeneous discrete cases in the solar domain**********************************
#Cross plane
#SZA = 20, SAA = 0
f_red = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfop_ROMCREF-HOM03_DIS_ERE_RED_20.mes'
f_nir = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfop_ROMCREF-HOM03_DIS_ERE_NIR_20.mes'
f_result = 'brfop_ROMCREF-HOM03_DIS_ERE_20_'
#prior_state = '0.3 1 0.1 0.5 0.5 0.5 0.5 1.5 2 2.5 0 0 5'
#prior_sd =    '0.7 3 0.5 0.5 0.5 0.5 0.5 1.5 2 2.5 0 0 5'
conf_file = 'RAMI_prior.conf'
azim = 90.0
saa = 0.0
lad = 2
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#SZA = 50, SAA = 0
f_red = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfop_ROMCREF-HOM03_DIS_ERE_RED_50.mes'
f_nir = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfop_ROMCREF-HOM03_DIS_ERE_NIR_50.mes'
f_result = 'brfop_ROMCREF-HOM03_DIS_ERE_50_'
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
'''
#principal plane
#SZA = 20, SAA = 0
f_red = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfpp_ROMCREF-HOM03_DIS_ERE_RED_20.mes'
f_nir = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfpp_ROMCREF-HOM03_DIS_ERE_NIR_20.mes'
f_result = 'brfpp_ROMCREF-HOM03_DIS_ERE_20_'
azim = 0.0
saa = 0.0
lad = 2
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#SZA = 50, SAA = 0
f_red = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfpp_ROMCREF-HOM03_DIS_ERE_RED_50.mes'
f_nir = '/media/sf_JRC/RAMI/HOM03_DIS_ERE/brfpp_ROMCREF-HOM03_DIS_ERE_NIR_50.mes'
f_result = 'brfpp_ROMCREF-HOM03_DIS_ERE_50_'
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#**************************Conifer forests: TOPOGRAPHY************************************
#
#Cross Plane
f_red = '/media/sf_JRC/RAMI/HET03_STO/brfop_ROMCREF-HET03_STO_UNI_RED_40.mes'
f_nir = '/media/sf_JRC/RAMI/HET03_STO/brfop_ROMCREF-HET03_STO_UNI_NIR_40.mes'
f_result = 'brfop_ROMCREF-HET03_STO_UNI_40_'
#prior_state = '[0.05,0.45,20,0.05,0.5,0.5,0.5,0.5,1.5,2,2.5,0,0,5]'
#prior_sd =    '[0.05,0.5,20,0.1,0.5,0.5,0.5,0.5,1.5,2,2.5,0,0,5]'
conf_file = 'RAMI_prior_forest.conf'
azim = 90.0
saa = 180
lad = 5
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#Principal Plane
#SZA = 40
f_red = '/media/sf_JRC/RAMI/HET03_STO/brfpp_ROMCREF-HET03_STO_UNI_RED_40.mes'
f_nir = '/media/sf_JRC/RAMI/HET03_STO/brfpp_ROMCREF-HET03_STO_UNI_NIR_40.mes'
f_result = 'brfpp_ROMCREF-HET03_STO_UNI_40_'
azim = 0.0
saa = 180
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#****************************Birch stand**********************************************************
#
#Cross plane
#SZA = 20, SAA = 0
f_red = '/media/sf_JRC/RAMI/HET05_STO_UNI/brfop_ROMCREF-HET05_STO_UNI_RED_20.mes'
f_nir = '/media/sf_JRC/RAMI/HET05_STO_UNI/brfop_ROMCREF-HET05_STO_UNI_NIR_20.mes'
f_result = 'brfop_ROMCREF-HET05_STO_UNI_20_'
azim = 90.0
saa = 180.0
lad = 5
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#SZA = 50, SAA = 0
f_red = '/media/sf_JRC/RAMI/HET05_STO_UNI/brfop_ROMCREF-HET05_STO_UNI_RED_50.mes'
f_nir = '/media/sf_JRC/RAMI/HET05_STO_UNI/brfop_ROMCREF-HET05_STO_UNI_NIR_50.mes'
f_result = 'brfop_ROMCREF-HET05_STO_UNI_50_.mes'
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#Principal plane
#SZA = 20, SAA = 0
f_red = '/media/sf_JRC/RAMI/HET05_STO_UNI/brfpp_ROMCREF-HET05_STO_UNI_RED_20.mes'
f_nir = '/media/sf_JRC/RAMI/HET05_STO_UNI/brfpp_ROMCREF-HET05_STO_UNI_NIR_20.mes'
f_result = 'brfpp_ROMCREF-HET05_STO_UNI_20_'
azim = 0.0
saa = 180.0
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#SZA = 50, SAA = 0
f_red = '/media/sf_JRC/RAMI/HET05_STO_UNI/brfpp_ROMCREF-HET05_STO_UNI_RED_50.mes'
f_nir = '/media/sf_JRC/RAMI/HET05_STO_UNI/brfpp_ROMCREF-HET05_STO_UNI_NIR_50.mes'
f_result = 'brfpp_ROMCREF-HET05_STO_UNI_50_.mes'
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#***************************************Conifer forests: NO TOPOGRAPHY************************************
#
conf_file = 'RAMI_prior_forest.conf'
#Cross Plane
#SZA = 40
f_red = '/media/sf_JRC/RAMI/HET06_STO/brfop_ROMCREF-HET06_STO_UNI_RED_40.mes'
f_nir = '/media/sf_JRC/RAMI/HET06_STO/brfop_ROMCREF-HET06_STO_UNI_NIR_40.mes'
f_result = 'brfop_ROMCREF-HET06_STO_UNI_40_'
azim = 90.0
saa = 180
lad = 5
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
#
#Principal Plane
#SZA = 40
f_red = '/media/sf_JRC/RAMI/HET06_STO/brfpp_ROMCREF-HET06_STO_UNI_RED_40.mes'
f_nir = '/media/sf_JRC/RAMI/HET06_STO/brfpp_ROMCREF-HET06_STO_UNI_NIR_40.mes'
f_result = 'brfpp_ROMCREF-HET06_STO_UNI_40_'
azim = 0.0
saa = 180
calc_inv(f_red, f_nir, saa, azim, lad, conf_file, f_result)
'''
print 'Done!'
