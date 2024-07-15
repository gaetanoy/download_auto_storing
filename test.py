import unittest
import os


class MyTestCase(unittest.TestCase):
    def test_main_directory_exists(self):
        self.directory_exists(r'C:\Users\UX325\Downloads')

    def directory_exists(self, directory):
        self.assertTrue(os.path.exists(directory))

    def test_image_directory_exists(self):
        self.directory_exists(r'C:\Users\UX325\Pictures\Images téléchargées')

    def test_document_directory_exists(self):
        self.directory_exists(r'C:\Users\UX325\Documents\Téléchargements\Documents téléchargés')

    def test_executable_directory_exists(self):
        self.directory_exists(r'C:\Users\UX325\Documents\Téléchargements\Executables téléchargés')

    def test_zip_directory_exists(self):
        self.directory_exists(r'C:\Users\UX325\Documents\Téléchargements\Zip téléchargés')

    def test_program_directory_exists(self):
        self.directory_exists(r'C:\Users\UX325\Documents\Téléchargements\Codes téléchargés\Programmes')

    def test_database_directory_exists(self):
        self.directory_exists(r'C:\Users\UX325\Documents\Téléchargements\Codes téléchargés\BD')

    def test_other_directory_exists(self):
        self.directory_exists(r'C:\Users\UX325\Documents\Téléchargements\Autres fichiers téléchargés')


if __name__ == '__main__':
    unittest.main()
