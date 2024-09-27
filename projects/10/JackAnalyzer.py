import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


class JackAnalyzer:
    def __init__(self, file_path):
        jack_files = self.parse_files(file_path)
        for jack_file in jack_files:
            self.analyze(jack_file)

    def parse_files(self, file_path):
        if '.jack' in file_path:
            return [file_path]
        else:
            file_path = file_path[:-1] if file_path[-1] == '/' else file_path
            dirpath, dirnames, filenames = next(
                os.walk(file_path), [[], [], []])
            jack_files = filter(lambda x: '.jack' in x, filenames)
            return [file_path + '/' + jack_file for jack_file in jack_files]

    def analyze(self, jack_file):
        ce = CompilationEngine(jack_file)
        ce.compile_class()
