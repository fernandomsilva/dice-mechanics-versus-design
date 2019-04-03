import random, sys, os, time
from ludo import *

def make_dir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)
		
def readInputFile(filepath):
	result = []
	input_file = open(filepath, 'r')
	
	for line in input_file:
		if len(line) > 2:
			temp = (line.split('[')[1]).split(']')[0]
			result.append([int(x) for x in temp.split(',')])
	
	input_file.close()

	return result

def saveDataToFile(filepath, data):
	output_file = open(filepath, 'w')
	
	for entry in data:
		output_file.write(str(entry[0]) + ';' + str(entry[1]) + '\n')
	
	output_file.close()
	
def firstPlayerWinRate(gstate_list):
	total = 0
	wins = 0
	
	for gs in gstate_list:
		total += 1
		first_player_id = gs.move_history[0].player_id
		if gs.result[0] == first_player_id:
			wins += 1
	
	return float(wins) / float(total)

def totalFirstPlayerWins(gstate_list):
	#total = 0
	wins = 0
	
	for gs in gstate_list:
		#total += 1
		first_player_id = gs.move_history[0].player_id
		if gs.result[0] == first_player_id:
			wins += 1
	
	return wins

def runNLudoGames(individual, n=10):
	results = []

	for i in range(0, n):
		gl = Gameloop(None, [MoveGreedy(), RandomAgent(), RandomAgent(), RandomAgent()], dice_mechanics.CustomMechanic(6, individual[0], individual[1], individual[2]))
		results.append(gl.run_game())

	return results

def runGames(individual, n=10):
	result = runNLudoGames(individual, n)
	metric = totalFirstPlayerWins(result)
	
	return metric

def main():
	directory = sys.argv[1]
	gpuid = sys.argv[2]
	numGames = int(sys.argv[3])
	numWorkers = int(sys.argv[4])
	
	if (len(sys.argv) < 6):
		gen = 0
	else:
		gen = int(sys.argv[5])
	
	while True:
		while not os.path.exists(directory + "/gen" + str(gen) + "/worker_data"):
			time.sleep(2) #sleep for 2 seconds
	
		input_individuals = readInputFile(directory + "/gen" + str(gen) + "/input.txt")
		file_count = 0

		while not os.path.exists(directory + "/gen" + str(gen) + "/output.txt") and numWorkers > len([name for name in os.listdir(directory + '/gen' + str(gen) + "/worker_data") if os.path.isfile(directory + '/gen' + str(gen) + "/worker_data/" + name)]):
			results = []
			
			for i in range(0, len(input_individuals)):
				results.append((numGames, runGames(input_individuals[i], numGames)))
			
				if os.path.exists(directory + "/gen" + str(gen) + "/output.txt") or numWorkers <= len([name for name in os.listdir(directory + '/gen' + str(gen) + "/worker_data") if os.path.isfile(directory + '/gen' + str(gen) + "/worker_data/" + name)]):
					break
			
			if not os.path.exists(directory + "/gen" + str(gen) + "/output.txt") and numWorkers > len([name for name in os.listdir(directory + '/gen' + str(gen) + "/worker_data") if os.path.isfile(directory + '/gen' + str(gen) + "/worker_data/" + name)]):
				saveDataToFile(directory + "/gen" + str(gen) + "/worker_data/worker-" + gpuid + "-" + str(file_count) + ".csv", results)
				
				file_count += 1
			
			results.clear()
		gen += 1
	
if __name__ == "__main__":    
    main()
