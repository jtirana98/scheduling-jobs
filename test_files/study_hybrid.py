import argparse
import numpy as np
import time
import sys


sys.path.insert(0,'../util_files')

import ILP_hybrid as ilp_hybrid
import ILP_solver as ilp_sol
import ADMM_hybrid as admm_hybrid
import utils as utils

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', type=str, default='test1.txt', help='filename for the logging')
    parser.add_argument('--clients', '-K', type=int, default=50, help='the number of clients')
    parser.add_argument('--helpers', '-H', type=int, default=2, help='the number of helpers')
    parser.add_argument('--splitting_points', '-S', type=str, default='3,33', help='give an input in the format of s1,s2') # resnet (3,20) #v3,10
    parser.add_argument('--model', '-m', type=str, default='resnet101', help='select model resnet101/vgg19')
    parser.add_argument('--scenario', '-s', type=int, default=1, help='scenario 1 for low heterogeneity or 2 for high')
    parser.add_argument('--dataset', '-d', type=str, default='cifar10', help='dataset, options cifar10/mnist')
    parser.add_argument('--slow_devices', type=int, default=0, help='the number of slow client devices')
    parser.add_argument('--slow_network', type=int, default=0, help='the number of slow connectivities')
    parser.add_argument('--max_slot', type=int, default=150, help='duration of slot')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()

    K = args.clients
    H = args.helpers

    scenario = args.scenario

    splitting_points = args.splitting_points

    points = list(splitting_points.split(','))
    point_a = int(points[0])
    point_b = int(points[1])

    # create the parameter table

    model_type = args.model
    dataset = args.dataset
    if model_type == 'resnet101':
        if dataset == 'cifar10':
            filename = '../real_data/resnet101_CIFAR.xlsx'
        elif dataset == 'mnist':
            filename = '../real_data/resnet101_MNIST.xlsx'
    elif model_type == 'vgg19':
        if dataset == 'cifar10':
            filename = '../real_data/vgg19_CIFAR.xlsx'
        elif dataset == 'mnist':
            filename = '../real_data/vgg19_MNIST.xlsx'

    # get the scenario of the system


    # for type A
    '''     
    (release_date, proc, 
    proc_local, trans_back, 
    memory_capacity, memory_demand, 
    release_date_back, proc_bck, 
    proc_local_back, trans_back_gradients) = utils.create_scenario_hybrid_typeA(filename, point_a, point_b, 
                                                                                K, H, 100, 
                                                                                args.slow_devices, args.slow_network)
    '''

    # for original
    (release_date, proc, 
    proc_local, trans_back, 
    memory_capacity, memory_demand, 
    release_date_back, proc_bck, 
    proc_local_back, trans_back_gradients) = utils.create_scenario_hybrid(filename, point_a, point_b, 
                                                                                K, H, args.max_slot, args.scenario)

    # Define the time horizon (original)
    T = np.max(release_date[0]) + K*np.max(proc[0][0,:]) + np.max(release_date_back[0]) + K*np.max(proc_bck[0][0,:]) \
                        + np.max(proc_local[0]) + np.max(proc_local_back[0])\
                        + np.max(np.max(trans_back[0])) + np.max(np.max(trans_back_gradients[0]))    
    
    T = int(T)
    start_ilp = time.time()
    print('---------------------- ORIGINAL -----------------------------------')
    w_original = 2
    
    ilp_sol.run(K, H, T, release_date[0].astype(int), proc[0].astype(int), 
                                            proc_local[0].astype(int), trans_back[0].astype(int), 
                                            memory_capacity[0].astype(int), 
                                            release_date_back[0].astype(int), proc_bck[0].astype(int), 
                                            proc_local_back[0].astype(int), trans_back_gradients[0].astype(int), 
                                            args.log)
    
    end_ilp = time.time()

    duration_ilp = end_ilp - start_ilp
    # Define the time horizon (hybrid)
    T_hybrid = np.max(release_date[1]) + K*np.max(proc[1][0,0:H]) \
                        + np.max(release_date_back[1]) + K*np.max(proc_bck[1][0,0:H])  \
                        + np.max(proc_local[1]) + np.max(proc_local_back[1])\
                        + np.max(np.max(trans_back[1])) + np.max(np.max(trans_back_gradients[1]))    

    T_hybrid = int(T_hybrid)
    print('time horizon')
    print(T_hybrid)
    print(T)
    print('end time horizon')

    print('---------------------- HYBRID -----------------------------------')
    start_hybrid_optimal = time.time()
    w_hybrid = 2
    w_hybrid = ilp_hybrid.run(K, H, T_hybrid, release_date[1].astype(int), proc[1].astype(int), 
                                            proc_local[1].astype(int), trans_back[1].astype(int), 
                                            memory_capacity[1].astype(int), 
                                            release_date_back[1].astype(int), proc_bck[1].astype(int), 
                                            proc_local_back[1].astype(int), trans_back_gradients[1].astype(int))
    
    end_hybrid_optimal = time.time()
    duration_ilp = end_hybrid_optimal - start_hybrid_optimal
    w_hybrid_admm = ([0,0], -1)
    print('---------------------- ADMM -----------------------------------')
    w_hybrid_admm = admm_hybrid.run(K, H, T_hybrid, release_date[1].astype(int), proc[1].astype(int), 
                                            proc_local[1].astype(int), trans_back[1].astype(int), 
                                            memory_capacity[1].astype(int), memory_demand[1].astype(int),
                                            release_date_back[1].astype(int), proc_bck[1].astype(int), 
                                            proc_local_back[1].astype(int), trans_back_gradients[1].astype(int))
    

    
    print(f"{utils.bcolors.OKGREEN}The original makespan is {w_original}, whereas the hybrid is {w_hybrid}{utils.bcolors.ENDC}")
    print(f"{utils.bcolors.OKGREEN}The hybrid ilp makespan is {w_hybrid}, whereas the admm is {w_hybrid_admm[0][-1]}{utils.bcolors.ENDC}")
    print(f"{utils.bcolors.OKGREEN}For the optimal solution we needed {duration_ilp} sec, while for the ADMM solution {w_hybrid_admm[1]} sec{utils.bcolors.ENDC}")