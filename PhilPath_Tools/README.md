# PhilPath Model Config Generator

A simple python script for generating a template JSON config file for PhilPath models.
The file can be created by providing either:
    (1) The number of classes
    (2) The keras model hdf5 file (this is simply used to infer the number of
    classes)
    (3) The JSON config file used to generate the keras model

In cases (1) and (2):
    (a) the `pixelSizeMicrons` key must be set afterwards (defaults to null)
    (b) each class gets a trivial, numbered `name`
    (c) each class gets assigned an `rgba` color which should look ok
    (d) each class gets the same `type` (defaults to `STRUCTURE`)

In case (3):
    (a) `pixelSizeMicrons` and the class `names` are retrieved from the config file
    (b) the `rgba` color for each class is appropriately guessed based on the `name`
    (c) the `type` is also guessed from the `name`

Run `python gen_philpath_config.py --help` from terminal for usage instructions.
