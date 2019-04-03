import random, sys, os, time, functools

from deap import base
from deap import creator
from deap import tools

from ludo import *
import parseWorkerFiles as pwf

def make_dir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)
		
def saveToFile(filepath, input_str_list):
	directory_str_list = filepath.split('/')
	new_directory = ""
	for dir in directory_str_list[:-1]:
		new_directory = new_directory + dir + "/"
		make_dir(new_directory)

	make_dir(new_directory + "worker_data")
		
	file_data = open(filepath, 'a')
	for line in input_str_list:
		file_data.write(str(line) + "\n")
	file_data.close()
	
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 100)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 3)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def eval(individual, results):
	return results[individual],

toolbox.register("evaluate", eval)
toolbox.register("mate", tools.cxOnePoint)
# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
#toolbox.register("mutate", tools.mutUniformInt, 0, 10, indpb=0.05)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.35)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
	#random.seed(64)
	directory = sys.argv[1]
	numWorkers = int(sys.argv[2])
	if len(sys.argv) < 4:
		g = 0
	else:
		g = int(sys.argv[3])
	
	pop = toolbox.population(n=300)
	CXPB, MUTPB = 0.5, 0.2

	if g == 0:
		saveToFile(directory + '/gen' + str(g) + '/input.txt', pop)
		
		while (numWorkers > len([name for name in os.listdir(directory + '/gen' + str(g) + "/worker_data") if os.path.isfile(directory + '/gen' + str(g) + "/worker_data/" + name)])):
			time.sleep(10) #sleep for 10 seconds
	
		print("Start of evolution")
	
		fitness_results = pwf.parseWorkerFiles(directory + '/gen' + str(g), numWorkers)

		fitnesses = list(map(functools.partial(toolbox.evaluate, results=fitness_results), range(0, len(pop))))
		for ind, fit in zip(pop, fitnesses):
			ind.fitness.values = fit

		print("  Evaluated %i individuals" % len(pop))

		fits = [ind.fitness.values[0] for ind in pop]
		files_to_delete = [name for name in os.listdir(directory + '/gen' + str(g) + "/worker_data") if os.path.isfile(directory + '/gen' + str(g) + "/worker_data/" + name)]
		for file in files_to_delete:
			os.remove(directory + '/gen' + str(g) + "/worker_data/" + file)
		saveToFile(directory + '/gen' + str(g) + '/output.txt', zip(pop, fits))
		
	else:
		pass # NEED TO CREATE THE INDIVIDUALS FROM THE EXISTING INPUT FILE!!!
	
	while g < 1000:
		g = g + 1
		print("-- Generation %i --" % g)
		
		offspring = toolbox.select(pop, len(pop))
		offspring = list(map(toolbox.clone, offspring))
	
		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random.random() < CXPB:
				toolbox.mate(child1, child2)

				del child1.fitness.values
				del child2.fitness.values

		for mutant in offspring:
			if random.random() < MUTPB:
				toolbox.mutate(mutant)
				del mutant.fitness.values
	
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		saveToFile(directory + '/gen' + str(g) + '/input.txt', invalid_ind)

		while (numWorkers > len([name for name in os.listdir(directory + '/gen' + str(g) + "/worker_data") if os.path.isfile(directory + '/gen' + str(g) + "/worker_data/" + name)])):
			time.sleep(10) #sleep for 10 seconds

		fitness_results = pwf.parseWorkerFiles(directory + '/gen' + str(g), numWorkers)

		fitnesses = map(functools.partial(toolbox.evaluate, results=fitness_results), range(0, len(invalid_ind)))
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit
		
		print("  Evaluated %i individuals" % len(invalid_ind))
		
		pop[:] = offspring
		
		fits = [ind.fitness.values[0] for ind in pop]
		files_to_delete = [name for name in os.listdir(directory + '/gen' + str(g) + "/worker_data") if os.path.isfile(directory + '/gen' + str(g) + "/worker_data/" + name)]
		for file in files_to_delete:
			os.remove(directory + '/gen' + str(g) + "/worker_data/" + file)
		saveToFile(directory + '/gen' + str(g) + '/output.txt', zip(pop, fits))
		
		length = len(pop)
		mean = sum(fits) / length
		sum2 = sum(x*x for x in fits)
		std = abs(sum2 / length - mean**2)**0.5
		
		print("  Min %s" % min(fits))
		print("  Max %s" % max(fits))
		print("  Avg %s" % mean)
		print("  Std %s" % std)
	
	print("-- End of (successful) evolution --")
	
	best_ind = tools.selBest(pop, 1)[0]
	print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

if __name__ == "__main__":	
	main()
