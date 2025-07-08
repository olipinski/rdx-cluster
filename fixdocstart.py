import os
import subprocess
from pathlib import Path

def insertDocumentStart(path):
    p = Path(path)
    contents = p.read_text(encoding='utf8')
    contents = '---\n' + contents
    p.write_text(contents, encoding='utf8')
    return contents

for subdir, dirs, filenames in os.walk("./"):
    for filename in filenames:
        if not filename.endswith('.yml') and not filename.endswith('.yaml'):
            continue

        if filename == 'vault.yaml':
            continue

        path = os.path.join(subdir, filename)

        proc = subprocess.run(
            f'yamllint --strict "{path}"',
            shell=True,
            stdout=subprocess.PIPE,
            encoding='utf8'
        )

        if 'missing document start' in proc.stdout:
            print('Inserting document start to:', path)
            insertDocumentStart(path)

        # Rename .yaml to .yaml
        if filename.endswith('.yml'):
            new_filename = filename[:-4] + '.yaml'
            new_path = os.path.join(subdir, new_filename)
            os.rename(path, new_path)
            print(f'Renamed {path} to {new_path}')

