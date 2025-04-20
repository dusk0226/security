import os
import hashlib

# Simulated database of known malicious hashes
malicious_hashes = {
    "5d41402abc4b2a76b9719d911017c592",  # Example hash (MD5 of "hello")
    "9e107d9d372bb6826bd81d3542a419d6",  # Another example
    # Add real malicious SHA-256 hashes here
}

# Function to calculate hash of a file
def calculate_hash(file_path, algorithm='sha256'):
    hash_func = getattr(hashlib, algorithm)()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()

# Simulated directory to scan (replace with real downloads folder if needed)
downloads_dir = 'C:/Users/admin/Desktop/SecurityCW/downloads'

# Scan each file in the folder
for filename in os.listdir(downloads_dir):
    file_path = os.path.join(downloads_dir, filename)
    if os.path.isfile(file_path):
        file_hash = calculate_hash(file_path)
        print(f"Scanned: {filename}, Hash: {file_hash}")
        
        if file_hash in malicious_hashes:
            print(f"[!] Malicious file detected: {filename}")
            # Uncomment below line to simulate deletion or quarantine
            # os.remove(file_path)
        else:
            print(f"[+] File is clean: {filename}")
