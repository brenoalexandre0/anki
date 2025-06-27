import unittest
from unittest.mock import MagicMock, patch
from aqt.exporting import ExportDialog
from pylib.anki.decks import DeckManager
from pylib.anki.collection import Collection
from aqt.main import AnkiQt
from aqt.forms.exporting import Ui_ExportDialog
from aqt.qt import QDialog, QPushButton

class TestSetupMethod(unittest.TestCase):

    def setUp(self):
        self.mock_col = MagicMock(spec=Collection)
        self.mock_mw = MagicMock(spec=AnkiQt)
        self.mock_mw.col = self.mock_col
        self.dialog = ExportDialog(self.mock_mw)
        self.dialog.frm = MagicMock(spec=Ui_ExportDialog)
        self.dialog.frm.format = MagicMock()
        self.dialog.frm.deck = MagicMock()
        self.dialog.frm.buttonBox = MagicMock()
        self.dialog.cids = None

    @patch("aqt.exporting.exporters")
    def test_CT1_did_none_cids_none(self, mock_exporters):
        mock_exporters.return_value = [("Text", MagicMock(ext=".txt"))]
        self.dialog.cids = None
        self.dialog.setup(did=None)

        self.assertEqual(self.dialog.frm.format.setCurrentIndex.call_args[0][0], 0)
        self.assertIn("All decks", self.dialog.decks[0])

    @patch("aqt.exporting.exporters")
    def test_CT2_did_given_cids_none(self, mock_exporters):
        mock_exporters.return_value = [("APKG", MagicMock(ext=".apkg"))]
        self.dialog.cids = None
        self.mock_col.decks.get.return_value = {"name": "TestDeck"}
        self.dialog.frm.deck.findText.return_value = 1

        self.dialog.setup(did=1234)

        self.assertEqual(self.dialog.frm.format.setCurrentIndex.call_args[0][0], 0)
        self.assertEqual(self.dialog.frm.deck.setCurrentIndex.call_args[0][0], 1)

    @patch("aqt.exporting.exporters")
    def test_CT3_did_none_cids_given(self, mock_exporters):
        mock_exporters.return_value = [("APKG", MagicMock(ext=".apkg"))]
        self.dialog.cids = [10, 20]

        self.dialog.setup(did=None)

        self.assertEqual(self.dialog.frm.format.setCurrentIndex.call_args[0][0], 0)
        self.assertEqual(self.dialog.decks[0], "Selected notes")

    @patch("aqt.exporting.exporters")
    def test_CT4_did_given_cids_given(self, mock_exporters):
        mock_exporters.return_value = [("APKG", MagicMock(ext=".apkg"))]
        self.dialog.cids = [10, 20]
        self.mock_col.decks.get.return_value = {"name": "TestDeck"}
        self.dialog.frm.deck.findText.return_value = 2

        self.dialog.setup(did=5678)

        self.assertEqual(self.dialog.frm.format.setCurrentIndex.call_args[0][0], 0)
        self.assertEqual(self.dialog.decks[0], "Selected notes")
        self.assertEqual(self.dialog.frm.deck.setCurrentIndex.call_args[0][0], 2)

if __name__ == '__main__':
    unittest.main()
