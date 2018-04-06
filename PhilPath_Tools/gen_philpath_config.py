#!/usr/bin/env python
import sys
import h5py
import json
import os
import argparse
import re
from collections import OrderedDict

class names():
    regex = {
            'non-tumour': re.compile(r'non.*tumo[u]?r.*', re.IGNORECASE),
            'tumour': re.compile(r'tumo[u]?r.*', re.IGNORECASE),
            'boundary': re.compile(r'bound', re.IGNORECASE),
            'background': re.compile(r'backgr', re.IGNORECASE)
            }
    def_type = 'STRUCTURE'

    colors = [
            [255, 0, 255],
            [255, 255, 0],
            [255, 153, 0],
            [102, 0, 204],
            [0, 153, 204],
            [0, 153, 51],
            [153, 153, 102],
            [153, 51, 51],
            [0, 0, 0]]

    def _infer_color_from_name(self, name, cid=None):
        if self.regex['non-tumour'].search(name):
            return [0, 255, 0]
        elif self.regex['tumour'].search(name):
            return [255, 0, 0]
        elif self.regex['background'].search(name):
            return [0, 0, 0, -255]
        elif self.regex['boundary'].search(name):
            return [0, 0, 255]
        else:
            return self.colors[cid]

    def _infer_type_from_name(self, name):
        if self.regex['boundary'].search(name):
            return 'BOUNDARY'
        elif self.regex['background'].search(name):
            return 'BACKGROUND'
        else:
            return self.def_type

parser = argparse.ArgumentParser(description='Generate config file for PhilPath'
        ' from either keras model hdf5 file or algorithm input JSON file.')
parser.add_argument('input_file', help='The input hdf5/JSON file (only required if'
        ' argument --num_classes is not specified).', default=None, nargs='?')
parser.add_argument('output', help='PhilPath json config output file (default: '
        '%(default)s).', default='channels.json', nargs='?')
parser.add_argument('--num_classes', help='Number of classes (default: '
        'inferred from model file).', default=None, type=int)
parser.add_argument('--class_type', help='Default class type (default: '
        '%(default)s).', default='STRUCTURE')
args = parser.parse_args()

infile = args.input_file
outfile = args.output
num_classes = args.num_classes
def_class_type = args.class_type

infiletmp, file_ext = os.path.splitext(str(infile))

cn = names()
cn.def_type = def_class_type
res = None

if (num_classes is None) and (infile is None):
    raise ValueError('Error: must specify either infile or num_classes.')

if num_classes is None:
    if file_ext == '.hdf5':
        foo = h5py.File(infile, 'r')
        my_list = list(filter(lambda x: 'conv2d' in x, list(foo['model_weights'])))
        my_list.sort()
        last_conv = my_list[-1]
        num_classes = len(list(foo['model_weights'][last_conv][last_conv]['bias']))
        class_names = ['Name_%d' % ii for ii in range(num_classes)]
    elif file_ext == '.json':
        with open(infile) as foo:
            algo_config = json.load(foo)
        res = algo_config['resolution'].replace('mpp', '')
        class_names = algo_config['classes']['names']
        num_classes = len(class_names)
    else:
        raise ValueError('File extenstion of input file neither hdf5 or json.')
else:
    class_names = ['Name_%d' % ii for ii in range(num_classes)]

phil_path_config = OrderedDict()
phil_path_config['pixelSizeMicrons'] = res
phil_path_config['channels'] = []

for channel in range(num_classes):
    tmp_dict = OrderedDict()
    tmp_dict['name'] = class_names[channel]
    tmp_dict['rgba'] = cn._infer_color_from_name(tmp_dict['name'], channel)
    tmp_dict['type'] = cn._infer_type_from_name(tmp_dict['name'])
    phil_path_config['channels'].append(tmp_dict)

with open(outfile, 'w') as fp:
    json.dump(phil_path_config, fp, indent=2, sort_keys=False)
