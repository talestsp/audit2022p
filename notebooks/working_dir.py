import os


def set_wd(path=None):
    if path is None:
        work_dir_split = os.getcwd().split("/")

        if "notebooks" in work_dir_split:
            notebooks_dir_i = work_dir_split.index("notebooks")
            os.chdir("/".join(work_dir_split[0:notebooks_dir_i]))
    else:
        os.chdir(path)

def get_wd():
    return os.getcwd()