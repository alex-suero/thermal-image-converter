from dji_thermal_sdk.dji_sdk import *
from dji_thermal_sdk.utility import rjpeg_to_heatmap
import rasterio
import os
import subprocess
import logging
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """
    Converts all thermal JPG images in the "input_images" folder to TIFF format 
    with Celsius temperature values. Resulting images are located in the 
    "output_images" folder.

    Requirements:
        - "dji_thermal_sdk" folder in the directory
        - "exiftool.exe" file in the directory
        - Input images should be in "input_images" folder
        - Output images will be saved in "output_images" folder

    Steps:
        1. List all thermal JPG images in the input folder.
        2. Convert each image to TIFF format with temperature values in a single 
           layer.
        3. Move TIFF files to the output folder.
        4. Delete temporary files.
    """
    input_folder = 'input_images'
    output_folder = 'output_images'
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # List input files
    input_files = [file for file in os.listdir(input_folder) 
                   if file.endswith('_T.JPG')]
    
    if len(input_files) == 0:
                logging.warning(
                     'No thermal images found in the input directory.'
                )
                return None

    # Convert thermal JPG files to thermal TIFF files
    logging.info('Converting thermal JPG files to thermal TIFF files')
    for file in tqdm(input_files):
        # Convert JPG to thermal TIFF
        try:
            jpg_to_thermal_tif(file, input_folder)
        except Exception as e:
            logging.error(f"Error converting {file}: {e}")
        

    # List new TIFF files and TIFF files without metadata
    tif_files = [file for file in os.listdir(input_folder) 
                 if file.endswith('.tif')]
    no_meta_tif_files = [file for file in os.listdir(input_folder) 
                         if file.endswith('original')]

    # Move TIFF files with metadata to output folder
    logging.info('Moving TIFF files')
    for file in tif_files:
        src_path = os.path.join(input_folder, file)
        dest_path = os.path.join(output_folder, file)
        os.rename(src_path, dest_path)
    
    # Delete TIFF files without metadata
    logging.info('Deleting temporary files')
    for file in no_meta_tif_files:
        os.remove(os.path.join(input_folder, file))

    logging.info('Done!')


def jpg_to_thermal_tif(filename: str, input_folder: str)-> None:
    """
    Converts an RJPEG thermal image to TIF format with a single layer containing
    temperature values in Celsius while maintaining original tags (metadata).

    Args:
        filename (str): name of the file inside the input folder.
        input_folder (str): path to the input folder containing the image files.
    """
    # Initialize DJI thermal SDK
    path = "dji_thermal_sdk/utility/bin/windows/release_x64/libdirp.dll"
    dji_init(path)

    # Set input filepath and output filepath
    filepath = os.path.join(input_folder, filename)
    out_file = filename.split('.')[0] + '.tif'
    out_filepath = os.path.join(input_folder, out_file)

    # Get temperature image as an array
    img = rjpeg_to_heatmap(filepath, 0)

    # Create and write the output TIFF file using rasterio
    with rasterio.open(
        out_filepath,
        'w',
        driver='GTiff',
        height=img.shape[0],
        width=img.shape[1],
        count=1,
        dtype=rasterio.float32,
    ) as dst:
        dst.write(img, 1)

    # Copy metadata from the original JPG file to the TIFF file
    subprocess.run(['exiftool', '-tagsfromfile', filepath, out_filepath],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__=='__main__':
    main()
