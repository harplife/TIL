import os
from shutil import copyfile

# homepath doesn't work unless current working directory is within default drive
os.chdir(os.getenv('HOMEDRIVE'))
# go to user folder
workspace = os.getenv('HOMEPATH')
# set user folder as workspace
os.chdir(workspace)
# create a folder named 'assets' in user folder
# pictures will be saved to this folder
target_fn = 'assets'
if not os.path.exists(target_fn):
    os.mkdir(target_fn)
# move to assets folder
os.chdir(target_fn)
target_folder = os.getcwd()

# this is where Windows keep those nice pictures
assets_folder = os.path.join(os.getenv('LocalAppData'), 'Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets')

n = 0
for _dir, _subdirs, files in os.walk(assets_folder):
    for file in files:
        old_fn = os.path.join(assets_folder, file)
        new_fn = os.path.join(target_folder, '.jpg')
        n += 1
        copyfile(old_fn, new_fn)
        # os.rename(old_fn, new_fn)  # this is pretty much cut
    print(n, 'files have been copied to', target_folder)