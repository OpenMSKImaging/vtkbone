import os
import vtkbone
import SimpleITK as sitk
import vtk
import numpy as np

def sitk_to_aim(file_path='', sitk_img=None, WRITE_AIM=False, output_path=''):
    """
    Convert a SimpleITK image to an AIM (Analyze Image) file using vtkbone.

    Parameters:
    - file_path (str, optional): Path to the SimpleITK image file. If specified, the SimpleITK image will be read from this file.
    - sitk_img (SimpleITK.Image, optional): SimpleITK image to be converted to AIM. If specified, the 'file_path' parameter will be ignored.
    - WRITE_AIM (bool, optional): If True, the converted AIM image will be written to a file. Defaults to False.
    - output_path (str, optional): Path to save the AIM file. If not provided, the AIM file will be saved in the same directory as the input file (if 'file_path' is given).

    Returns:
    - vtk_img (vtk.vtkImageData): Converted vtkImageData.

    Raises:
    - ValueError: If neither 'file_path' nor 'sitk_img' is provided, or if an incorrect image unit is specified in metadata.
    - Warning: If no unit is specified for SimpleITK, it assumes native units.

    Example:
    ```python
    vtk_img = sitk_to_aim(file_path='path/to/sitk_image.mha', WRITE_AIM=True, output_path='path/to/aim_output.aim')
    ```

    """
    # error if no input is given
    if file_path == '' and sitk_img is None:
        raise ValueError('You have to specify either a SimpleITK image or a file path')

    # if path given, read in path
    elif file_path != '':
        sitk_img = sitk.ReadImage(file_path)

    # check header info and image unit
    keys = sitk_img.GetMetaDataKeys()
    if 'processing_log' not in keys:
        raise ValueError('No header information present in SimpleITK image')

    elif 'unit' not in keys:
        raise Warning('No unit specified for SimpleITK, assuming native units.')
        unit = 'native'
    else:
        unit = sitk_img.GetMetaData('unit')

    img_log = sitk_img.GetMetaData('processing_log')
    img_log = img_log.replace('_LINEBREAK_', '\n')

    # to numpy array
    np_image = sitk.GetArrayFromImage(sitk_img)

    if unit == 'mu':
        mu_scaling, hu_mu_water, hu_mu_air, density_slope, density_intercept = get_aim_calibration_constants_from_processing_log(img_log)
        np_image_native = np_image * mu_scaling

    elif unit == 'HU':
        mu_scaling, hu_mu_water, hu_mu_air, density_slope, density_intercept = get_aim_calibration_constants_from_processing_log(img_log)
        m, b = get_aim_hu_equation(img_log)
        np_image_native = (np_image - b) / m

    elif unit == 'BMD':
        mu_scaling, hu_mu_water, hu_mu_air, density_slope, density_intercept = get_aim_calibration_constants_from_processing_log(img_log)
        np_image_native = (np_image - density_intercept) * mu_scaling / density_slope

    elif unit == 'native':
        np_image_native = np_image

    else:
        raise ValueError(f'Incorrect image unit specified in metadata: {unit}.')

    # vtk and itk have their x and z axes flipped
    np_image_native = np.transpose(np_image_native)

    origin = sitk_img.GetOrigin()
    spacing = sitk_img.GetSpacing()
    vtk_img = numpy_to_vtkImageData(np_image_native, spacing=spacing, origin=origin, array_type=vtk.VTK_SHORT)

    if WRITE_AIM:
        if file_path == '' and output_path == '':
            raise ValueError('No output path is given to write AIM file')
        elif output_path == '':
            folder = os.path.dirname(file_path)
            file = os.path.basename(file_path).split('.')[0]
            output_path = os.path.join(folder, f'{file}.aim')

        writer = vtkbone.vtkboneAIMWriter()
        writer.SetFileName(output_path)
        writer.SetInputData(vtk_img)
        writer.NewProcessingLogOff()
        writer.SetProcessingLog(img_log)
        writer.Update()
        writer.Write()

    return vtk_img
