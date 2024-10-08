import numpy as np
import os
import random
import time
import shutil
import archive.theta_init as theta_init
import interface
import mutation
import reproduction
import matplotlib.pyplot as plt # type: ignore

def theta_generate(Theta_1_size, Theta_2_size, Theta_3_size, n):

    """For initializing training set"""

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
        theta_init.create_file(Theta_1_size, Theta_2_size, Theta_3_size, file_name = f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{dataset}.npz", init_type = "logistic")

def theta_review(theta_set):

    """Display purposes"""

    theta = np.load(f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data/nn_theta_set_0.npz")
    # theta = np.load("/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/manuel_best_copy/Nov 27 depth 6 unbeatable")
    # theta = np.load(f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{theta_set}.npz")
    print(theta['Theta1'])
    print(theta['Theta2'])
    print(theta['Theta3'])

    y = np.arange(0, np.size(theta['Theta1'])) 
    x = theta['Theta1']
    # print(np.size(x))
    # print(np.size(y))

    plt.scatter(x, y, s = 5)
    plt.show()

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


def multi_tournament_phase_2(heats, survivor_num, nn_depth, random_depth):

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
                    f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_elite_data/nn_theta_set_0.npz')
    
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

    n = 0
    for player in trainer:
        shutil.copyfile(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{strongest}.npz', 
                    f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_trainer_data/nn_theta_set_{n}.npz')
        n += 1

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
        shutil.copyfile(
            f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_0.npz", 
            f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/generation_best_data/nn_theta_set_{i}.npz"
        )

    toc = time.perf_counter()
    print(toc - tic)


# theta_generate((85,50), (51,50), (51, 1), 256)
# genetic_algorithm(16, 100, 5, 0.005, 2, 4, training_phase=2)


# for i in range(4):
#     fig = plt.figure(num = 100 - i)
#     theta_review(100 - i)
# plt.show()

theta_review(0)



