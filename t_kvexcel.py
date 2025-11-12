import unittest
from unittest.mock import patch, MagicMock
import kvexcel


class TestUpdateExcelCells(unittest.TestCase):
    """Unit tests for kvexcel.update_excel_cells and related utilities."""

    @patch("kvexcel.win32.Dispatch")
    @patch("kvexcel.ensure_onedrive_file_local")
    def test_update_cells_basic(self, mock_ensure, mock_dispatch):
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

        kvexcel.update_excel_cells("dummy.xlsx", {"Sheet1": {"A1": "A", "B2": "B"}})

        mock_dispatch.assert_called_once_with("Excel.Application")
        mock_excel.Workbooks.Open.assert_called_once()
        mock_cell.Value = "B"  # should have been assigned last

    @patch("kvexcel.win32.Dispatch")
    @patch("kvexcel.ensure_onedrive_file_local")
    def test_detects_already_open_workbook(self, mock_ensure, mock_dispatch):
        """Test behavior when workbook is already open in Excel."""
        mock_excel = MagicMock()
        mock_workbook = MagicMock()
        mock_sheet = MagicMock()

        # Simulate Excel open failure and fallback to existing workbook
        mock_excel.Workbooks.Open.side_effect = Exception("Already open")
        mock_excel.Workbooks.__getitem__.return_value = mock_workbook
        mock_workbook.Sheets.__getitem__.return_value = mock_sheet
        mock_dispatch.return_value = mock_excel

        kvexcel.update_excel_cells("dummy.xlsx", {"Sheet1": {"A1": "test"}})
        mock_dispatch.assert_called_once_with("Excel.Application")
        mock_workbook.Sheets.__getitem__.assert_called_with("Sheet1")

    @patch("kvexcel.os.path.exists")
    def test_ensure_onedrive_file_local_success(self, mock_exists):
        """Test ensure_onedrive_file_local returns successfully when file exists."""
        mock_exists.return_value = True
        # Should not raise
        kvexcel.ensure_onedrive_file_local("dummy.xlsx")

    @patch("kvexcel.os.path.exists")
    def test_ensure_onedrive_file_local_fail(self, mock_exists):
        """Test ensure_onedrive_file_local raises FileNotFoundError if missing."""
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            kvexcel.ensure_onedrive_file_local("dummy.xlsx")

    @patch("kvexcel.win32.Dispatch")
    @patch("kvexcel.ensure_onedrive_file_local")
    def test_error_handling(self, mock_ensure, mock_dispatch):
        """Test that exceptions inside Excel updates are raised."""
        mock_excel = MagicMock()
        mock_excel.Workbooks.Open.side_effect = Exception("Excel crash")
        mock_dispatch.return_value = mock_excel

        with self.assertRaises(Exception):
            kvexcel.update_excel_cells("bad.xlsx", {"Sheet1": {"A1": "X"}})


if __name__ == "__main__":
    unittest.main()
