########################################################################
# Name: PRIVFAIR
# Contact: sikha@uw.edu
# Description: Read MPC output and fill desired json file
########################################################################
import traceback
from pathlib import Path
import json
import numpy as np
import sys





class ProcessFile:
    def __init__(self, data_path='./upload'):
        self.data_path = data_path
        self.EMOTION_CLASS = {'6': 'neutral', '3': 'happy', '4': 'sad', '0': 'angry',
                              '2': 'fearful', '1': 'disgust', '5': 'surprised'}

    def process_mpc_output_images_infer(self):
        try:
            set_inference = {}
            sample_id = 0
            with open(Path.joinpath(self.data_path, 'mpc_infer_out.txt'), 'r') as mpcfile:
                for line in mpcfile:
                    if line.startswith('Sample:'):
                        sample_inference = {}
                        str_prob = line.split(':')[1]
                        str_prob = str_prob.lstrip('[')
                        str_prob = str_prob.rstrip(']')
                        probs = str_prob.split(", ")
                        for ind,prob in enumerate(probs):
                            sample_inference[self.EMOTION_CLASS[str(ind)]] = float(prob)
                set_inference[sample_id] = sample_inference
                sample_id = sample_id + 1
            mpcfile.close()

        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
        return json.dump(set_inference)


    def process_mpc_output_images_fair(self):
        final_json = {}
        json_metrics = {}
        try:
            metrics_male = {}
            metrics_female = {}
            #final_metrics_male = {}
            #final_metrics_female = {}
            final_json["type"] = "result"
            with open(Path.joinpath(self.data_path, 'mpc_out.txt'), 'r') as mpcfile:
                for line in mpcfile:
                    if line.startswith('Male:'):
                        metrics = line.split(':')
                        for ind in range(1, len(metrics)):
                            vals = metrics[ind].split('-')
                            if vals[1][-1] == '\n':
                                metrics_male[vals[0]] = round(int(vals[1])/pow(2,16), 2)
                            else:
                                d = dict(x.split("=") for x in vals[1].split(","))
                                for key,val in d.items():
                                    d[key] = round(int(d[key])/pow(2,16), 2)
                                metrics_male[vals[0]] = d

                    if line.startswith('Female:'):
                        metrics = line.split(':')
                        for ind in range(1, len(metrics)):
                            vals = metrics[ind].split('-')
                            if vals[1][-1] == '\n':
                                metrics_female[vals[0]] = round(int(vals[1])/pow(2,16), 2)
                            else:
                                d = dict(x.split("=") for x in vals[1].split(","))
                                for key,val in d.items():
                                    d[key] = round(int(d[key])/pow(2,16), 2)
                                metrics_female[vals[0]] = d
                    if line.startswith('Acc:'):
                        metrics = line.split(':')
                        json_metrics['OA accuracy'] = round(int(metrics[1])/pow(2,16), 2)
            mpcfile.close()



            json_metrics['Male'] = metrics_male
            json_metrics['Female'] = metrics_female
            final_json['message'] = json.dumps(json_metrics)

            #with open(Path.joinpath(self.data_path, 'metrics.json'), "w") as outfile:
            #    json.dump(json_metrics, outfile)

        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
        return json.dumps(final_json)

    def process_mpc_output_tab(self):
        try:
            print("To implement")
        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)

    def process_mpc_output_other(self):
        try:
            print("To implement")
        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
