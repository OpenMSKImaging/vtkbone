import os
import vtkbone
import SimpleITK as sitk
import numpy as np

def aim_to_sitk(file_path, scaling, WRITE_MHA=False):
    """
    Convert a bone imaging file in AIM format to a SimpleITK image.

    Parameters:
    - file_path (str): Path to the AIM bone imaging file.
    - scaling (str): Scaling option for the image. Choose from 'HU', 'mu', 'BMD', or 'none'.
    - WRITE_MHA (bool, optional): If True, the converted image will be saved as an MHA file in the same directory.
                                   Defaults to False.

    Returns:
    - sitk_img (SimpleITK.Image): Converted SimpleITK image.

    Raises:
    - ValueError: If an invalid scaling option is provided.

    Example:
    ```python
    sitk_img = aim_to_sitk('path/to/aim_file.aim', scaling='HU', WRITE_MHA=True)
    ```

    """
    # read in aim image
    reader = vtkbone.vtkboneAIMReader()
    reader.DataOnCellsOff()
    reader.SetFileName(file_path)
    reader.Update()
    img_file = reader.GetOutput()
    img_log = reader.GetProcessingLog()

    # convert to numpy array for scaling
    np_image = vtkImageData_to_numpy(img_file)

    if scaling == 'mu':
        # get calibration information from AIM processing log
        mu_scaling, hu_mu_water, hu_mu_air, density_slope, density_intercept = get_aim_calibration_constants_from_processing_log(img_log)
        np_image_scaled = np_image / mu_scaling
        print("image converted to linear attenuation")

    elif scaling == 'HU':
        # get calibration information from AIM processing log
        mu_scaling, hu_mu_water, hu_mu_air, density_slope, density_intercept = get_aim_calibration_constants_from_processing_log(img_log)
        m, b = get_aim_hu_equation(img_log)
        np_image_scaled = (np_image * m) + b
        print("image converted to linear attenuation")

    elif scaling == 'BMD':
        # get calibration information from AIM processing log
        mu_scaling, hu_mu_water, hu_mu_air, density_slope, density_intercept = get_aim_calibration_constants_from_processing_log(img_log)
        np_image_scaled = (np_image / mu_scaling) * density_slope + density_intercept
        print('image converted to bone mineral density')

    elif scaling == 'none':
        np_image_scaled = np_image
        print("image values are unchanged")

    else:
        raise ValueError(f'{scaling} is not a valid scaling option. Enter with \'HU\', \'mu\', \'BMD\' or \'none\'')

    # convert to SimpleITK image class
    origin = np.asarray(img_file.GetOrigin())
    spacing = np.asarray(img_file.GetSpacing())

    # vtk and itk have their x and z axes flipped
    origin[0], origin[2] = origin[2], origin[0]
    spacing[0], spacing[2] = spacing[2], spacing[0]
    np_image_scaled = np.transpose(np_image_scaled)

    sitk_img = sitk.GetImageFromArray(np_image_scaled)
    sitk_img.SetOrigin(origin)
    sitk_img.SetSpacing(spacing)

    if WRITE_MHA:
        folder = os.path.dirname(file_path)
        file = os.path.basename(file_path).split('.')[0]
        out_path = os.path.join(folder, f'{file}.mha')
        print(f'Writing image to {out_path}')
        sitk.WriteImage(sitk_img, out_path)

    return sitk_img
