import unittest
import os
import json
from modules import notes_manager

TEST_DATA_PATH = 'data/test_notes_data.json'
notes_manager.DATA_PATH = TEST_DATA_PATH  # Override for testing

class TestNotesManager(unittest.TestCase):
    def setUp(self):
        with open(TEST_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)

    def tearDown(self):
        if os.path.exists(TEST_DATA_PATH):
            os.remove(TEST_DATA_PATH)

    def test_add_note_and_load(self):
        notes_manager.add_note("Sample", "Content")
        notes = notes_manager.load_notes()
        self.assertTrue(any(note['title'] == "Sample" for note in notes))

    def test_edit_note(self):
        notes_manager.add_note("Title1", "Content1")
        notes_manager.edit_note(0, title="Edited Title")
        notes = notes_manager.load_notes()
        self.assertEqual(notes[0]['title'], "Edited Title")

    def test_delete_note(self):
        notes_manager.add_note("Will Delete", "Content")
        notes_manager.delete_note(0)
        notes = notes_manager.load_notes()
        self.assertEqual(len(notes), 0)

if __name__ == '__main__':
    unittest.main()
