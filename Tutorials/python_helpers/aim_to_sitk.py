import os

import numpy as np
import SimpleITK as sitk
import vtk
from python_helpers.aim_calibration_header import (
    get_aim_calibration_constants_from_processing_log, get_aim_hu_equation)
from python_helpers.vtk_util import vtkImageData_to_numpy

import vtkbone


def aim_to_sitk(file_path, scaling, WRITE_MHA=False):
    """
    This function reads in an aim file, scales it to an image unit of choice and returns it as a SimpleITK image.
    Scaling is achieved by calibration information from the aim header file.
    
    Input:
        - file_path <str>: path to input aim
        - scaling <str>: unit of output image. Specify as HU, mu, BMD or none
        - WRITE_MHA <bool>: bool to indicate whether or not to write the image as an mha-file.
        
    Output:
        - sitk_img: SimpleITK image class of aim image
    """
    
    # read in aim image
    reader = vtkbone.vtkboneAIMReader()
    reader.DataOnCellsOff()
    reader.SetFileName(file_path)
    reader.Update()
    img_file = reader.GetOutput()
    img_log = reader.GetProcessingLog()
    
    #convert to numpy array for scaling
    np_image = vtkImageData_to_numpy(img_file)
    
    if scaling == 'mu':
        #get calibration information from AIM processing log
        mu_scaling, hu_mu_water, hu_mu_air, density_slope, density_intercept = get_aim_calibration_constants_from_processing_log(img_log)
        np_image_scaled = np_image/mu_scaling
        print("image converted to linear attenuation")
    
    elif scaling == 'HU':
        #get calibration information from AIM processing log
        mu_scaling, hu_mu_water, hu_mu_air, density_slope, density_intercept = get_aim_calibration_constants_from_processing_log(img_log)
        m, b = get_aim_hu_equation(img_log)
        np_image_scaled = (np_image*m)+b
        print("image converted to linear attenuation")
        
    elif scaling == 'BMD':
        #get calibration information from AIM processing log
        mu_scaling, hu_mu_water, hu_mu_air, density_slope, density_intercept = get_aim_calibration_constants_from_processing_log(img_log)
        np_image_scaled = np_image/mu_scaling * density_slope + density_intercept
        print('image converted to bone mineral density')
    
    elif scaling == 'none': 
        np_image_scaled = np_image
        print("image values are unchanged")   
    
    else:
        raise ValueError(f'{scaling} is not a valid scaling option. Enter with \'HU\', \'mu\', \'BMD\' or \'none\'')
    
    # convert to SimpleITK image class
    origin = np.asarray(img_file.GetOrigin())
    spacing = np.asarray(img_file.GetSpacing())
    
    # #vtk and itk have their x and z axes flipped
    np_image_scaled = np.transpose(np_image_scaled)
        
    sitk_img = sitk.GetImageFromArray(np_image_scaled)
    sitk_img.SetOrigin(origin)
    sitk_img.SetSpacing(spacing)
    
    # adding the processing log, no \n for sitk compatibality
    sitk_log = img_log.replace('\n', '_LINEBREAK_')
    sitk_img.SetMetaData('processing_log', sitk_log)
    
    # adding a new meta data key that stores the current image unit
    unit = scaling if scaling is not 'none' else 'native'
    sitk_img.SetMetaData('unit', unit)

    if WRITE_MHA:
        # writing in same directory as aim file
        folder = os.path.dirname(file_path)
        file = os.path.basename(file_path).split('.')[0]
        out_path = os.path.join(folder, f'{file}.mha')
        print(f'Writing image to {out_path}')
        sitk.WriteImage(sitk_img, out_path)

    return sitk_img
