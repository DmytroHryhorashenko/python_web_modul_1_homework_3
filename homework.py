
import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count
import time
import sys


def copy_file(file_path: Path, target_dir: Path):
    ext = file_path.suffix[1:] or "no_ext"
    dest_folder = target_dir / ext
    dest_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, dest_folder)

def process_directory(src_dir: Path, target_dir: Path):

    with ThreadPoolExecutor() as executor:
        for entry in src_dir.iterdir():
            if entry.is_file():
                executor.submit(copy_file, entry, target_dir)
            elif entry.is_dir():
                executor.submit(process_directory, entry, target_dir)


def factorize_number(n: int):
    """Повертає список дільників числа n"""
    return [i for i in range(1, n + 1) if n % i == 0]

def factorize_sync(*numbers):
    return [factorize_number(n) for n in numbers]

def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        return pool.map(factorize_number, numbers)


def main():

    src_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("Хлам")
    dst_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")
    dst_path.mkdir(parents=True, exist_ok=True)
    print(f"Sorting files from {src_path} to {dst_path} ...")
    process_directory(src_path, dst_path)
    print("Files sorted by extension successfully!\n")


    numbers = (128, 255, 99999, 10651060)

    print("Synchronous factorization...")
    start = time.time()
    sync_result = factorize_sync(*numbers)
    print(sync_result)
    print("Time:", time.time() - start)

    print("\nParallel factorization using all CPU cores...")
    start = time.time()
    parallel_result = factorize_parallel(*numbers)
    print(parallel_result)
    print("Time:", time.time() - start)


    a, b, c, d = sync_result
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print("\nAll tests passed!")

if __name__ == "__main__":
    main()