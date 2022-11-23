import xarray as xr
import os
##################### import data #####################

def get_local_directory():
    cwd = os.getcwd()
    print("CWD: {}".format(cwd))
    return cwd

def import_mdf_dataset(directory, folder):
    '''
    read xarray multi-file dataset for CMIP5/CMIP6 global climate models
    folders are arranged per model as 'cmip5/<model_name>' or 'cmip6/<model_name>'
    see: https://xarray.pydata.org/en/stable/generated/xarray.open_mfdataset.html
    '''
    #directory = '/Users/malavirdee/Documents/climate_data/'
    print("Import model: dir {} folder {}".format(directory, folder))
    path = os.path.join(directory+"/"+folder+"/*.nc")
    return xr.open_mfdataset(path, engine="netcdf4")

def download_s3_folder(bucket, s3_folder, local_dir=None):
    """
    Taken from: https://stackoverflow.com/a/62945526
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    print("Downloading S3 folder... {} / {}".format(bucket, s3_folder))
    if os.path.exists(os.path.join(local_dir)):
        print("Skipping the download because it's already downloaded")
        return
    for obj in bucket.objects.filter(Prefix=s3_folder):
        print("Looping for downloading S3 object {}".format(obj))
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':
            continue
        bucket.download_file(obj.key, target)
