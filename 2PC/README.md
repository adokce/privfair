# PRIVFAIR with Peer to Peer connections
--------------------
## Overview
One way to securely compute fairness of ML Models is with Peer to Peer (P2P) connections. This covers the case where, for example, two parties
Alice and Bob use their local machines to securely compute fairness metrics over an ML model.

--------------------
## Overview on how to run the code
The standard way to run this program is over the internet. With that being said, tests were run over a VPC, thus the 
following instructions will use privte IPs as opposed to external ones. To start, you will need to make sure you have downloaded MP-SPDZ
as described [on their github page](https://github.com/data61/MP-SPDZ). After you have MP-SPDZ set up, you will want to make sure you have
compiled the correct virtual machine. In our example, we use semi2k to run our secure code, which will require you to run **make -j8 semi2k-party.x**
at the top of the MP-SPDZ folder to compile the virtual machine nescesarry for secure computations.

After you have set up MP-SPDZ, you can clone into our repository to run the code. The only thing you should have to edit is the settings files.
In the settings directory, you will see two files, the *audit_data_owner.yaml* file, and the *model_owner.yaml* file. Here, we will go over
what each setting does in the files

## Settings file
- path_to_public_data: If you are the model owner, then this value should point to the absolute path of your model. If you are the audit data owner, then it should point to the directory containing the data. From there, the program will expect two files, *x.csv*, and *y.csv*. x.csv will be the features of the data you wish to determine the fairness of, and y.csv will be the corresponding labels. There currently exists an example of this in the data directory.
- party: Party number.
- party_id_of_model_holder: The number of the party who owns the model
- type_of_data: "audit" means that this settings file is for audit data, "model" means that the settings file is for the ML model.
- model_holders_ip: The IP of the model owner.
- model_holders_port: Port number that the model owners server listens on
- path_to_private_data: This is the absolute for where a parties data that must be kept private (e.g., audit data) should be stored during computations. By default, it should be kept in *MP-SPDZ/Player-Data/Input-P'n'-0*, where 'n' is the party number
- path_to_this_repo: Absolute path to the top of the PrivFair directory
- path_to_top_of_mpspdz: Absolute path to the top of the MP-SPDZ directory
- compile: "true" means that the secure code should be compiled, false otherwise.
- model_type: The name of the model we are using, e.g., lr for logistic regression
- metrics: The types of fairness metrics we wish to use on the ML model as a list.
- recipients: The list of parties we wish to reveal results to. Currently, in MP-SPDZ, there can be problems with revealing to multiple parties, so it may be ideal to just keep it at 0, indicating that party 0 should recieve the results.
- num_of_parties: This indicates the number of parties that will be participating in the computations. In most pratical aplications, the number would remain at 2.
- compiler: The settings we use for the MP-SPDZ compiler.
- VM: What MP-SPDZ virtual machine we use for secure computations, and the settings.
- protected_col: The index of the colum in x.csv that is considered protected, e.g., the gender column.
- protected_col_vals: How the values of the protected column are represented, e.g., 0 for male, 1 for female.
- online: "true" means that secure operations are being performed over different severs, whereas "false" means that operations are being done locally. Note that since the purpose of this repo is to determine the fairness of an ML model over the internet, the offline settings are not well tested, so it may be possible that you run into issues using "false".
- my_private_ip: The IP of the server you are running the code on.

## Running the code
After you set up the files correctly, running the code is simply. On the server containing the model, you can run **python3 run.py settings/model_owner.yaml**. The run.py file will call runAudit.py in the clear_code directory, which will initialize files, and wait for a connection with the auditor. To run code on the auditors server, you simply run **python3 run.py settings/audit_data_owner.yaml**. The parties will connect, share public metadata with eachother, and then automatically execute the secure code.
