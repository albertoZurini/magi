import numpy as np
import pandas as pd
from collections import Counter
from tqdm.auto import tqdm
import random, pickle, math, warnings
import itertools,  multiprocessing, json
#warnings.simplefilter('ignore')
print("CPU Count: ", multiprocessing.cpu_count())

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()  # Set model to evaluation mode

def calculate_perplexity(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt")
    
    # Get logits from the model
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss  # The loss is the mean cross-entropy loss
    
    # Calculate perplexity
    perplexity = torch.exp(loss)
    return perplexity.item()

import random

phrase = 'would just in happened town the what you not believe'
words = phrase.split(" ")

population_count = len(words) *1.5


population = []


while len(population) < population_count:
    random.shuffle(words)
    add = True
    for w in population:
        if w["words"] == words:
            add = False
            break

    if add:
        population.append({
            "words": words.copy(),
            "fitness": calculate_perplexity(" ".join(words))
        })
population = sorted(population, key=lambda x: x["fitness"])

# Implement order crossover

def get_average_fitness(population):
    total = 0
    for p in population:
        total += p["fitness"]
    return total/len(population)

def get_first_spot(parent):
    for i in range(len(parent)):
        if parent[i] == "":
            return i
    return len(parent)-1

def order_crossover(parent1, parent2):
    start_index = random.randint(0,len(parent1)-1)
    end_index = start_index + random.randint(1,len(parent1)-start_index) # non inclusive

    child = ["" for _ in range(len(parent1))]
    child[start_index:end_index] = parent1[start_index:end_index]

    # I have to put the words that aren't in child in the same order as they appear in parent2
    i = 0
    while i < len(parent1):
        if parent2[i] not in child:
            # If this word is not present in the children, let's put it at the first available spot
            child[get_first_spot(child)] = parent2[i]
        i += 1
    
    return child

def mutate(el):
    i = random.randint(0,len(el)-1)
    j = random.randint(0,len(el)-1)
    while i == j:
        j = random.randint(0,len(el)-1)
    
    el[i], el[j] = el[j], el[i]
    return el

MUTATION_RATE = 10

for i in range(30):
    print(get_average_fitness(population), population[0])
    offspring = []

    pop_pick = [p["words"] for p in population]
    weights = [1/p["fitness"] for p in population]

    while len(offspring) < population_count:
        # TODO: use randomness with weight based on fitness
        """
        p1_i = len(offspring)
        p2_i = len(offspring) + 1
        if p2_i >= len(parent1):
            p2_i = 0

        parent1 = population[p1_i]["words"]
        parent2 = population[p2_i]["words"]
        """

        parent1 = random.choices(pop_pick, weights)[0]
        parent2 = random.choices(pop_pick, weights)[0]
        while parent2 == parent1:
            parent2 = random.choices(pop_pick, weights)[0]

        child = order_crossover(parent1, parent2)

        if random.randint(0,100) < MUTATION_RATE:
            child = mutate(child)

        offspring.append({
            "words": child.copy(),
            "fitness": calculate_perplexity(" ".join(child))
        })
    
    population = offspring.copy()
    population = sorted(population, key=lambda x: x["fitness"])

pass