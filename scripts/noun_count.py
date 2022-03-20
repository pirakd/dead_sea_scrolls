from text_reader import read_text
from text_parser import MorphParser
from os import path
from utils import root_path, filter_data_by_field, readYaml
from collections import defaultdict, Counter

text_file = path.join(root_path, 'data', 'texts', 'dss_nonbib.txt')
yaml_dir = path.join(root_path, 'data',  'yamls')
book_path = path.join(yaml_dir, 'books_to_read.yaml')
morph_parser = MorphParser(yaml_dir=yaml_dir)

books_yaml = readYaml(book_path)['nonbib']
books_flat = [scroll for scrolls in books_yaml for scroll in books_yaml[scrolls]]
data, lines = read_text(text_file, yaml_dir)
filtered_data = filter_data_by_field('scroll_name', books_flat, data)
for book in books_flat:
    for entry in filtered_data[book]:
        entry['parsed_morph'] = morph_parser.parse_morph(entry['morph'])

count = {book:defaultdict(lambda:0) for book in books_flat}
for book in books_flat:
    for entry in filtered_data[book]:
        parsed_morph = entry['parsed_morph']
        if 'sp' in parsed_morph:
            if parsed_morph['sp'] == 'subs':
                if 'st' in parsed_morph:
                    if entry['parsed_morph']['st'] == 'c':
                        count[book]['construct_noun'] += 1
                    elif entry['parsed_morph']['st'] == 'a' or entry['parsed_morph']['st'] == 'd':
                        count[book]['absolute_noun'] += 1
                    else:
                        pass
                else:
                    if parsed_morph['cl'] == 'cmn':
                        count[book]['common_noun'] += 1
                    elif parsed_morph['cl'] == 'prp':
                        count[book]['proper'] += 1
                    elif parsed_morph['cl'] == 'gent':
                        count[book]['gentilic'] += 1
                    elif parsed_morph['cl'] == 'mult':
                        count[book]['multitude'] += 1
                    else:
                        pass

total_counts = {}
for book, scrolls in books_yaml.items():
    total_counts[book] = Counter()
    for scroll in scrolls:
        total_counts[book].update(count[scroll])
