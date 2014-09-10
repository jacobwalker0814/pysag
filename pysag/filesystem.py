import os
import glob
import yaml
import json

# TODO reformat for less indentation


class DataNode:
    def populate(self, data):
        self.data = data

    def export(self):
        return self.data


class Reader:
    def read(self, data_dir):
        # Walk through the directory {data_dir}. Any folders there become top
        # level elements in our data. Any .yml files there will be parsed into
        # results

        all_data = {}
        for data_type in os.listdir(data_dir):
            all_data[data_type] = []
            for file_name in glob.glob('%s/%s/*' % (data_dir, data_type)):
                # Read the file as YAML
                f = open(file_name, 'r')
                data = yaml.load(f)
                f.close()

                # The file's basename is its id
                basename = os.path.splitext(os.path.basename(file_name))[0]
                data['id'] = basename
                node = DataNode()
                node.populate(data)

                all_data[data_type].append(node)

        return all_data


class Writer:
    def _write_json(self, data, path):
        with open(path, 'w') as f:
            json.dump({'result': data}, f)

    def write(self, data, output_dir):
        for key in data:
            all_data = []
            os.makedirs('%s/%s' % (output_dir, key))
            for node in data[key]:
                node_data = node.export()
                all_data.append(node_data)
                path = '%s/%s/%s.json' % (output_dir, key, node_data['id'])
                self._write_json(node_data, path)

            path = '%s/%s.json' % (output_dir, key)
            self._write_json(all_data, path)
