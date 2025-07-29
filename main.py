import os
import hashlib
import logging

# Configure logging
logging.basicConfig(filename='file_monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_file_hash(file_path):
    """Generate SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def monitor_directory(directory):
    """Monitor a directory for file changes."""
    file_hashes = {}

    # Initial scan of the directory
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_hashes[filename] = get_file_hash(os.path.join(directory, filename))

    while True:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                current_hash = get_file_hash(file_path)

                # Check for new or modified files
                if filename not in file_hashes:
                    logging.info(f'New file detected: {filename}')
                    file_hashes[filename] = current_hash
                elif file_hashes[filename] != current_hash:
                    logging.info(f'Modified file detected: {filename}')
                    file_hashes[filename] = current_hash

        # Check for deleted files
        for filename in list(file_hashes.keys()):
            if filename not in os.listdir(directory):
                logging.info(f'Deleted file detected: {filename}')
                del file_hashes[filename]

if __name__ == "__main__":
    # Directory to monitor
    directory_to_monitor = "/path/to/monitor"
    monitor_directory(directory_to_monitor)