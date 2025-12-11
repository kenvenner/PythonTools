"""
@author:   Ken Venner
@contact:  ken@venerllc.com
@version:  1.03

Library of tools used to read excel files with the native desktop application excel

update_excel_cells - open xlsx, and update list of row/col/value/optionally-sheet, and save updates

pip install pywin32


"""

import time
from pathlib import Path
import ctypes
import win32com.client as win32

def normalize_excel_path(path: str) -> str:
    r"""
    Normalize paths returned by Excel COM to match local filesystem paths.
    Handles forward slashes, accidental https:\ prefixes, and duplicate backslashes.
    """
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
    except Exception as e:
        return False

def ensure_onedrive_file_local(filename: str, timeout=5):
    """
    Ensure a OneDrive file is locally available.
    Handles files in OneDrive folders properly.
    """
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
    except Exception as e:
        pass

def update_excel_cells(filename: str, updates: list[dict], visible: bool=True, leave_open: bool=False, disp_msg: bool=True):
    """
    Update Excel cells. Auto-close workbook if opened by this script.
    updates = [{'sheet':'Sheet1', 'row':1,'col':1,'value':'X'}, ...]

    filename - name/path to the excel file to be worked in
    updates - list of dict changes as defined above
    visible - bool, when true we make the chnages visible that are taking place
    leave_open - bool, when true, we do NOT close this file after we are doing processing
                       when false, and we open the file with this script - then close the file when done
    disp_msg - bool, when true, we print to console messagers we are progress
    """
    if disp_msg:
        print(f"DEBUG: filename received = {filename}")

    abs_path = str(ensure_onedrive_file_local(filename))

    try:
        excel = win32.GetActiveObject("Excel.Application")
        if disp_msg:
            print("Attached to existing Excel instance.")
    except Exception as e:
        excel = win32.Dispatch("Excel.Application")
        if disp_msg:
            print("Started new Excel instance.")

    excel.Visible = visible

    workbook = None
    _opened_by_script = False

    # Check if workbook is already open (robust)
    for wb in excel.Workbooks:
        if is_same_workbook(wb.FullName, abs_path):
            workbook = wb
            if disp_msg:
                print(f"Workbook already open: {abs_path}")
            break

    # Open workbook if not already open
    if workbook is None:
        workbook = excel.Workbooks.Open(abs_path)
        _opened_by_script = True
        if disp_msg:
            print(f"Opened workbook: {abs_path}")

    if visible:
        bring_excel_to_front(excel)

    # Update cells
    for upd in updates:
        sheet_name = upd.get("sheet")
        row = upd["row"]
        col = upd["col"]
        value = upd["value"]
        try:
            ws = workbook.Sheets(sheet_name) if sheet_name else workbook.ActiveSheet
            ws.Cells(row, col).Value = value
            if disp_msg:
                print(f"Updated {sheet_name or 'ActiveSheet'} cell ({row},{col}) = {value}")
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


if __name__ == "__main__":
    test_file = r"test.xlsx"  # Local file in current dir (OneDrive folder)
    updates = [
        {"sheet": "Sheet1", "row": 1, "col": 1, "value": "Hello"},
        {"sheet": "Sheet1", "row": 2, "col": 1, "value": "World"}
    ]

    try:
        update_excel_cells(test_file, updates, visible=True, disp_msg=True)
        print("Excel update completed successfully.")
    except Exception as e:
        print(f"Error updating Excel: {e}")
