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

if __name__ == '__main__':
    # read dataset
    if world.dataset in ['gowalla', 'yelp2018', 'amazon-book','ml-1m']:
        dataset = dataloader.Loader(path="./data/"+world.dataset)
    elif world.dataset == 'lastfm':
        dataset = dataloader.Loader(path="./data")
    #hyperparameter
    #K = 4
    xi = 0.05
    sigma = 1
    #keep record the result
    with open(f"{world.dataset}_AppPG_top20_recall.txt", 'a') as file:
        # 在需要时写入内容
        file.write(f"This is {world.dataset}_AppPG_top20_recall:\n")
    #grid search: alpha
    for ii in range(1,5):
        alpha = 0.2*ii
        #initialize the statistics
        recall = 0
        precision = 0
        F = 0
        NDCG = 0
        with open(f"{world.dataset}_AppPG_top20_recall.txt", 'a') as file:
            file.write(f"alpha={alpha} :\n")
        graph,norm_graph = dataset.getSparseGraph()
        C= graph.copy()
        normC = norm_graph.copy()
        M = dataset.n_users
        N = dataset.m_items
        #get the test set:testarray
        #get the originial user records:uservector
        #testarray = [[] for _ in range(M)]
        testarray = dataset.test.copy()
        uservector = dataset.UserItemNet.copy()
        #print(dataset.test)
        #input("test查看")
        #for idx, user in enumerate(dataset.test):
            #??怎么好像这里会被打乱,testarray是[[]], test是{[]}
            #print(idx,user)
            #input("下一组")
            #testarray[idx] = dataset.test[user]
        for s in range(0,M):
            ppr = pushflowcap_vector(C,s,alpha,xi,sigma,"joint",M+N,normC)
            ppr_item = ppr.copy().reshape(-1)
            print(ppr_item.shape,type(ppr_item))
            ppr_item = ppr_item[M:]
            print(M,N)
            print(ppr_item.shape)
            re,pre,F1,ndcg = Ktop_single(uservector.getrow(s), ppr_item, M, N, 20,testarray,s)
            recall += re
            precision += pre
            F += F1
            NDCG += ndcg
        recall = recall / float(M)
        precision /= float(M)
        F /= float(M)
        NDCG /= float(M)
        with open(f"{world.dataset}_AppPG_top20_recall.txt", 'a') as file:
            file.write(f"top20 ver:  recall: {recall} pre:{precision} F:{F} ndcg:{NDCG}\n")
        #save_npz(f"{world.dataset}_result_{K}layer_{alpha}_new.npz", rowM(vector_propagate,M))
