from data import Data, DataLocationType, DataType
import argparse
import json
import sys
import boto3
from datetime import datetime
import pandas as pd

# TEST_DATA_S3_URI = "s3://climate-ensembling/test_data.csv"
TEST_DATA_KEY = "tst/EC-Earth3/"
TEST_DATA_BUCKET = "climate-ensembling"

"""
How to structure the data in S3 for flexible / automatic data finding?

Possibilities:

Example 1:

s3://climate-ensembling/<task-1>/<task-2>/..../<task-n>
climate-ensembling/<model>/<select_city>/<bias_correction>/<aggregation>

Example 2:
???

"""

class Hypervisor():
    def __init__(self):
        self.data = {}

    def parse(self, verbose=True):

        print("Arguments passed {} \n\n".format(sys.argv))

        parser = argparse.ArgumentParser(description='Choice of Climate Ensembling task and parameters for it')
        parser.add_argument('--parameters',
                            help='the parameters dictionary')
        args = parser.parse_args()
        real_args = json.loads(args.parameters)
        print("Parser arguments output: {}".format(real_args))

        return real_args

    def _parse_s3_uri(self, uri):
        components = uri[5:].split('/')
        s3_key = '/'.join(components[1:])
        s3_bucket = components[0]
        return s3_key, s3_bucket

    def _is_input_data(self, value):
        return isinstance(value, type("")) and value.startswith("s3://")

    def _parse_data(self, key, value): 
        if self._is_input_data(value):
            s3_key, s3_bucket = self._parse_s3_uri(value)
            print("Parsing data for key: {} value: {}, coming from s3 key {} and bucket {}.".format(key, value, s3_key, s3_bucket))
            if key not in self.data:
                self.data[key] = {}
            dtype = DataType.CSV if '.csv' in value else DataType.MDF
            print("Retrieving for bucket {} and key {}".format(s3_bucket, s3_key))
            self.data[key][value] = (Data(dtype, DataLocationType.S3, s3_key=s3_key, s3_bucket_name=s3_bucket))
        else:
            return value
        return self.data[key][value]

    def load_data(self, inputs, parameters):
        """
        Returns the parameters ditionary, combined with the inputs, having loaded any parameters in either that were from S3 and replaced them with a Data object.
        
        e.g
        {'base_model' : Data(s3_key='s3://.....', ...)}
        """

        loaded_parameters = {}

        for key, value in {**inputs, **parameters}.items():
            if key in parameters and key in inputs:
                print("************** WARNING ************* inputs and parameters share a key ({}), this will cause issues, please rename one of them to a unique name.".format(key))
            print("Inputs to load in : ")
            print("Key: {} Value: {}".format(key, value))
            if isinstance(value, list):
                loaded = []
                listvalue = value
                for v in listvalue:
                    loaded.append(self._parse_data(key, v))
            else:
                loaded = self._parse_data(key, value)
            loaded_parameters[key] = loaded

        return loaded_parameters

    def upload_outputs(self, outputs, bucket_name='climate-ensembling'):
        """
        Assumes outputs is a list of DataFrames [df, df, ...]
        """
        s3 = boto3.resource("s3")
        print("Upload these outputs! Outputs: {}".format(outputs))
        # datetime object containing current date and time
        now = datetime.now()
         
        print("now =", now)
        dt_string = now.strftime("%d:%m:%Y:%H:%M")
        # dd/mm/YY H:M:S
        for location, output in outputs.values():
                print("Output: {} Location: {}".format(output, location))
                if isinstance(output, pd.DataFrame):
                    filename=dt_string+'.csv'
                    print("Output: {} {}".format(outputs, type(output)))
                    output.to_csv(filename)
                else:#is MFD type then
                    filename=dt_string+'.nc'
                    output.to_netcdf(filename)

                s3_key, bucket_name = self.parse_s3_uri(location)
                s3_bucket = s3.Bucket(name=bucket_name)
                obj_name = s3_key + filename
                print("Uploading local file {} to bucket {} and location {}".format(filename, s3_bucket, obj_name))
                s3_bucket.upload_file(filename, obj_name)

        print ("Finished uploading data!")

    def run_task(self, task, task_list, parameters):
        """
        Returns a list or tuple of outputs from the task.
        """
        print("Task: {}".format(task))
        print("Parameters: {}".format(parameters))
        if task in task_list:
            return task_list[task](parameters)
        else:
            assert False, "No valid task chosen!"
