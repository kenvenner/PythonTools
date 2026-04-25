import unittest
from unittest.mock import patch, MagicMock
import kvexcel
import os

import kvxls

"""
Test to add 2026-01-19

def get_existing_column_hidden( xls_filename, ws_sheetname = None, disp_msg=False ):

def apply_col_hidden_ws_obj( ws, col_hidden, disp_msg=True ):

changed
-def format_xlsx_with_filter_and_freeze( xls_filename, ws_sheetname=None, col_width=None, disp_msg=True ):
+def format_xlsx_with_filter_and_freeze( xls_filename, ws_sheetname=None, col_width=None, col_hidden=None, disp_msg=True ):

Possibly enhance this so we don't need to reopen the file between calls - we save the file and check for sameness?


"""


class TestUpdateExcelCells(unittest.TestCase):
    """Unit tests for kvexcel.update_excel_cells and related utilities."""

    @patch("kvexcel.win32.Dispatch")
    @patch("kvexcel.ensure_onedrive_file_local")
    def test_update_excel_cells_p01_basic(self, mock_ensure, mock_dispatch):
        """Test basic cell updates in Excel workbook."""
        mock_excel = MagicMock()
        mock_workbook = MagicMock()
        mock_sheet = MagicMock()
        mock_cell = MagicMock()

        # Excel workbook hierarchy (with __getitem__ enabled)
        mock_excel.Workbooks.Open.return_value = mock_workbook
        mock_workbook.Sheets.__getitem__.return_value = mock_sheet
        mock_sheet.Cells.__getitem__.return_value = mock_cell
        mock_dispatch.return_value = mock_excel

        kvexcel.update_excel_cells(
            "dummy.xlsx",
            [
                {"sheet": "Sheet1", "row": 1, "col": 1, "value": "A"},
                {"row": 2, "col": 2, "value": "B"},
            ],
        )

        mock_dispatch.assert_called_once_with("Excel.Application")
        mock_excel.Workbooks.Open.assert_called_once()
        mock_cell.Value = "B"  # should have been assigned last

    def test_update_excel_cells_p03_real_file(self):
        """Create file, update file, validate updates"""

        excel_file = "t_kvexcel.xlsx"

        # create the xlsx
        data = [
            {"Wine": "Cab", "Store": "Bevmo", "Price": 39.99},
            {"Wine": "Cab", "Store": "Total", "Price": 19.00},
            {"Wine": "Pinot", "Store": "Pavillions", "Price": 35.00},
        ]
        kvxls.writelist2xls(excel_file, data)

        # define the updates and expected results
        # remember row 1 is the header row
        updates = [
            {"row": 2, "col": 3, "value": 20},
            {"row": 4, "col": 2, "value": "Total"},
        ]
        data[0]["Price"] = 20
        data[2]["Store"] = "Total"

        # cause the onscreen updates
        kvexcel.update_excel_cells(excel_file, updates)

        # now read in the results
        results = kvxls.readxls2list(excel_file)

        # compare
        self.assertEqual(results, data)

        # cleanup
        os.remove(excel_file)

    def test_update_excel_cells_p04_basic(self, mock_ensure, mock_dispatch):
        """Test basic cell updates in Excel workbook."""
        mock_excel = MagicMock()
        mock_workbook = MagicMock()
        mock_sheet = MagicMock()
        mock_cell = MagicMock()

        # Excel workbook hierarchy (with __getitem__ enabled)
        mock_excel.Workbooks.Open.return_value = mock_workbook
        mock_workbook.Sheets.__getitem__.return_value = mock_sheet
        mock_sheet.Cells.__getitem__.return_value = mock_cell
        mock_dispatch.return_value = mock_excel

        kvexcel.update_excel_cells(
            "dummy.xlsx",
            [
                {"sheet": "Sheet1", "row": 1, "col": 1, "value": "A"},
                {"row": 2, "col": 2, "value": "B"},
            ],
        )

        mock_dispatch.assert_called_once_with("Excel.Application")
        mock_excel.Workbooks.Open.assert_called_once()
        mock_cell.Value = "B"  # should have been assigned last

    def test_update_excel_cells_f01_updates_empty(self):
        """Pass in invalid empty updates"""
        with self.assertRaises(Exception):
            kvexcel.update_excel_cells("dummy.xlsx", [])

    def test_update_excel_cells_f02_updates_dict(self):
        """Pass in invalid dict updates"""
        with self.assertRaises(Exception):
            kvexcel.update_excel_cells("dummy.xlsx", {"a": 1})

    def test_update_excel_cells_f03_updates_list_of_list(self):
        """Pass in invalid list of list updates"""
        with self.assertRaises(Exception):
            kvexcel.update_excel_cells("dummy.xlsx", [[1, 2, 3]])

    def test_update_excel_cells_f04_updates_missing_keys(self):
        """Pass in invalid list of dict missing keys updates"""
        with self.assertRaises(Exception):
            kvexcel.update_excel_cells("dummy.xlsx", [{"sheet": "sheet", "row": 1}])

    # tried mocking out the attribute - it works but it is clearer if we just test with a real and known file
    # def test_ensure_onedrive_file_local_p01_success(self, mock_exists, mock_GetFileAttributesW):
    # @patch("ctypes.windll.kernel32.GetFileAttributesW")
    @patch("kvexcel.Path.exists")
    def test_ensure_onedrive_file_local_p01_success(self, mock_exists):
        """Test ensure_onedrive_file_local returns successfully when file exists."""
        mock_exists.return_value = True
        # mock_GetFileAttributesW = 32
        # Should not raise
        kvexcel.ensure_onedrive_file_local("t_kvexcel.py")
        # kvexcel.ensure_onedrive_file_local("dummy.xlsx")

    @patch("kvexcel.Path.exists")
    def test_ensure_onedrive_file_local_f01_fail(self, mock_exists):
        """Test ensure_onedrive_file_local raises FileNotFoundError if missing."""
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            kvexcel.ensure_onedrive_file_local("dummy.xlsx")

    @patch("kvexcel.win32.Dispatch")
    @patch("kvexcel.ensure_onedrive_file_local")
    def test_update_excel_cells_f01_test_error_handling(
        self, mock_ensure, mock_dispatch
    ):
        """Test that exceptions inside Excel updates are raised."""
        mock_excel = MagicMock()
        mock_excel.Workbooks.Open.side_effect = Exception("Excel crash")
        mock_dispatch.return_value = mock_excel

        with self.assertRaises(Exception):
            kvexcel.update_excel_cells("bad.xlsx", [{"row": 2, "col": 2, "value": "B"}])

    ########################################
    # the function name: def normalize_excel_path(path: str) -> str:
    def test_normalize_excel_path_p01_pass(self):
        """Unix slashes converted to DOS"""
        result = kvexcel.normalize_excel_path("/path1/path2/path3")
        self.assertEqual(result, "path1\\path2\\path3")

    def test_normalize_excel_path_p02_pass(self):
        """https removal"""
        result = kvexcel.normalize_excel_path("https:\\mypath\\to\\file")
        # print(f"\n{result=}\n")
        self.assertEqual(result, "mypath\\to\\file")

    ########################################
    # the function name: def is_same_workbook(path1: str, path2: str) -> bool:
    # def test_is_same_workbook_p01_pass(self):
    ########################################
    # prior function: ensure_onedrive_file_local
    # the function name: def bring_excel_to_front(excel):
    # def test_bring_excel_to_front_p01_pass(self):


if __name__ == "__main__":
    unittest.main()
