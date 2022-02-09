# get cwd
#
# wzzk through folders
# get date of file
# move file to correct month
# if cannot-- log error

#

import datetime
import os
import pathlib

cwd = os.getcwd()


os.walk(cwd)

errorFound = False

for cur_path, dir_list, file_list in os.walk(cwd):
    for file in file_list:
        # print(f'filename: {file}')
        if file.split(".")[-1] == "pdf":
            fullpath = os.path.join(cur_path, file)
            file_p = pathlib.Path(fullpath)
            modified_time = datetime.datetime.fromtimestamp(file_p.stat().st_mtime)
            new_location = os.path.join(
                cwd, str(modified_time.year), str(modified_time.month)
            )
            new_path = os.path.join(new_location, file)

            if not os.path.isdir(new_location):
                pathlib.Path(new_location).mkdir(parents=True)
            with open("errors.txt", "a") as err_file:

                try:
                    os.replace(fullpath, new_path)
                except OSError:
                    errorFound = True
                    print(OSError)
                    err_file.write(f"failed\t{fullpath}\t{OSError}\n")
                except Exception as ex:
                    errorFound = True
                    err_file.write(
                        f"failed\t{fullpath}\tunknown error: {type(ex).__name__}\n"
                    )
if not errorFound:
    print("files have been sorted")
else:
    print("At least one error occurred, Check error log")
