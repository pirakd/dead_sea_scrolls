from text_reader import read_text
from text_parser import MorphParser
from os import path
from utils import root_path

text_file = path.join(root_path, 'data', 'texts', 'dss_nonbib.txt')
yaml_dir = path.join(root_path, 'data',  'yamls')


data, lines = read_text(text_file, yaml_dir)
morph_parser = MorphParser(yaml_dir=yaml_dir)

morph_seq = data[9]['morph']
parsed_morph = morph_parser.parse_morph(morph_seq)