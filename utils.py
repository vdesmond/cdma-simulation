#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

# ? Note that walsh_code_generator is recursive in nature
def walsh_code_generator(ini_mat, mat_size):
    """
    This function generates Walsh code using Hadamard matrices for chip sequences in CDMA

    Args:
            ini_mat (list): Initial Hadamard matrix
            mat_size (int): Walsh code of size N (nearest power of 2 greater than mat_size)
    """
    templist = ini_mat.copy()
	
    if(len(ini_mat) >= mat_size):
    	return ini_mat

    aclimit = len(ini_mat) - 1
    limit = len(ini_mat)*2

    recurs_mat = [[0 for j in range(limit)] for i in range(limit)]
    outer, inner, cnt = 0, 0, 0
    cnt = 0
    for i in range(limit):
    	for j in range(limit):
                
                # ? If bottom right matrix, multiply by -1
    		if i >= limit / 2 and j >= limit / 2:
    			recurs_mat[i][j] = templist[outer][inner] * -1

                # ? Else copy the matrix as it is
    		else:
    			recurs_mat[i][j] = templist[outer][inner]
    		inner+= 1
    		if inner> aclimit:
    			inner= 0

    	outer += 1
    	if outer> aclimit:
    		outer, inner = 0, 0
    	cnt += 1

    return walsh_code_generator(recurs_mat, mat_size)

def text2binarr(message):
	"""Converts text to binary array 

	Args:
		message (str): text string

	Returns:
		bin2arr (ndarray): 2D binary array
	"""
	mes2bin = "".join(f"{ord(char):08b}" for char in message)
	bin2arr = np.array([[int(i) for i in mes2bin]], dtype=int)
	return bin2arr

def binarr2text(binary_array):
	"""Converts text to binary array 

	Args:
		bin2arr (ndarray): 2D binary array
		
	Returns:
		message (str): text string
	"""
	temp = list(zip(*[iter(binary_array.flat)]*8))
	message = ""

	for char in temp:
		binstr = int("".join(str(bit) for bit in char), 2)
		message += chr(binstr)
	
	return message