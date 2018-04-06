#!/usr/bin/env python
import sys
import h5py
import json
import os
import argparse

parser = argparse.ArgumentParser(description='Generate config file for PhilPath'
        ' from keras model hdf5 file.')
parser.add_argument('model', help='The input hdf5 model file (only required if'
        ' argument --num_classes is not specified).', default=None, nargs='?')
parser.add_argument('output', help='PhilPath json config output file (default: '
        '%(default)s).', default='channels.json', nargs='?')
parser.add_argument('--num_classes', help='Number of classes (default: '
        'inferred from model file).', default=None, type=int)
parser.add_argument('--class_type', help='Default class type (default: '
        '%(default)s).', default='STRUCTURE')
args = parser.parse_args()

infile = args.model
outfile = args.output
num_classes = args.num_classes
def_class_type = args.class_type

colors = [[255, 0, 0],
        [0, 255, 0],
        [0, 0, 255],
        [255, 0, 255],
        [255, 255, 0],
        [255, 153, 0],
        [102, 0, 204],
        [0, 153, 204],
        [0, 153, 51],
        [153, 153, 102],
        [153, 51, 51],
        [0, 0, 0]]

if (num_classes is None) and (infile is None):
    raise ValueError('Error: must specify either infile or num_classes.')

if num_classes is None:
    foo = h5py.File(infile, 'r')
    my_list = list(filter(lambda x: 'conv2d' in x, list(foo['model_weights'])))
    my_list.sort()
    last_conv = my_list[-1]
    num_classes = len(list(foo['model_weights'][last_conv][last_conv]['bias']))

phil_path_config = {'pixelSizeMicrons': 1.0, 'channels': []}

for channel in range(num_classes):
    tmp_name = 'Name_%d' % channel
    tmp_dict = {'name': tmp_name, 'type': def_class_type, 'rgba': list(colors[channel])}
    phil_path_config['channels'].append(tmp_dict)

with open(outfile, 'w') as fp:
    json.dump(phil_path_config, fp, indent=2, sort_keys=False)
