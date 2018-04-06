# PhilPath Model Config Generator

A simple python script for generating a template JSON config file for a given model.
It simply generates a template JSON file populated with a number of classes (either
input by the user or inferred from a keras model hdf5 file). The default colors of
the classes are ok as a starting point. Default pixelSizeMicrons is 1.0 and should
be changed and the default class names are trivial (not sure if either or both of
these pieces of information can be found from the hdf5 file?).
