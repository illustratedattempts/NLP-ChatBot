import sys
import os
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'nltk'])

# download nltk packages
test = "python -m nltk.downloader stopwords punkt wordnet"
os.system(test)
