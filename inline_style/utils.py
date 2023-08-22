import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_folder = os.path.join(current_dir, "course/common/libs")
sys.path.append(lib_folder)