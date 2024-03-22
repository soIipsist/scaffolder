import unittest
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parent_directory) 

from templates.python_template.tests.test_base import TestBase, run_test_methods

from src.scaffold import *
from src.update import *
from src.settings import *
from src.licenses import *
from src.templates import *
from src.constants import *

from templates.python_template.utils.file_operations import overwrite_file

licenses = ['mit', 'afl-3.0']
target_directory = os.getcwd()
author = 'soIipsis'

class TestScaffolder(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.template_directory = template_directory
        self.project_directory = project_directory
        self.license = license
        self.author = author
        self.git_username = git_username
        self.create_repository = create_repository
        self.repository_visibility = repository_visibility
        self.parameters = ['template_directory', 'license']

        self.update_source_directory = update_source_directory
        self.update_destination_directory = update_destination_directory
        self.update_files = update_files

        self.test_files_dir = self.get_test_files_dir()
        self.test_files_dir_2 = self.get_test_files_dir('dir2')


    def get_test_files_dir(self, dirname:str = 'dir1', language='python'):
        target_dir = {
            'python': 'python_test_files',
            'java': 'java_test_files'
        }
        return os.path.join(os.getcwd(), target_dir.get(language), dirname)
    
    def test_get_files_dir(self):
        dir1 = self.get_test_files_dir()
        print(dir1)
        self.assertTrue(os.path.exists(dir1))

        dir2 = self.get_test_files_dir('dir2')
        print(dir2)
        self.assertTrue(os.path.exists(dir2))

    def test_get_licenses(self):
        paths = get_license_paths(licenses)
        self.assertTrue(len(paths) > 0)

        print(paths)
        new_licenses = ['red']
        paths = get_license_paths(new_licenses)
        self.assertTrue(len(paths) == 0)

    def test_view_license(self):
        # test singular
        paths = view_license('mit')
        self.assertTrue(len(paths) > 0)

        # test multiple
        paths = view_license(licenses)
        self.assertTrue(len(paths) > 0)

        # test invalid license
        paths = view_license(['no'])
        self.assertTrue(len(paths) == 0)

    def test_view_all_licenses(self):
        paths = view_license()
        self.assertIsNotNone(paths)

    def test_create_license(self):
        license = 'mit'
        path = create_license(license=license, target_directory=target_directory, author=author)
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))

    def test_scaffold_local(self):
        self.create_repository = False
        self.repository_visibility = 0
        scaffold(self.template_directory, self.project_directory, self.license, self.author, self.git_username, self.create_repository, self.repository_visibility)
        self.assertTrue(os.path.exists(self.project_directory))

    def test_scaffold(self):
        self.create_repository = True
        self.repository_visibility = 1
        scaffold(self.template_directory, self.project_directory, self.license, self.author, self.git_username, self.create_repository, self.repository_visibility)

    def test_scaffold_update(self):
        # test with repo that already exists
        self.assertTrue(git_repo_exists(self.project_directory))
        scaffold(self.template_directory, self.project_directory, self.license, self.author, self.git_username, self.create_repository, self.repository_visibility)


    def test_update_python(self):
        self.update_files = []
        self.update_source_directory = self.get_test_files_dir()
        self.update_destination_directory = self.get_test_files_dir('dir2')

        print(self.update_source_directory)

        # try with no update files given
        source_files, funcs, updated_content = update(self.update_files, self.update_source_directory, self.update_destination_directory)
        
    def test_update_java(self):
        self.update_files = []
        self.update_source_directory = self.get_test_files_dir(language='java')
        self.update_destination_directory = self.get_test_files_dir('dir2', 'java')

        # try with no update files given
        source_files, funcs, updated_content = update(self.update_files, self.update_source_directory, self.update_destination_directory, language='java')


    def test_find_and_replace_in_directory(self):
        # create a file called red.txt with some text
        file_path = os.path.join(self.test_files_dir, "red.txt")
        file_content =  "hello red"
        overwrite_file(file_path, file_content)

        content = read_file(file_path)
        self.assertTrue(file_content == content)
        find_and_replace_in_directory(self.test_files_dir, "red", "blue")


    def test_settings(self):
        settings = list_settings(self.parameters)
        self.assertIsNotNone(settings)
        self.assertListEqual(list(settings.keys()), self.parameters)

    
    def test_list_templates(self):
        templates = list_templates()
        print(templates)
    
    def test_add_template(self):
        template_directory = '/Users/p/Desktop/template_example'
        template_name = None
        add_template(template_directory, template_name)
    
    def test_delete_template(self):
        indices = delete_template('template_example')
        self.assertTrue(len(indices) > 0)

    def test_get_template_directory(self):
        template_dir = get_template_directory('python_template')
        print(template_dir)

        with self.assertRaises(ValueError):
            template_dir = get_template_directory('re')
            print(template_dir)
        
        template_dir = get_template_directory('fastapi_template')
        print(template_dir)

        template_dir = get_template_directory('template_example')
        print(template_dir)
    
    # def test_create_languages(self):
    #     languages = read_json_file(languages_path2)
    #     languages:dict

    #     new_languages = {}
    #     for key, val in languages.items():
    #         new_languages.update({key: {"extensions": val.get("extensions")}})

    #     overwrite_json_file(languages_path, new_languages)
    #     # print(new_languages)
        
    def test_detect_language(self):
        file_path = ''
        with self.assertRaises(FileNotFoundError):
            detect_language(file_path)
        
        file_path = f'{parent_directory}/tests/test_files/test.py'
        java_path = f'{parent_directory}/tests/test_files/java.java'

        self.assertTrue(detect_language(file_path) == 'python')
        self.assertTrue(detect_language(java_path) == 'java')
        print(detect_language(java_path))

    def test_add_function_patterns(self):
        language = 'python'



if __name__ == "__main__":
    run_test_methods(TestScaffolder.test_add_function_patterns)
