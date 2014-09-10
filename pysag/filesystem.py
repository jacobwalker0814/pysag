import os
import glob
import yaml


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

        data = {}
        for data_type in os.listdir(data_dir):
            data[data_type] = []
            for file_name in glob.glob('%s/%s/*' % (data_dir, data_type)):
                # Read the file as YAML
                f = open(file_name, 'r')
                datum = yaml.load(f)
                f.close()

                # The file's basename is its id
                basename = os.path.splitext(os.path.basename(file_name))[0]
                datum['id'] = basename
                data[data_type].append(datum)

        return data
