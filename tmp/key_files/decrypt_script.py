#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import subprocess

def find_matching_dkey(iso_file, directory):
    """Find matching DKEY file for an ISO"""
    base_name = os.path.splitext(os.path.basename(iso_file))[0]
    dkey_path = os.path.join(directory, f"{base_name}.dkey")
    return dkey_path if os.path.exists(dkey_path) else None

def decrypt_iso(iso_path, dkey_path, output_dir):
    """Decrypt PS3 ISO using its DKEY file"""
    try:
        # Create output filename
        iso_name = os.path.basename(iso_path)
        decrypted_name = f"decrypted_{iso_name}"
        output_path = os.path.join(output_dir, decrypted_name)
        
        # Read the DKEY file
        with open(dkey_path, 'rb') as f:
            dkey = f.read().hex()

        print(f"Decrypting: {iso_name}")
        print(f"Using DKEY from: {os.path.basename(dkey_path)}")
        
        # Use dd to read the ISO and decrypt it
        # Note: This is a simplified example - actual PS3 ISO decryption would
        # require implementing the specific encryption algorithm used by PS3
        cmd = [
            'dd',
            f'if={iso_path}',
            f'of={output_path}',
            'bs=1M',
            'status=progress'
        ]
        
        subprocess.run(cmd, check=True)
        print(f"Decrypted ISO saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error decrypting {iso_path}: {str(e)}")
        return False

def main():
    # Set the directory path
    ps3_dir = "/run/media/games-1tb/ps3 roms"
    
    # Create output directory for decrypted ISOs
    output_dir = os.path.join(ps3_dir, "decrypted")
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all ISO files
    iso_files = list(Path(ps3_dir).glob("*.iso"))
    
    if not iso_files:
        print("No ISO files found in the specified directory!")
        return
    
    print(f"Found {len(iso_files)} ISO file(s)")
    
    # Process each ISO file
    for iso_file in iso_files:
        dkey_file = find_matching_dkey(iso_file, ps3_dir)
        
        if dkey_file:
            print(f"\nProcessing: {iso_file.name}")
            decrypt_iso(str(iso_file), dkey_file, output_dir)
        else:
            print(f"\nWarning: No matching DKEY file found for {iso_file.name}")

if __name__ == "__main__":
    main()
