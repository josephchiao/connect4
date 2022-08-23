import numpy as np
import os
import random
import time
import shutil
import theta_init

def theta_generate(Theta_1_size, Theta_2_size, Theta_3_size, n):

    folder = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for dataset in range(n):
        theta_init.create_file(Theta_1_size, Theta_2_size, Theta_3_size, file_name = f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{dataset}.npz")


def tournament(rounds):
    for r in range(rounds):
        population = len(os.listdir('/home/joseph/Desktop/chess_neural_network/engine_data'))
        parity_bins = [[], []]
        for i in range(population // 2):
            i = (i + 1) * 2

            print(i, " vs ", (i - 1))

            winner, loser, win_state = fight.fight([i, i - 1])
            os.remove(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{loser}.mat")
            parity_bins[winner % 2].append(winner)

        folder = '/home/joseph/Desktop/chess_neural_network/engine_data/'
        if 1 in parity_bins[1]:
            new_num = population + 1 + population % 2
            os.rename(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{1}.mat", f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{new_num}.mat")
            parity_bins[1].remove(1)
            parity_bins[1].append(new_num)

        for x in range(population // 2):
            bin = parity_bins[x % 2]
            if len(bin) == 0:
                bin = parity_bins[x % 2 - 1]
            
            os.rename(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{bin[0]}.mat", f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{x + 1}.mat")
            bin.pop(0)


def multi_tournament(heats, survivor_num):

    population = len(os.listdir('/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data'))
    # print("Current population: ", population)

    players = list(range(population))
    fight_sequense = list(players)
    random.shuffle(fight_sequense)
    fight_info = {players[i]: 0 for i in range(len(fight_sequense))}

    for heat in range(heats):
        for round in range(population):
            player_1 = fight_sequense[round]
            player_2 = fight_sequense[(round + heat + 1) % population]
            
            print(player_1, " vs ", player_2)
            print(f"Heat: {heat + 1} / {heats}")
            print(f"Round: {round + 1} / {population}")

            winner, loser, win_state = fight.fight([player_1, player_2])

            if win_state:
                fight_info[winner] += 1
                fight_info[loser] -= 1
            else:
                fight_info[winner] += 0.1
                fight_info[loser] -= 0.1
    
    print(fight_info)

    strongest = max(fight_info, key = fight_info.get)
    folder = '/home/joseph/Desktop/chess_neural_network/elite_data/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    if strongest != 1:
        shutil.copyfile(f'/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{strongest}.mat', 
                        f'/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{1}.mat'
    )
    
    players.sort(key = lambda player: fight_info[player], reverse = True)
    survivors = players[:survivor_num]
    death = players[survivor_num:]
    
    print(survivors)
    print("number of survivors: ", len(survivors))

    for player in death:
        os.remove(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{player}.mat")
    
    survivors.sort()
    n = 1
    for player in survivors:
        os.rename(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{player}.mat", f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{n}.mat")
        n += 1
    
    folder = '/home/joseph/Desktop/chess_neural_network/parent_engine_data/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    source = '/home/joseph/Desktop/chess_neural_network/engine_data/'
    destination = '/home/joseph/Desktop/chess_neural_network/parent_engine_data/'
  
    allfiles = os.listdir(source)
    population = len(allfiles)
    print("Population: ", population)
  
    for f in allfiles:
        shutil.move(source + f, destination + f)


def multi_tournament_self_train(heats, survivor_num, heat_size):

    population = len(os.listdir('/home/joseph/Desktop/chess_neural_network/engine_data'))
    print("Current population: ", population)

    players = list(range(1, population + 1)) * heat_size
    fight_sequense = list(players)
    random.shuffle(fight_sequense)
    fight_info = {players[i]: 0 for i in range(len(fight_sequense))}

    for heat in range(heats):
        X_win = []
        y_win = []
        X_lose = []
        y_lose = []
        X_draw = []
        y_draw = []

        for round in range(len(fight_sequense)):
            player_1 = fight_sequense[round]
            player_2 = fight_sequense[(round + heat + 1) % population]
            
            print(player_1, " vs ", player_2)
            print(f"Heat: {heat + 1} / {heats}")
            print(f"Round: {round + 1} / {len(fight_sequense)}")
            print(f"examples (w, l, d): {(len(y_win), len(y_lose), len(y_draw))}")

            X_j, y_j = fight.fight_unassisted([player_1, player_2])
            
            if y_j[-1] > 0.5:
                X_win += X_j
                y_win += y_j
                winner = player_1
                loser = player_2

            elif y_j[-1] < 0.5:
                X_lose += X_j
                y_lose += y_j
                winner = player_2
                loser = player_1

            else:
                X_draw += X_j
                y_draw += y_j
                winner = player_1
                loser = player_2

            fight_info[winner] += round
            fight_info[loser] -= round

        example_cutoff = min(len(X_win), len(X_lose))
        if example_cutoff != 0:
            for player in players:
                n = octave.back_prop(
                    player, 
                    np.array(X_win[:example_cutoff] + X_lose[:example_cutoff] + X_draw[:min(len(X_draw), 2 * example_cutoff)]), 
                    np.array(y_win[:example_cutoff] + y_lose[:example_cutoff] + y_draw[:min(len(y_draw), 2 * example_cutoff)]),
                    0.01
                )

    strongest = max(fight_info, key = fight_info.get)
    folder = '/home/joseph/Desktop/chess_neural_network/elite_data/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    if strongest != 1:
        shutil.copyfile(f'/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{strongest}.mat', 
                        f'/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{1}.mat'
    )
    
    players.sort(key = lambda player: fight_info[player], reverse = True)
    survivors = players[:survivor_num]
    death = players[survivor_num:]
    
    print(survivors)
    print("number of survivors: ", len(survivors))

    for player in death:
        os.remove(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{player}.mat")
    
    survivors.sort()
    n = 1
    for player in survivors:
        os.rename(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{player}.mat", f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{n}.mat")
        n += 1

    folder = '/home/joseph/Desktop/chess_neural_network/parent_engine_data/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    source = '/home/joseph/Desktop/chess_neural_network/engine_data/'
    destination = '/home/joseph/Desktop/chess_neural_network/parent_engine_data/'
  
    allfiles = os.listdir(source)
    population = len(allfiles)
    print("Population: ", population)
  
    for f in allfiles:
        shutil.move(source + f, destination + f)


def reproduction(population):
    octave.addpath("/home/joseph/Desktop/chess_neural_network")
    for datasets in range(population // 4):
        dataset_1 = (datasets + 1) * 2
        dataset_2 = dataset_1 - 1
        n = octave.reproduction(dataset_1, dataset_2, dataset_1, dataset_2)

def multi_reproduction(goal_population):

    current_population = 0

    folder = '/home/joseph/Desktop/chess_neural_network/engine_data/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    population = len(os.listdir('/home/joseph/Desktop/chess_neural_network/parent_engine_data/'))
    while current_population < goal_population:

        parent_1 = random.randint(1, population)

        parent_2 = random.randint(1, population)
        while parent_2 == parent_1:
            parent_2 = random.randint(1, population)

        n = octave.reproduction_single(parent_1, parent_2, current_population + 1)
        current_population += 1


def mutation(mutation_rate):

    allfiles = os.listdir('/home/joseph/Desktop/chess_neural_network/engine_data/')
    population = len(allfiles)

    for dataset in range(population//2):
        n = octave.mutation(dataset + 1, mutation_rate)

def generation_sequence(heats, survivor_num, goal_population, mutation_rate, self_training, heat_size):
    if self_training:
        multi_tournament_self_train(heats, survivor_num, heat_size)
    else:
        multi_tournament(heats, survivor_num)
    
    # multi_reproduction(goal_population)
    # mutation(mutation_rate)
    source = '/home/joseph/Desktop/chess_neural_network/parent_engine_data/'
    destination = '/home/joseph/Desktop/chess_neural_network/engine_data/'
  
    allfiles = os.listdir(source)
  
    for f in allfiles:
        shutil.move(source + f, destination + f)
    
def genetic_algorithm(population, survivor_num, generations, descend_generations, heats, mutation_rate, layer_1, layer_2, self_training = False, heat_size = 1):

    tic = time.perf_counter()
    theta_init(np.array([770, layer_1]), np.array([layer_1 + 1, layer_2]), np.array([layer_2 + 1, 1.]), population)
    octave.addpath("/home/joseph/Desktop/chess_neural_network")

    for i in range(generations - 1):
        print(f"Gen: {i + 1} / {generations}")
        generation_sequence(heats, survivor_num, population, mutation_rate, self_training, heat_size) 
        shutil.copy(
            f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_1.mat", 
            f"/home/joseph/Desktop/chess_neural_network/best_of_generations/neural_net_dataset_{i + 1}.mat"
        )

    print(f"Gen: {generations} / {generations}")
    generation_sequence(heats, 1, population, mutation_rate, self_training, heat_size) 
    shutil.copy(
        f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_1.mat", 
        f"/home/joseph/Desktop/chess_neural_network/best_of_generations/neural_net_dataset_{generations}.mat"    
    )

    toc = time.perf_counter()
    print(toc - tic)
