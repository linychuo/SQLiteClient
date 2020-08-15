import os
import shutil
import subprocess


def package():
    cur_dir = os.path.dirname(__file__)
    return subprocess.call([
        'python',
        '-OO',
        '-m',
        'PyInstaller',
        '-w',
        '-F',
        # '-i',
        # os.path.abspath(os.path.join(cur_dir, '../resources',
        #                              'favicon.ico')), '--version-file',
        # os.path.abspath(os.path.join(cur_dir, 'file_version_info.txt')),
        '--name',
        'SQLiteClient',
        '--distpath',
        os.path.abspath(os.path.join(cur_dir, '..', '..', 'dist')),
        os.path.abspath(os.path.join(cur_dir, '..', 'app.py'))
    ])


if __name__ == '__main__':
    if package() == 0:
        if os.path.exists("./build"):
            shutil.rmtree('./build')
        if os.path.exists("./SQLiteClient.spec"):
            os.remove('./SQLiteClient.spec')
