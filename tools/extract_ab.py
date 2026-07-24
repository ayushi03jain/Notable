#!/usr/bin/env python3
import sys
import os
import io
import tarfile
import zlib
import gzip

def extract_ab(ab_path, out_dir):
    with open(ab_path, 'rb') as f:
        # Read header lines
        header_lines = []
        for i in range(3):
            line = f.readline()
            if not line:
                break
            header_lines.append(line.decode('utf-8', errors='replace').strip())

        if not header_lines or not header_lines[0].startswith('ANDROID BACKUP'):
            print('Not an android backup file')
            return 2

        # compression method is the 3rd header line (index 2)
        compression = header_lines[2] if len(header_lines) > 2 else 'none'
        payload = f.read()

        # handle no compression, gzip, or zlib
        if compression == 'none':
            tar_bytes = payload
        else:
            # try gzip first
            try:
                tar_bytes = gzip.decompress(payload)
            except Exception:
                try:
                    tar_bytes = zlib.decompress(payload)
                except Exception as e:
                    print('Failed to decompress payload:', e)
                    return 3

        # write tar to memory and extract
        tarf = tarfile.open(fileobj=io.BytesIO(tar_bytes))
        tarf.extractall(path=out_dir)
        print('Extracted to', out_dir)
        return 0

def main():
    if len(sys.argv) < 3:
        print('Usage: extract_ab.py <backup.ab> <out_dir>')
        return 1
    ab_path = sys.argv[1]
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    return extract_ab(ab_path, out_dir)

if __name__ == '__main__':
    sys.exit(main())
