import os

for dirpath, subdirs, files in os.walk('./data/185'):
    for x in files:
        if x.endswith(".psa"):
            os.system(f'pog -p {os.path.join(dirpath, x)}')
