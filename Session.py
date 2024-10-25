#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 23:25:52 2022

@author: dell
"""

from condition.Block import genFitBlock

class Session(object):
    def __init__(self, dimension, levels):
        self.dim = dimension
        self.levels = levels
        
        self.target = self.genPairs()
        self.sess = self.genSess()

    
    def genSess(self):
        session = []
        block_num = int(len(self.target) / (self.levels**2))
        for block_id in range(block_num):
            block_tmp = genFitBlock(self.dim,self.levels)
            session[block_id] = block_tmp
        return session
        
    
    def _genPairsTarget():
        pass
    
    
    def _genPairsSess():
        pass
        
        
    def genPairs(self,sources,pairs_type):
        if pairs_type == 'target':
            return self._genPairsTarget
        elif pairs_type == 'sess':
            return self._genPairsSess
    

    def sess_fitness():
        #pairs_target = genPairs(mapSet,'target')
        #pairs_session = genPairs(session,'sess')
        #fitness_sess = pairs_overlap(pairs_targe,pairs_session)
        return fitness
        pass