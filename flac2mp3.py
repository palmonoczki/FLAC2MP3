import os
import sys
import shutil
import subprocess

def convert_flac_to_mp3_ffmpeg(source_path, dest_path):
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", source_path,
            "-ab", "320k", "-map_metadata", "0", "-id3v2_version", "3", dest_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Converted: {source_path} -> {dest_path}")
    except subprocess.CalledProcessError:
        print(f"Failed to convert: {source_path}")

def process_directory(src_root, dst_root):
    for root, _, files in os.walk(src_root):
        rel_path = os.path.relpath(root, src_root)
        target_dir = os.path.join(dst_root, rel_path)
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            if file.lower().endswith(".flac"):
                dst_file = os.path.join(target_dir, os.path.splitext(file)[0] + ".mp3")
                convert_flac_to_mp3_ffmpeg(src_file, dst_file)
            else:
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)
                print(f"Copied: {src_file} -> {dst_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python flac2mp3_ffmpeg.py <source_directory> <destination_directory>")
        sys.exit(1)

    source_dir = sys.argv[1]
    destination_dir = sys.argv[2]
    process_directory(source_dir, destination_dir)
