import os
import subprocess
import time
import shutil  # For copying files
from datetime import datetime

# Configuration
INPUT_DIRECTORY = "Z:\FEED"  # Replace with your shared drive path
OUTPUT_DIRECTORY = "Z:\FEED\Output"  # Replace with your desired output directory
CONVERSION_OPTIONS = [
    "-c:v", "h264_nvenc",
    "-preset", "p4",  # You can adjust the preset (e.g., "fast", "slow")
    "-rc", "vbr",          # Rate control mode (variable bit rate)
    "-crf", "23",        # Adjust the Constant Rate Factor (lower for higher quality)
    "-vf", "scale=1920:1080,setsar=1:1",
    "-c:a", "aac",
    "-b:a", "192k"
]
ERROR_RECONVERSION_DELAY = 120  # seconds (2 minutes)
MAX_RECONVERSION_ATTEMPTS = 3

conversion_queue = []
processing_file = None
failed_conversions = {}

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def find_ts_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(".ts")]

def add_to_queue(filepath):
    if filepath not in conversion_queue and filepath not in failed_conversions:
        conversion_queue.append(filepath)
        log(f"Added to queue: {os.path.basename(filepath)}")

def copy_file_locally(filepath):
    local_path = os.path.join("C:\\temp_conversion", os.path.basename(filepath))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    log(f"Copying '{os.path.basename(filepath)}' to local drive...")
    try:
        shutil.copy2(filepath, local_path)  # copy2 preserves metadata
        log(f"Successfully copied to '{local_path}'")
        return local_path
    except Exception as e:
        log(f"Error copying '{os.path.basename(filepath)}': {e}")
        return None

def convert_ts_to_mp4(input_path, output_path):
    global processing_file
    processing_file = os.path.basename(input_path)
    log(f"Starting conversion of '{processing_file}'...")
    command = [
        "ffmpeg",
        "-i", input_path,
        *CONVERSION_OPTIONS,
        output_path
    ]

    process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)

    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # Look for the progress information (you might need to adjust the regex)
            if "frame=" in output and "time=" in output and "speed=" in output:
                print(f"\rProgress: {output.strip()}", end="")

    return_code = process.wait()
    processing_file = None
    if return_code == 0:
        log(f"\nSuccessfully converted '{os.path.basename(input_path)}' to '{os.path.basename(output_path)}'")
        return True
    else:
        error_output = process.stderr.read()
        log(f"\nError converting '{os.path.basename(input_path)}': Return code {return_code}\n{error_output}")
        return False

def process_queue():
    global conversion_queue
    while conversion_queue:
        filepath = conversion_queue.pop(0)
        filename_without_ext = os.path.splitext(os.path.basename(filepath))[0]
        output_filepath = os.path.join(OUTPUT_DIRECTORY, f"{filename_without_ext}.mp4")

        local_filepath = copy_file_locally(filepath)
        if local_filepath:
            if convert_ts_to_mp4(local_filepath, output_filepath):
                try:
                    os.remove(local_filepath)  # Clean up the local copy
                except Exception as e:
                    log(f"Error deleting local file '{os.path.basename(local_filepath)}': {e}")
            else:
                if filepath not in failed_conversions:
                    failed_conversions[filepath] = 1
                    log(f"Added '{os.path.basename(filepath)}' to failed conversions for retry.")
                elif failed_conversions[filepath] < MAX_RECONVERSION_ATTEMPTS:
                    failed_conversions[filepath] += 1
                    log(f"Re-adding '{os.path.basename(filepath)}' to queue (attempt {failed_conversions[filepath]}).")
                    # Re-insert at the beginning for immediate retry (you might adjust this)
                    conversion_queue.insert(0, filepath)
                else:
                    log(f"Maximum reconversion attempts reached for '{os.path.basename(filepath)}'.")

def monitor_directory():
    existing_files = set(find_ts_files(INPUT_DIRECTORY))
    log("Starting directory monitoring...")
    while True:
        current_files = set(find_ts_files(INPUT_DIRECTORY))
        new_files = list(current_files - existing_files)
        if new_files:
            log(f"New files found: {', '.join([os.path.basename(f) for f in new_files])}")
            for file in new_files:
                add_to_queue(file)
            existing_files.update(new_files)
        process_queue()
        time.sleep(10)  # Check for new files every 10 seconds

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    os.makedirs("C:\\temp_conversion", exist_ok=True)
    monitor_directory()
