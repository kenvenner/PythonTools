"""
@author:   Ken Venner
@contact:  ken@venerllc.com
@version: 1.04

Library of tools used to read excel files with the native desktop application excel COM  connection

This enables a shared xlsx to be updated in real time through the Excel UI - rather than driving updates through openpyxl

The major function called:
update_excel_cells - open xlsx, and update list of row/col/value/optionally-sheet, and save updates

pip install pywin32


"""

import time
from pathlib import Path
import ctypes
import win32com.client as win32


def normalize_excel_path(path: str) -> str:
    """
    Normalize paths returned by Excel COM to match local filesystem paths.
    Handles forward slashes, accidental https:\\ prefixes, and duplicate backslashes.
    """
    # take Unix slashes and make them DOS slashes
    s = str(path).replace("/", "\\")
    # Strip any accidental https:\ prefix
    if "https:\\" in s.lower():
        s = s.split("https:\\")[-1]
    # Remove empty segments from duplicated backslashes
    s = "\\".join(part for part in s.split("\\") if part)
    return s.lower()  # Windows paths are case-insensitive


def is_same_workbook(path1: str, path2: str) -> bool:
    """
    Robust comparison of Excel workbook paths.
    Compares normalized, lower-cased paths to avoid issues with OneDrive and Excel COM.
    """
    try:
        p1 = normalize_excel_path(path1)
        p2 = normalize_excel_path(path2)
        return p1.endswith(p2) or p2.endswith(p1)
    except Exception:
        # any type of failure they are not the same but we swallow the error
        return False


def ensure_onedrive_file_local(filename: str, timeout: int = 5):
    """
    Ensure a OneDrive file is locally available.
    Handles files in OneDrive folders properly.
    """
    # convert string to Path object
    fpath = Path(filename)

    # If the path looks like a URL, raise error
    if str(fpath).lower().startswith(("http://", "https://")):
        raise ValueError(f"Excel COM cannot open a URL: {filename}")

    # Detect if path contains a mistakenly prepended https:\ (OneDrive issue)
    if "https:\\" in str(fpath).lower():
        # Strip everything before the last valid local path
        parts = str(fpath).split("https:\\")[-1].replace("/", "\\")
        fpath = Path(parts)
        if not fpath.is_absolute():
            fpath = (Path.cwd() / fpath).resolve()
    else:
        if not fpath.is_absolute():
            fpath = (Path.cwd() / fpath).resolve()
        else:
            fpath = fpath.resolve()

    # Wait until OneDrive makes file local
    start = time.time()
    while True:
        if fpath.exists():
            try:
                attrs = ctypes.windll.kernel32.GetFileAttributesW(str(fpath))
                if not (attrs & 0x1000):  # FILE_ATTRIBUTE_OFFLINE
                    return fpath
            except Exception as e:
                print(f"ctypes error: {e}")
                pass
        if time.time() - start > timeout:
            raise FileNotFoundError(f"File not available locally: {fpath}")
        time.sleep(0.1)


def bring_excel_to_front(excel):
    """Bring Excel window to front if visible."""
    try:
        hwnd = excel.Application.Hwnd
        ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    except Exception:
        # if we have a failure we eat it and move on
        pass


def update_excel_cells(
    filename: str,
    updates: list[dict],
    visible: bool = True,
    leave_open: bool = False,
    disp_msg: bool = True,
):
    """
    Update Excel cells. Auto-close workbook if opened by this script.

    updates = [
        {'sheet':'Sheet1', 'row':1,'col':1,'value':'X'},
         ...,
    ]

    filename - name/path to the excel file to be worked in
    updates - list of dict changes as defined above
    visible - bool, when true we make the chnages visible that are taking place
    leave_open - bool, when true, we do NOT close this file after we are doing processing
                       when false, and we open the file with this script - then close the file when done
    disp_msg - bool, when true, we print to console messagers we are progress
    """
    # tests inputs
    if not updates:
        raise ValueError("updates must be populated")
    if not isinstance(updates, list):
        raise TypeError(f"updates must be list but is: {type(updates)}")
    if not isinstance(updates[0], dict):
        raise TypeError(f"updates[0] must be dict but is:  {type(updates[0])}")
    # see if the updates definitions has the right set of keys
    # did not check for sheet as it is NOT a required field
    missingkeys = [x for x in ("row", "col", "value") if x not in updates[0].keys()]
    if missingkeys:
        raise ValueError(f"updates[0] missing following keys: {','.join(missingkeys)}")

    # local variables
    opened_excel = False

    # display message
    if disp_msg:
        print(f"DEBUG: filename received = {filename}")

    # get the absolute path to this file and assure it is locally available
    abs_path = str(ensure_onedrive_file_local(filename))

    # start up excel as a COM object
    try:
        excel = win32.GetActiveObject("Excel.Application")
        if disp_msg:
            print("Attached to existing Excel instance.")
    except Exception:
        excel = win32.Dispatch("Excel.Application")
        opened_excel = True
        if disp_msg:
            print("Started new Excel instance.")

    # let excel know if it should be visible
    excel.Visible = visible

    # set the local variables
    workbook = None
    _opened_by_script = False

    # Check if workbook is already open (robust)
    # step through all the open work books and see if we have already opened this file
    for wb in excel.Workbooks:
        if is_same_workbook(wb.FullName, abs_path):
            # the desired workbook is already open in Excel - save this
            workbook = wb
            if disp_msg:
                print(f"Workbook already open: {abs_path}")
            # and break out we found the already open instance
            break

    # We did nto find the workbook so we now need to open it
    if workbook is None:
        # open the desired workbook
        workbook = excel.Workbooks.Open(abs_path)
        # and set the flag that we opened it to true
        _opened_by_script = True
        if disp_msg:
            print(f"Opened workbook: {abs_path}")

    # if the user wanted to see the changes, then bring forward this window
    if visible:
        bring_excel_to_front(excel)

    # Update cells based on information in updates
    for upd in updates:
        # pull out the values of interest - optionally pull sheet
        sheet_name = upd.get("sheet")
        # the following fields are required and the script will fail if they don't exist in the dictionary
        row = upd["row"]
        col = upd["col"]
        value = upd["value"]
        # make the updates
        try:
            # if sheet is populated - change to that sheet in this workbook - otherwise we just work the active sheet
            ws = workbook.Sheets(sheet_name) if sheet_name else workbook.ActiveSheet
            # set the value in the defined cell
            ws.Cells(row, col).Value = value
            if disp_msg:
                print(
                    f"Updated {sheet_name or 'ActiveSheet'} cell ({row},{col}) = {value}"
                )
        except Exception as e:
            if disp_msg:
                print(f"Failed to update cell ({row},{col}): {e}")

    # Save workbook
    try:
        workbook.Save()
        if disp_msg:
            print(f"Workbook saved: {abs_path}")
    except Exception as e:
        if disp_msg:
            print(f"Failed to save workbook: {e}")
        raise

    # Close if we opened it
    if _opened_by_script and not leave_open:
        workbook.Close(SaveChanges=True)
        if disp_msg:
            print(f"Workbook closed: {abs_path}")

    # if we opened excel we may want to close it
    if opened_excel:
        excel.Quit()
        if disp_msg:
            print("Quit Excel")


if __name__ == "__main__":
    test_file = r"test.xlsx"  # Local file in current dir (OneDrive folder)
    updates = [
        {"sheet": "Sheet1", "row": 1, "col": 1, "value": "Hello"},
        {"sheet": "Sheet1", "row": 2, "col": 1, "value": "World"},
    ]

    try:
        update_excel_cells(test_file, updates, visible=True, disp_msg=True)
        print("Excel update completed successfully.")
    except Exception as e:
        print(f"Error updating Excel: {e}")
