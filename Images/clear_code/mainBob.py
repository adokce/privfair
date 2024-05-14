#! /usr/bin/python

#######################################################################
# Name: PRIVFAIR
# Contact: sikha@uw.edu
# Description: Main file checks the command line arguments
#######################################################################
import os
import pathlib
import sys
import traceback
import fileprocessor
import preprocess
import CONSTANTS as C
import messagingObj
#import websockets as ws
#import asyncio
import numpy as np
import time
import argparse
from os import listdir
from os.path import isfile, join
# Main


if __name__ == '__main__':
    try:
       # messenger_obj = messagingObj.messenger()

        print("<=== PrivFair: Private Auditing of Fairness on Machine Learning Models  ===>")
        print("<=== Processing Started  ===>")
        # messenger_obj.sendMessage("1. Parsing Arguments", False)
        parser = argparse.ArgumentParser()

        parser.add_argument('-n', '--num_uploads',
                            required=True,
                            type=int,
                            default=56,
                            dest="num_uploads",
                            metavar="<num_uploads>",
                            help="Files uploaded to check if I recieved all files")
        parser.add_argument('-d', '--data_type',
                            required=False,
                            type=str,
                            default='img',
                            dest="data_type",
                            metavar="<type_of_data>",
                            help="Type of data to be evaluated, Allowed - img, tab")
        parser.add_argument('-u', '--user',
                            required=False,
                            type=str,
                            default='bob',
                            dest="username",
                            metavar="<username>",
                            help="User")
        args = parser.parse_args()
        data_type =  args.data_type
        username = args.username
        messenger_obj = messagingObj.messenger(username)
        file_num = 0
        count = 0
        while file_num < args.num_uploads:
                file_num =len( [f for f in listdir(pathlib.Path(C.USER_INDIR)) if
                             isfile(join(pathlib.Path(C.USER_INDIR), f)) and (f[-5:] == '__img')])
                time.sleep(1)
                count = count + 1
                if count == 11:
                    print("I did not get all files for processing")
                    sys.exit(1)

        print("1. Preprocess data")
        pre_processor = preprocess.ProcessRawData(pathlib.Path(C.USER_INDIR))  # USER_INDIR
        pre_process_method = getattr(pre_processor, C.PRE_PROCESS_FUNC[data_type])
        public_const = pre_process_method()
        print("Processed " + str(public_const[0]) + " samples")
        if public_const[0] == 0:
            print("No samples to evaluate on")
            sys.exit(1)

        print("2. Declare public constants to all")
        
        '''
        async def hello():
            uri = C.WS_URI
            async with ws.connect(uri) as websocket:
                await websocket.send(public_const[0])
                print("3. MPC servers perform compilation")
                isComplete = await websocket.recv()
                if isComplete == 'RUN':
                    return


        asyncio.run(hello())
        '''
        print("4. Secret share private inputs of data and annotations to MPC servers and wait for result")
        os.system(
            "cd /MP-SPDZ/ && ./bankers-bonus-client.x 0 3 0 spdz1 spdz2 spdz3 > " + C.USER_INDIR + "/mpc_out.txt")

        print("5. Private fairness evaluation completed, get data from file and parse it as json")
        file_parser = fileprocessor.ProcessFile(pathlib.Path(C.USER_INDIR))
        file_parse_method = getattr(file_parser, C.FILE_PROCESSOR_FAIR[data_type])
        json_results = file_parse_method()
        messenger_obj.sendResults(json_results, 1)
        #np.set_printoptions(precision=2)
        print(json_results)

        print("6. Display metrics to user ")

        print("<=== Processing Ended ===>")
        
    except:
        print("Some error occurred. Please contact team with below information")
        print("Unexpected error:", sys.exc_info()[0])
        print("Unexpected error:", sys.exc_info()[1])
        print(traceback.print_exc())
