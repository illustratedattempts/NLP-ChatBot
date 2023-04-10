import sys
import os
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'nltk'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'google-api-python-client'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'urllib3'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-dotenv'])

# download nltk packages
test = "python -m nltk.downloader stopwords punkt wordnet"
os.system(test)
