from dji_thermal_sdk.dji_sdk import *
from dji_thermal_sdk.utility import rjpeg_to_heatmap
from osgeo import gdal
import os
import subprocess
import logging

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
        2. Convert each JPG to a thermal TIFF file with temperature values.
        3. Move TIFF files to the output folder.
        4. Clean up any intermediate files without metadata.
    """
    input_folder = 'input_images'
    output_folder = 'output_images'
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # List input files
    input_files = [file for file in os.listdir(input_folder) 
                   if file.endswith('_T.JPG')]
    
    if len(input_files) == 0:
                logging.warning('No thermal images found in the input directory.')
                return None

    # Convert thermal JPG files to thermal TIFF files
    logging.info('Converting thermal JPG files to thermal TIFF files...')
    total = len(input_files)
    for n, file in enumerate(input_files):
        # Print progress bar
        progress_bar(n + 1, total)
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
    print('\nMoving TIFF files...')
    for file in tif_files:
        src_path = os.path.join(input_folder, file)
        dest_path = os.path.join(output_folder, file)
        os.rename(src_path, dest_path)
    
    # Delete TIFF files without metadata
    print('Deleting temporary files...')
    for file in no_meta_tif_files:
        os.remove(os.path.join(input_folder, file))

    logging.info('Done!')
        
def progress_bar(progress, total):
    """
    Prints a progress bar for a given process.

    Args:
        progress (int): current iteration number
        total (int): total number of iterations
    """
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent/2) + '-'*(50 - int(percent/2))
    print(f"\r|{bar}| {progress}/{total} [{percent:.1f}%]", end="\r")
    
def jpg_to_thermal_tif(filename, input_folder):
    """
    Converts an RJPEG thermal image to TIF format with a single layer containing
    temperature values in Celsius while maintaining original tags (metadata).

    Arguments:
        filename: Name of the file inside the input folder.
        input_folder: Path to the input folder containing the image files.
    """
    # Initialize DJI thermal SDK
    path = "dji_thermal_sdk/utility/bin/windows/release_x64/libdirp.dll"
    dji_init(path)

    # set input filepath and output filepath
    filepath = os.path.join(input_folder, filename)
    out_file = filename.split('.')[0]+'.tif'
    out_filepath = 'input_images/'+out_file

    # get temperature image as an array
    img = rjpeg_to_heatmap(filepath, 0)

    # create output TIFF file
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(out_filepath, img.shape[1], 
                           img.shape[0], 1, gdal.GDT_Float32)
    out_band = out_ds.GetRasterBand(1)

    # write array (temperature) to TIFF file
    out_band.WriteArray(img)
    out_ds = None

    # copy metadata from original JPG file to TIFF file
    subprocess.run(['exiftool', '-tagsfromfile', filepath, out_filepath], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__=='__main__':
    main()
