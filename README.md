# scheduling-jobs


Set-up steps:

1. Python > 3.9
2. Install cvxpy, run: `$ pip install cvxpy`
3. Install GUROBI for cvxpy, run:  `$  pip install gurobipy`
4. Get access to GUROBI license.
5. Other libraries:
    - numpy
    - pandas
    

Scripts Organasation:
- utils.py: read from input files
- fwd_only.py: implementaion of the model that contains the forward propagation (x,y).
- fwd_bwd.py: implementation of the whole model (forward and backward propagation) (x,y,z).
- back_only.py: Calls the fwd_only to get the machine allocation and forward task scheduling (x,y) and optimizes the scheduling of the back-propagation tasks (z).
- fifo.py: Returns computing time for a fifo scenario and node allocation based on a naive load balancing policy.
- the following scripts were used auxilary for testing:
    - f_only_initial_vatiable.py : fwd_only with hardcoded initial values
    - fwd_only_initial_variables.py: fwd_bwd with initial values (x,y,z) generated by the fwd_only.py and back_only.
    - fwd_only_tetsting.py: call solver repeatively to get avg running time.
- generate_test_samples.py: is a script that we use to generate the testing files with random values.

Testing files:

All files contain values for maximun 100 data owners and 5 compute nodes. You can use these files for smaller number of data owners or/and number of compute nodes, by defining the respective values (K, H) and the util files will read up to K data owners and up to H compute nodes. Note to not exceed K>100 and H>5.

For sake of simplicity we use the following definitions:
- Data owners are charcterised by -> (D-capacity, distance), where D-capacity is the device's capacity and distance is how far is from the machine (the farrer the worst connection they have)
- Compute Nodes are charectirised by -> (C-capacity, Memory)

The test are organised to the following files:
- fully_symmetric.xlsx: 
    - Data owners: are the same  (i.e, (D-cap, dist) is the same for all)
    - Compute nodes: are the same (i.e, (C-cap, meme) is the same for all)
- symmetric_machines.xlsx:
    - for the data owners we have:
        - two types of capacity: fast and slow machine.
        - we have two type of distance: near and far.
        - The data owners get (D-cap, dist) randomly one of the aforementioned types.
    - all machines have the same capacity and memory.
- symmetric_data_owners.xlsx:
    - all data owners are the same machine and have the same distance.
    - for the compute nodes we have:
        - two types of capacity: fast and slow machine.
        - memory can be taken from the distibution == (lowest,maximum)
        - The compute nodes get (D-cap, memory) randomly one of the aforementioned types.
- fully_heterogeneous.xlsx:
    - The data owners get (D-cap, dist) randomly one of the aforementioned types.
    - The compute nodes get (D-cap, memory) randomly one of the aforementioned types.

-> Note: in the future the combinations of (D-cap, memory), (D-cap, memory) should be split in more test examples in order to better study the schedulers results.