from utils import readYaml
from os import path
import collections
from field_names import FieldNames
names = FieldNames()


class MorphParser:
    def __init__(self, yaml_dir):
        self.raw_morph_yaml, self.morph_dict, self.speech_parts_values = self.read_morph_dict(yaml_dir)
        self.parsed_morphs = collections.defaultdict(set)
        self.names = FieldNames()

    def parse_morph(self, morphs):
        if isinstance(morphs, str):
            morphs = [morphs]

        parsed = None

        for morph in morphs:
            if morph in self.parsed_morphs:
                parsed = self.parsed_morphs[morph]
            else:
                parsed = self.__read_tag__(morph)
                self.parsed_morphs[morph] = parsed
        return parsed

    def __read_tag__(self, morph):
        tag = self.replace_esc(morph)
        parsed = {}
        part_num = 0

        while tag:
            m = tag[0]
            if part_num == 0 or tag.startswith("X"):
                tag, parsed = self.__read_tag_part__(tag, part_num)
                part_num += 1
            else:
                parsed.setdefault(names.merr, "")
                parsed[names.merr] += m
                tag = tag[1:]
        return parsed

    def __read_tag_part__(self, tag, part_n):
        m = tag[0]
        tag = tag[1:]
        if not tag:
            return tag, {}
        pos = names.unknown if m == names.null else self.speech_parts_values.get(m, None)

        parsed = {}

        if not pos:
            parsed.setdefault(names.merr, "")
            parsed[names.merr] += m
            return tag, {}

        pos_field = 'sp' if not part_n else 'sp' + str(part_n+1)
        parsed[pos_field] = pos

        features = self.morph_dict[pos].keys()
        for features in features:
            if not tag:
                break
            m = tag[0]
            values = self.morph_dict[pos][features]
            mft = f"{features}{part_n + 1}" if part_n else features

            value = names.unknown if m == names.null else values.get(m, None)
            if value is not None:
                parsed[mft] = value
                tag = tag[1:]

        return tag, parsed

    @staticmethod
    def read_morph_dict(yaml_dir):
        raw_morph_yaml = readYaml(path.join(yaml_dir, 'morph.yaml'))
        value_dict = {}
        for (pos, feats) in raw_morph_yaml["tags"].items():
            pos_values = {}
            for feature_data in feats:
                feat_values = {}
                for (feature, values) in feature_data.items():
                    for v in values:
                        m = (
                            raw_morph_yaml["values"][feature][v][0]
                            if feature != 'cl'
                            else raw_morph_yaml["values"][feature][pos][v][0]
                        )
                        feat_values[m] = v
                pos_values[feature] = feat_values
            value_dict[pos] = pos_values
        speech_part_dict = {v[0]: k for (k, v) in raw_morph_yaml["values"]['sp'].items()}
        return raw_morph_yaml, value_dict, speech_part_dict

    def replace_esc(self, tag):
        for x in self.raw_morph_yaml['escapes']:
            tag = tag.replace(*x)
        return tag
