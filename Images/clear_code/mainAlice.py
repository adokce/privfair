#! /usr/bin/python

#######################################################################
# Name: PRIVFAIR
# Contact: sikha@uw.edu
# Description: Main file checks the command line arguments
#######################################################################
import os
import pathlib
import subprocess
import sys
import traceback

#from paramiko.client import SSHClient

#import fileprocessor

import datetime
import argparse
import time
#import messagingSocket
#import preprocess
#import shutil
#from pathlib import Path
#import shlex
#import CONSTANTS as C
#import messagingObj
#import scp
import json
import requests

# Main
# Arguments - input_path for each session, output_path json

if __name__ == '__main__':
    try:
        #messenger_obj = messagingObj.messenger()

        # messenger_mpc = messagingSocket.MessageSocket()

        print("<=== PrivFair: Private Auditing of Fairness on Machine Learning Models  ===>")
        print("<=== Processing Started  ===>")

        data_type = 'img' #args.data_type
        print("1. Extracting model parameters")
        time.sleep(30)
        print("-- Send public constants to evaluator")
        print("2. Declare public constants to all")
        print("3. MPC servers perform compilation")
        #print("Now assuming they have already done it")
        print("4. Secret share private inputs of data and annotations to MPC servers and wait for result")
        os.system("cd /MP-SPDZ/ && ./bankers-bonus-client.x 1 3 1 spdz1 spdz2 spdz3 >  mpc_out.txt")
        #print("5. Private fairness evaluation completed")
        #mesenger_obj.sendResults()
        time.sleep(20)
        print("<=== Processing Ended from my side===>")
        headers = {"Content-Type":"application/json"}
        api_url = "http://aaai-demo:8080/message/alice"
        final_json = {}
        final_json["type"] = "completed"
        final_json['message'] = "Completed"
        result = json.dumps(final_json)
        response = requests.post(api_url, data=result, headers=headers)


    except:
        print("Some error occurred. Please contact team with below information")
        print("Unexpected error:", sys.exc_info()[0])
        print("Unexpected error:", sys.exc_info()[1])
        print(traceback.print_exc())
