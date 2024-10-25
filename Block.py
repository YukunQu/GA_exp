#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 17:07:02 2022

@author: dell
"""
import time 
import random
import numpy as np
import pandas  as pd 


class Block(object):
    
    """Class representing single in population"""
    def __init__(self, dimension, levels,child=False):
        self.dim = dimension
        self.levels = levels
        self.blockfile = None
        self.target = range(1,self.levels**2+1)
        
        self.mapset = self.genMapset()
        if not child:
            self.blockfile = self.genBlock()
            self.fitness = self.block_fitness()
        
        
    def genMapset(self):
        levels = self.levels
        # assign the attack and defence power
        x = range(1,levels+1)
        y = range(1,levels+1)
        d1,d2 = np.meshgrid(x,y)
        d1 = d1.reshape(-1)
        d2 = d2.reshape(-1)
        mapset = pd.DataFrame({'Pos_Index':range(1,levels**2+1),
                               'Attack_Power':d1,'Defence_Power':d2,
                               'useable':[1]*len(d1)})
        return mapset


    # @classmethod
    def genPath(self):
        """generate path as genes"""
        if self.dim == 'ap':
            sample_dim = 'Attack_Power'
        elif self.dim == 'dp':
            sample_dim = 'Defence_Power'
        
        path = []
        idx  = []
        for pos_rank in range(self.levels):
            pos_rank = pos_rank + 1
            useable_image = self.mapset[self.mapset['useable']==1]
            pos_info = useable_image.query('{}=={}'.format(sample_dim, pos_rank)).sample(1)
            idx.append(pos_rank)
            path.append(pos_info)
            pos_index = pos_info.index
            self.mapset.loc[pos_index,'useable'] = 0 
        
        path = pd.concat(path,axis=0)
        path.index = idx
        return path

    
    # @classmethod
    def genBlock(self):
        """generate block as chromosome"""
        # levels N means the rank number of the  map 
        
        block = []
        for path_id in range(self.levels):
            path_tmp = self.genPath()
            block.append(path_tmp)
        return block
        
    
    def mate(self,parBlockY):
        '''
        Perform mating and produce new offspring
        '''
        child_blockfile = []
        child_block = Block(self.dim,self.levels,True)
        prob = random.random() 
        # insert random mutated path
        if prob < 0.5:
            random_index= round(random.uniform(0,4))
            self.blockfile[random_index] = self.genPath()
            child_blockfile = self.blockfile
        else:
            for path_id,(pathx,pathy) in enumerate(zip(self.blockfile,parBlockY.blockfile)):
                
                # random probability
                prob = random.random() 
                # if prob is less than 0.45, insert gene, insert gene from blcok-parentX
                if prob < 0.45:
                    child_blockfile.append(pathx)
                # if prob is between 0.45 and 0.90, insert gene from blcok-parentY
                elif prob < 0.90:
                    child_blockfile.append(pathy)
                else:
                    child_blockfile.append(self.genPath())
            
        child_block.blockfile = child_blockfile
        child_block.fitness = child_block.block_fitness()
        return child_block
    
    
    def img_index(self):
        imgs_index = []
        for pathfile in self.blockfile:
            imgs_index.extend(pathfile['Pos_Index'].to_list()) # 
        imgs_index.sort()
        return imgs_index
    
    
    def block_fitness(self):
        # test the block contains all images
        imgs_index = self.img_index()
        fitness = 0 # fitness: how many images in the block  fit the target
        for bimg,btar in zip(imgs_index,self.target):
            if bimg == btar: fitness +=1
        return fitness
    

def genFitBlock(dimension,levels=5, population_size=10):
    # initialize generation
    generation = 1
    found = False
    population = []
    start_time = time.time()
    
    # create initial population
    for _ in range(population_size):
        population.append(Block(dimension, levels))
    
    while not found:
        # sort the population in decreasing order of fitness score
        population = sorted(population, reverse = True, key = lambda x:x.fitness)
        
        # if the individual having largest fitness score ie.
        # then we know that we have reached to the target and break the loop       
        if population[0].fitness >= levels**2:
            found = True
            break
        
        # Otherwise generate new offsprings for new generation
        new_generation = []
        # Perform Elitism, that mean 10% of fittest population goes to the next generation
        s = int((10*population_size)/100)
        new_generation.extend(population[:s])
        
        # From 50% of fittest population, Individuals will mate to produce offspring
        s = int((90*population_size)/100)
        for _ in range(s):
            parent1 = random.choice(population[:5])
            parent2 = random.choice(population[:5])
            child = parent1.mate(parent2)
            new_generation.append(child)
        
        population = new_generation

        print("Generation: {}\t Fitness: {}".format(generation,population[0].fitness))
        generation += 1
    
    end_time = time.time()
    print("Last_Generation: {}\t Fitness: {}\t Time:{}"\
          .format(generation,population[0].fitness,start_time - end_time))
    return population[0]
            

block = genFitBlock('ap')