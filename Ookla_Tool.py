# !/usr/bin/env python

# Ookla
# Updated 5/30/18

# This Python script queries a list of available data extract files from Speedtest Intelligence,
# determines what data sets are available, and then downloads the most recent version of each.
# By default the files are stored in the directory where the script is running, but modifying
# the storageDir variable will allow you to specify a directory.

import pandas
try: # Python3
    import urllib.request as compatible_urllib
except ImportError: # Python 2
    import urllib2 as compatible_urllib
import json
import os
import base64
import sys
import pdb
import os, zipfile
import pandas as pd
from glob import glob
import time
import configparser

def main_(days):

    config_file_path = os.getcwd() + '\\config_file\\'
    config = configparser.RawConfigParser()
    config.read('%sconfig.ini' % config_file_path, encoding='utf-8-sig')

    ID = config['Path']['UserName']
    PW = config['Path']['Password']

    # print('Processing Start Please Wait!')
    start = time.time()
    print('Processing!')

    extracts_url = 'https://intelligence.speedtest.net/extracts'

    # Please replace MyApiKey and MyApiSecret below with your organization's API key.
    username = ID
    # username = '0cc38219-52a5-4036-88a1-570ec62dd798'
    password = PW
    # password = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IjlkZmQ2OGIyLWEyYzMtNGQ4ZC1hYmIwLWEwYjNmZTFiNDVjZCI.2ChMVsnJG9YzlyY2-0LWpMIFtqI-mxLFPOClwdeHGHI'

    # By default, the script stores the extract files in the directory where the script is running
    # To specify a storage directory, change this value to a string represting the directory where
    # the files should be stored.
    # Example: storageDir = '/data/ookla/extracts'
    storageDir = os.getcwd()

    opener = compatible_urllib.build_opener()
    compatible_urllib.install_opener(opener)
    opener.addheaders = [('Accept', 'application/json')]

    # setup authentication
    login_credentials = '%s:%s' % (username, password)
    base64string = base64.b64encode(login_credentials.encode('utf-8')).decode('ascii')
    opener.addheaders = [('Authorization', 'Basic %s' % base64string)]

    # makes request for files
    try:
        response = compatible_urllib.urlopen(extracts_url).read()
    except compatible_urllib.HTTPError as error:
        if error.code == 401:
            print("Authentication Error\nPlease verify that the API key and secrete are correct")
        elif error.code == 404:
            print("The account associated with this API key does not have any files attached to it.\nPlease contact your technical account manager to enable data extracts for this account.")
        elif error.code == 500:
            print("Server Error\nPlease contact your technical account manager")
        sys.exit()

    try:
        content = json.loads(response)
    except ValueError as err:
        print(err)
        sys.exit()

    ###########################################################

    # loop through contents, sort through files and directories
    def All_Files(days):


        # subdir = 'https://intelligence.speedtest.net/extracts' + '/cell_only/'

        subdir = extracts_url + '/servers/'
        contents = json.loads(compatible_urllib.urlopen(subdir).read())
        new_files = []
        type_list = []
        i = 0
        for entry in contents:
            if entry['type'] == 'file' and entry['name'].find('headers') == -1 and '_20' in entry['name']:

                type_list.append(entry['name'].split('_')[0] + str(i))
                new_files.append( {'name': entry['name'], 'url': entry['url'], 'age': entry['mtime']})
            i = i + 1

        if days == '':
            files = dict(zip(type_list, new_files))
        else:
            days = int(days)
            #
            type_list_ios = []
            type_list_and = []



            for i in type_list:

                type_list_ios.append(i.split('android')[0])

            for i in type_list:
                type_list_and.append(i.split('iOS')[0])



            while '' in type_list_and:
                type_list_and.remove('')

            while '' in type_list_ios:
                type_list_ios.remove('')

            type_list_and_ = type_list_and[-days:]
            type_list_ios_ = type_list_ios[-days:]

            #
            new_files_and = new_files[:len(type_list_and)]
            new_files_ios = new_files[-len(type_list_and):]

            new_files_and_ = new_files_and[-days:]
            new_files_ios_ = new_files_ios[-days:]


            new_typelist = type_list_and_ + type_list_ios_
            new_new_files = new_files_and_ + new_files_ios_

            files = dict(zip(new_typelist, new_new_files))

        return files

    def download(files):
        #
        if not files:
            print("No data extract files found. If this is an error, please contact your technical account manager.")
            return

        for data_set, file in files.items():
            response = compatible_urllib.urlopen(file['url'])
            #
            dir_name = file['name'].split('_')[0]
            # if dir_name == 'android'
            flocation = storageDir + '/' + dir_name + '/' + file['name']
            print(("Downloading: %s" % (file['name'])))
            with open(flocation, 'wb') as content:
                content.write(response.read())

    #############################################################

    def Unzip_all(dir_):

        if dir_ == 'android':

            path_ = str(os.getcwd())
            dir_name = str(os.getcwd()) +'\\android'
        else:
            path_ = str(os.getcwd())
            dir_name = str(os.getcwd()) +'\\iOs'

        extension = ".zip"
        os.chdir(dir_name)

          # change directory from working dir to dir with files

        for item in os.listdir(dir_name):  # loop through items in dir
            if item.endswith(extension):  # check for ".zip" extension
                file_name = os.path.abspath(item)  # get full path of files
                zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
                zip_ref.extractall(dir_name)  # extract file to dir
                zip_ref.close()  # close file
                os.remove(file_name)  # delete zipped file

        interesting_files = glob(dir_name + '\\' + "*.csv")  # it grabs all the csv files from the directory you mention here
        df_list = []
        os.chdir(path_)
        # del os

        for filename in sorted(interesting_files):
            df_list.append(pd.read_csv(filename))

        full_df = pd.concat(df_list)
        # save the final file in same/different directory:
        full_df.to_csv(str(os.getcwd())+'\\Output\\' + dir_ + ' Output.csv', index=False)


        if dir_ == 'android':
            android = full_df
            return android

        else:
            ios = full_df
            return ios


    files = All_Files(days)
    download(files)


    android = Unzip_all('android')
    ios = Unzip_all('iOs')


    android = android.append(ios)

    #
    # android['Date'] = android['test_date'].str.split(' ').str[0]

    android.to_csv(str(os.getcwd())+'\\Output\\Combined android & iOs servers Output.csv', index=False)
    end = time.time()
    Execute_Time = "{:.3f}".format((end - start) / 60)
    print('The Execution Time of this Tool is %s minutes.' % Execute_Time)
    time.sleep(1)
    print('Execution Completed Succcessfully!')
    time.sleep(1)
    print('')
    print('')
    print('---------------Huawei RF Middle East----------------')
    print('---------For Support: Danish Ali(dwx854280)---------')
    print('---------------Contact: 00971508552942--------------')
    time.sleep(2)
