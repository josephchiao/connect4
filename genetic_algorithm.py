import re
import numpy as np
import os
import random
import time
import shutil
import theta_init
import interface
import mutation
import reproduction

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


# def tournament(rounds):
#     for r in range(rounds):
#         population = len(os.listdir('/home/joseph/Desktop/chess_neural_network/engine_data'))
#         parity_bins = [[], []]
#         for i in range(population // 2):
#             i = (i + 1) * 2

#             print(i, " vs ", (i - 1))

#             winner, loser, win_state = fight.fight([i, i - 1])
#             os.remove(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{loser}.mat")
#             parity_bins[winner % 2].append(winner)

#         folder = '/home/joseph/Desktop/chess_neural_network/engine_data/'
#         if 1 in parity_bins[1]:
#             new_num = population + 1 + population % 2
#             os.rename(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{1}.mat", f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{new_num}.mat")
#             parity_bins[1].remove(1)
#             parity_bins[1].append(new_num)

#         for x in range(population // 2):
#             bin = parity_bins[x % 2]
#             if len(bin) == 0:
#                 bin = parity_bins[x % 2 - 1]
            
#             os.rename(f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{bin[0]}.mat", f"/home/joseph/Desktop/chess_neural_network/engine_data/neural_net_dataset_{x + 1}.mat")
#             bin.pop(0)


def multi_tournament_phase_1(heats, survivor_num, nn_depth, random_depth):

    red_win_stat = 0
    yellow_win_stat = 0
    win_ratio = None
    draw_stat = 0

    population = len(os.listdir('/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data'))
    # print("Current population: ", population)

    players = list(range(population))
    fight_sequense = list(players)
    fight_info = {players[i]: 0 for i in range(len(fight_sequense))}

    for heat in range(heats):
        for round in range(population):
            player = fight_sequense[round]
            
            print(f"Heat: {heat + 1} / {heats}", f"       Round: {round + 1} / {population}")

            red_win, yellow_win, draw = interface.nn_vs_random(player, nn_depth, random_depth)

            if red_win:
                fight_info[player] -= 1
                red_win_stat += 1
            elif yellow_win:
                fight_info[player] += 1
                yellow_win_stat += 1
            elif draw:
                fight_info[player] -= 0.25
                draw_stat += 1
            
            if red_win_stat != 0:
                win_ratio = yellow_win_stat/red_win_stat

            print("Red wins = ", red_win_stat, "   Yellow wins = ", yellow_win_stat, "   Draws = ", draw_stat, "   Win ratio = ", win_ratio)

    print(fight_info)

    strongest = max(fight_info, key = fight_info.get)
    print(strongest)
    
    folder = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    
    shutil.copyfile(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{strongest}.npz', 
                    f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data/nn_theta_set_0.npz'
    )
    
    players.sort(key = lambda player: fight_info[player], reverse = True)
    survivors = players[:survivor_num]
    death = players[survivor_num:]
    
    print(survivors)
    print("number of survivors: ", len(survivors))

    for player in death:
        os.remove(f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{player}.npz")
    
    survivors.sort()
    n = 0
    for player in survivors:
        os.rename(f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{player}.npz", 
                  f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{n}.npz")
        n += 1
    
    folder = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_parent_data'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    source = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/'
    destination = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_parent_data/'
  
    allfiles = os.listdir(source)
    population = len(allfiles)
    print("Population: ", population)
  
    for f in allfiles:
        shutil.move(source + f, destination + f)


def multi_tournament_phase_2(heats, survivor_num, nn_depth, random_depth, previous_eval):

    red_win_stat = 0
    yellow_win_stat = 0
    win_ratio = None
    draw_stat = 0

    population = len(os.listdir('/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data'))
    # print("Current population: ", population)

    fight_sequense = list(range(population))
    fight_info = {fight_sequense[i]: 0 for i in range(len(fight_sequense))}

    for heat in range(heats):
        for round in range(population):
            player = fight_sequense[round]
            
            print(f"Heat: {heat + 1} / {heats}", f"       Round: {round + 1} / {population}")

            red_win, yellow_win, draw = interface.nn_vs_nn(player, heat, nn_depth, random_depth)

            if red_win:
                fight_info[player] -= 1
                red_win_stat += 1
            elif yellow_win:
                fight_info[player] += 1
                yellow_win_stat += 1
            elif draw:
                fight_info[player] -= 0.25
                draw_stat += 1
            
            if red_win_stat != 0:
                win_ratio = yellow_win_stat/red_win_stat

            print("Red wins = ", red_win_stat, "   Yellow wins = ", yellow_win_stat, "   Draws = ", draw_stat, "   Win ratio = ", win_ratio)

    print(fight_info)

    strongest = max(fight_info, key = fight_info.get)
    print(strongest)
    
    folder = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    
    shutil.copyfile(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{strongest}.npz', 
                    f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data/nn_theta_set_0.npz'
    )
    
    fight_sequense.sort(key = lambda player: fight_info[player], reverse = True)
    survivors = fight_sequense[:survivor_num]
    trainer = fight_sequense[:heats]
    death = fight_sequense[survivor_num:]
    
    print(survivors)
    print("number of survivors: ", len(survivors))

    folder = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_trainer_data'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for player in trainer:
        shutil.copyfile(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{strongest}.npz', 
                    f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data/nn_theta_set_0.npz'
    )

    for player in death:
        os.remove(f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{player}.npz")
    
    survivors.sort()
    n = 0
    for player in survivors:
        os.rename(f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{player}.npz", 
                  f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{n}.npz")
        n += 1
    
    folder = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_parent_data'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    source = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/'
    destination = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_parent_data/'
  
    allfiles = os.listdir(source)
    population = len(allfiles)

    print("Population: ", population)
  
    for f in allfiles:
        shutil.move(source + f, destination + f)

    return eval

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

def multi_reproduction(goal_population, population):

    current_population = 0

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
    
    while current_population < goal_population:

        parent_1 = random.randint(0, population - 1)

        parent_2 = random.randint(0, population - 1)
        while parent_2 == parent_1:
            parent_2 = random.randint(0, population - 1)

        theta_1, theta_2, theta_3 = reproduction.basic_reproduction(parent_1, parent_2)
        np.savez(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{current_population}.npz', Theta1 = theta_1, Theta2 = theta_2, Theta3 = theta_3)
        current_population += 1

    shutil.copyfile(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data/nn_theta_set_0.npz', 
                    f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_0.npz'
    )

def mutate(mutation_rate):

    allfiles = os.listdir('/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data')
    population = len(allfiles)

    for dataset in range(population):
        mutation.point_mutaion(dataset, mutation_rate)

def generation_sequence(heats, survivor_num, goal_population, mutation_rate, training_phase, heat_size, nn_depth, random_depth):
    
    if training_phase == 1:
        multi_tournament_phase_1(heats, survivor_num, nn_depth, random_depth)
    elif training_phase == 2:
        multi_tournament_phase_2(heats, survivor_num, nn_depth, random_depth)
    
    multi_reproduction(goal_population, survivor_num)
    mutate(mutation_rate)
    
def genetic_algorithm(survivor_num, generations, heats, mutation_rate, nn_depth, random_depth, training_phase = 1, heat_size = 1):

    allfiles = os.listdir('/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data')
    population = len(allfiles)

    tic = time.perf_counter()

    for i in range(generations):
        print(f"Gen: {i + 1} / {generations}")
        generation_sequence(heats, survivor_num, population, mutation_rate, training_phase, heat_size, nn_depth, random_depth) 
        shutil.copy(
            f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_1.npz", 
            f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/generation_best_data/nn_theta_set_{i + 1}.npz"
        )

    toc = time.perf_counter()
    print(toc - tic)


# multi_tournament(2, 8)
# theta_generate((85,25), (26,25), (26, 1), 256)
genetic_algorithm(16, 100, 5, 0.005, 2, 5)