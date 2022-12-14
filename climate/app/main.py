#!/usr/bin/env python

import pandas as pd
from hypervisor_container import ClimateHypervisor
from data import Data, DataLocationType, DataType

"""
Interface Design

Parameters dictionary is passed for a single task run - any lists in this dictionary are treated as single parameters still, and not "looped over" to form multiple outputs.

Outputs are not lists but single layer dictionaries of strings, if there is more than one input or output they must all be named. 


"""

if __name__ == "__main__":
    print("Hello and welcome to the AutoAI Hypervisor Testing Facility!")

    hv = ClimateHypervisor()

    args = hv.parse()
    service_name = args['service_name']
    inputs = args['inputs']
    output_locations = args['outputs']
    

    print("Running task with parameters {}".format(args))

    parameters = args['parameters'][service_name]
    loaded_parameters = hv.load_data(inputs, parameters) # -> [Data]
    print("************************ Data ********************* \n {}".format(loaded_parameters))

    outputs = hv.run_task(service_name, loaded_parameters)
    print("Returned outputs from run_task: {}".format(outputs))
    combined_output_locations = {}
    for i, (k) in enumerate(output_locations.keys()):
        combined_output_locations[k] = (output_locations[k], outputs[i])
    print("combined_output_locations: {}".format(combined_output_locations))

    hv.upload_outputs(combined_output_locations)
    print("\n\nWe're done!!!!!\n\n\n")
 
