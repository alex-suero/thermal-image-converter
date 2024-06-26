# Thermal Image Converter

This repository contains a Python script that converts thermal JPEG images captured by DJI drones into TIFF format containing a single layer with temperature values in Celsius. The converted images are saved in the "output_images" folder.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Author](#author)

## Requirements

- `dji_thermal_sdk` (included in the repository)
- `exiftool` (included in the repository)
- `GDAL` (version 3.4.3 for Python 3.11 and Windows included in repository)

- Python 3.11
- The following Python libraries:
  - `gdal`
  - `dji_thermal_sdk`

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/alex-suero/thermal-image-converter.git
    cd thermal-image-converter
    ```

2. **Install the required Python libraries:**
    
    - Example with provided GDAL wheel:

   ```sh
    pip install dji_thermal_sdk
    python -m pip install GDAL-3.4.3-cp311-cp311-win_amd64.whl
    ```

4. **Make sure `exiftool.exe` is in the root directory:**

    - You can download `exiftool` from [here](https://exiftool.org/).

## Usage

1. **Prepare your input images:**

    - Place all thermal JPEG images (with `_T.JPG` suffix) in the `input_images` folder.

2. **Run the script:**

    ```sh
    python thermal_converter.py
    ```

3. **Find your converted images:**

    - The converted TIFF images will be saved in the `output_images` folder.

## Example

Here's an example of how to use the script:

1. **Place your thermal JPEG images in the `input_images` folder:**

    ```
    input_images/
    ├── image1_T.JPG
    ├── image2_T.JPG
    └── image3_T.JPG
    ```

2. **Run the script:**

    ```sh
    python thermal_converter.py
    ```

3. **Check the `output_images` folder for the converted TIFF images:**

    ```
    output_images/
    ├── image1.tif
    ├── image2.tif
    └── image3.tif
    ```

## Author
This script was developed by [Alexis Suero Mirabal](https://github.com/alex-suero).
