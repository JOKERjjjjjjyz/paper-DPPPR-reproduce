import time

from sensi import *
import dataloader
import world
import torch
from dataloader import Loader
import sys
import scipy.sparse as sp
from train import *
import numpy as np
from scipy.sparse import csr_matrix
import torch.sparse
from scipy.sparse import save_npz

#main2.py是用于进行小型矩阵上的测试以验证复现的正确性
if __name__ == '__main__':
    if world.dataset in ['gowalla', 'yelp2018', 'amazon-book','ml-1m']:
        dataset = dataloader.Loader(path="./data/"+world.dataset)
    elif world.dataset == 'lastfm':
        dataset = dataloader.Loader(path="./data")
    #K = 4
    xi = 0.01
    sigma = 3
    with open(f"{world.dataset}_AppPG_top20_recall.txt", 'a') as file:
        # 在需要时写入内容
        file.write(f"This is {world.dataset}_AppPG_top20_recall:\n")
    for ii in range(1,5):
        alpha = 1- 0.2*ii
        with open(f"{world.dataset}_AppPG_top20_recall.txt", 'a') as file:
            file.write(f"alpha={alpha} :\n")
        graph,norm_graph = dataset.getSparseGraph()
        C= graph.copy()
        normC = norm_graph.copy()
        M = dataset.n_users
        N = dataset.m_items
        s = random.randint(1, M)
        testarray = [[] for _ in range(M)]
        uservector = dataset.UserItemNet.copy()
        for idx, user in enumerate(dataset.test):
            testarray[idx] = dataset.test[user]
        
        #G = sp.csr_matrix([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
        #s = 0
        #alpha = 0.4
        #xi = 0.01
        #sigma = 3.0
        #type = "joint"
        ppr = pushflowcap(C,s,alpha,xi,sigma,"joint",M+N)
        ppr[s] = 0
        print(ppr)
        '''
        ppr + dp noise
        Add dp algorithm here
        '''
        print("completed")
        #C_user = rowM(ppr,M)
        #vector_propagate = C_user.dot(uservector)
        
        recall = Ktop_single(uservector, ppr[M:], M, N, 20,testarray,s)
        with open(f"{world.dataset}_AppPG_top20_recall.txt", 'a') as file:
            file.write(f"topk20 ver:  recall: {recall}\n")
        #save_npz(f"{world.dataset}_result_{K}layer_{alpha}_new.npz", rowM(vector_propagate,M))
