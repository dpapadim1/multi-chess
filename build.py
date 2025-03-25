import shutil
import os
from app import freezer

# Define the build directory
build_dir = 'build'

# Remove the build directory if it exists
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

if __name__ == "__main__":
    freezer.freeze()
