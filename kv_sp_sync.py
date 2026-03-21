"""
@author:   Ken Venner
@contact:  ken.venner@hermeus.com
@version: 1.19

This library provides tools used when interacting with sharepoint sites and local synch links to sharepoint sites

"""

import os

# global variables
AppVersion = "1.19"

ONEDRIVE_DIR_OPTIONS_BY_OS_NAME = {
    "nt": [
        "Hermeus Corp/",
        "OneDrive - Hermeus Corp/",
    ],
    "posix": [
        "Library/CloudStorage/OneDrive-SharedLibraries-HermeusCorp/",
    ],
}


def sp_synced_dir_path(
    sp_path: str,
    onedrive_path: str | None = None,
    local_path: str | None = None,
    debug=False,
) -> str:
    """
    For mac and windows return back the path to the synched folder in sharepoint of interest

    sp_path - the sharepoint name and folder path to the directory of interest
       e.g.:  "/NetSuite Implementation - Documents/Master Mapping Files/output/"
    onedrive_path - the path from HOME/HOMEPATH to the location where sharepoint files are synched
       can be empty - will default if not set
    local_path - the path to return if the sp path does not exist

    requires:  import os

    return - os.path object to the synched folder or returns local_path if synched folder does not exist

    requires:  import os
    """

    # strip the starting dir
    if sp_path and sp_path[0] in "/\\":
        sp_path = sp_path[1:]

    # not the default path - make sure the path does not start with dir symbol
    if onedrive_path and onedrive_path[0] in "/\\":
        onedrive_path = onedrive_path[1:]

    # calculate the homedir for this user
    home_dir = ""

    # Define the master directory path using the home directory
    if os.name == "posix":
        home_dir = os.environ.get("HOME")
    else:
        home_dir = os.environ.get("HOMEPATH")

    # debugging outputs
    if debug:
        print("home_dir", home_dir)
        print("onedrive_path", onedrive_path)
        print("sp_path", sp_path)

    # make the path the concatenation of the parts
    if onedrive_path:
        sp_full_path = os.path.join(home_dir, onedrive_path, sp_path)
    else:
        # determine which works
        for onedrive_path in ONEDRIVE_DIR_OPTIONS_BY_OS_NAME[os.name]:
            # calculate it
            sp_full_path = os.path.join(home_dir, onedrive_path, sp_path)
            # check to see if it exists
            if os.path.exists(sp_full_path):
                # it exists - get out
                break

    # debugging outputs
    if debug:
        print("sp_full_path:", sp_full_path)

    # check for existance of this sharepoint path, or the local_path was not set
    if os.path.exists(sp_full_path) or not local_path:
        return sp_full_path
    else:
        return local_path


# eof
