# TS to MP4 Converter

This Python script is specifically crafted for Jamuna Television Ltd. It's designed for daily use to efficiently convert approximately 100 video files per day, which are sent in by reporters from outdoor locations. By automating this conversion process, the script significantly streamlines the workflow for the IT team, making their work more manageable and faster.

This Python script automatically converts `.ts` video files from a shared network drive folder to `.mp4` format using FFmpeg with NVIDIA GPU acceleration. It monitors the input folder, copies files locally for processing, and handles errors with retries.


**Target PC Configuration:**

* **Processor:** 13th Gen Intel(R) Core(TM) i7-13700 @ 2.10 GHz
* **RAM:** 32.0 GB
* **Graphics:** NVIDIA GeForce RTX 4060 Ti
* **OS:** Windows 11 Version 24H2

  
## Prerequisites

1.  **FFmpeg:** Version 7.1.1 installed and its `bin` directory added to your system's PATH.
2.  **Python:** Version 3.13.3 installed with "Add Python to PATH" selected during installation.

## Setup

1.  **Download Script:** Save the `ts_converter.py` file to `C:/ffmpeg/bin/`.
2.  **Configure Directories:** Edit `ts_converter.py`:
    * Set `INPUT_DIRECTORY` to your shared network drive input folder (e.g., `"Z:\FEED"`).
    * Set `OUTPUT_DIRECTORY` to your desired output folder on the shared drive (e.g., `"Z:\FEED\Output"`).
3.  **Review `CONVERSION_OPTIONS`:** Adjust FFmpeg encoding settings (codec, preset, resolution, etc.) as needed.

## Running the Script

1.  **Create Batch File:** Save the following code as `run_converter.bat` in the same directory as `ts_converter.py` (i.e., `C:/ffmpeg/bin/`):

    ```batch
    @echo off
    echo Starting the TS to MP4 conversion script...
    python ts_converter.py
    echo Conversion script finished.
    pause
    ```

2.  **Execute:** Double-click `run_converter.bat` to start the conversion process. The script will monitor the input folder and process new `.ts` files automatically.

## Operation

* Monitors the `INPUT_DIRECTORY` for new `.ts` files.
* Copies new files to `C:\temp_conversion` for local processing.
* Converts to `.mp4` using FFmpeg with specified options and NVIDIA GPU.
* Saves the output in `OUTPUT_DIRECTORY`.
* Retries failed conversions up to 3 times after a 2-minute delay.

## Important

* Ensure correct network share permissions.
* NVIDIA GPU and drivers are required for hardware acceleration.
* Sufficient free space on the `C:` drive for temporary files.
