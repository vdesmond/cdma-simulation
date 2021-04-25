#!/usr/bin/env python
# -*- coding: utf-8 -*-


def walsh_generator_matrix(ini_mat, x):
    """
    This function generates outerwalsh code matrix for chip sequences in CDMA

    Args:
            ini_mat (list): Inital matrix for Walsh code
            x (int): Walsh code of size N (nearest power of 2 greater than x)
    """
    templist = ini_mat.copy()
	
    if(len(ini_mat) >= x):
    	return ini_mat

    aclimit = len(ini_mat) - 1
    limit = len(ini_mat)*2

    recurs_mat = [[0 for j in range(limit)] for i in range(limit)]
    outer, inner, cnt = 0, 0, 0
    cnt = 0
    for i in range(limit):
    	for j in range(limit):
    		if i >= limit / 2 and j >= limit / 2:
    			recurs_mat[i][j] = templist[outer][inner] * -1
    		else:
    			recurs_mat[i][j] = templist[outer][inner]
    		inner+= 1
    		if inner> aclimit:
    			inner= 0

    	outer += 1
    	if outer> aclimit:
    		outer= 0
    		inner= 0
    	cnt += 1
		
    return walsh_generator_matrix(recurs_mat, x)