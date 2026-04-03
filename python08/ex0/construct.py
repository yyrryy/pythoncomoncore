import sys
import os
import site

if __name__ == "__main__":
    # sys.prefix is set to venv path inside a virtual env.
    # sys.base_prefix points to the original Python installation.
    if sys.base_prefix != sys.prefix:
        print("MATRIX STATUS: Welcome to the construct")
        print(f"\nCurrent Python: {sys.executable}")
        print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
        print(f"Environment Path: {sys.prefix}")
        print("\nSUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print("\nPackage installation path:")
        site_packages = site.getsitepackages()
        print(site_packages[0])

    else:
        print("MATRIX STATUS: You're still plugged in")
        print(f"\nCurrent Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")
        print("\nTo enter the construct, run:")
        print("python3 -m venv matrix_env")
        print("matrix_env\\Scripts\\activate  # On Windows")
        print("source matrix_env/bin/activate  # On Unix")
        print("\nThen run this program again.")
