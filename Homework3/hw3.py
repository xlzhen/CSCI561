
# policy iteration

import collections
import itertools
import copy
import numpy as np

DISCOUNT_FACTOR = 0.9

class State:
    def __init__(self, dimension, grid, obstacles, start_loc, end_loc):
        self.grid = grid
        self.dimension = dimension
        self.obstacles = obstacles
        self.start_loc = start_loc
        self.end_loc = end_loc
    
    def get_reward(self, move):
        res = 0
        if move in self.obstacles:
            res += -100.0
        elif move == self.end_loc:
            res += 100.0
        return res - 1.0

    def in_block(self, move):
        if move[0] < 0 or move[0] >= self.dimension or move[1] < 0 or move[1] >= self.dimension:
            return False
        else: return True

    def max_action(self, x, y):
        
        orientations = EAST, NORTH, WEST, SOUTH = [(1,0), (0,-1),(-1,0),(0,1)]
        
        move_N = (NORTH[0] + x, NORTH[1] + y)
        if not self.in_block(move_N):
            move_N = (x, y)

        move_E = (EAST[0] + x, EAST[1] + y)
        if not self.in_block(move_E):
            move_E = (x, y)

        move_W = (WEST[0] + x, WEST[1] + y)
        if not self.in_block(move_W):
            move_W = (x, y)

        move_S = (SOUTH[0] + x, SOUTH[1] + y)
        if not self.in_block(move_S):
            move_S = (x, y)

        R_north = self.get_reward(move_N)
        grid_N = self.grid[move_N[0]][move_N[1]]
        
        R_west = self.get_reward(move_W)
        grid_W = self.grid[move_W[0]][move_W[1]]
        
        R_south = self.get_reward(move_S)
        grid_S = self.grid[move_S[0]][move_S[1]]
        
        R_east = self.get_reward(move_E)
        grid_E = self.grid[move_E[0]][move_E[1]]

        Rewards_north = 0.7 * grid_N + 0.1 * grid_W + 0.1 * grid_S + 0.1 * grid_E
        Rewards_west = 0.7 * grid_W + 0.1 * grid_N + 0.1 * grid_S + 0.1 * grid_E
        Rewards_south = 0.7 * grid_S + 0.1 * grid_W + 0.1 * grid_E + 0.1 * grid_N
        Rewards_east = 0.7 * grid_E + 0.1 * grid_W + 0.1 * grid_S + 0.1 * grid_N
        
        tmp = np.array([Rewards_north, Rewards_south, Rewards_east, Rewards_west], dtype=np.float64)
        i = np.argmax(tmp)
        rewards = [Rewards_north,Rewards_south, Rewards_east, Rewards_west]
        actions = [NORTH, SOUTH, EAST, WEST]
        
        return (rewards[i], actions[i])

    def policy_parser(self):
        policies = {}
        for x in range(self.dimension):
            for y in range(self.dimension):
                if (x, y) == self.end_loc:
                    policies[(x,y)] = None
                else:
                    _, action = self.max_action(x, y)
                    policies[(x,y)] = action
        return policies


    def value_iteration(self, epsilon = 0.1):
        delta = 0
        while True:
            temp_grid = [[0]*self.dimension for i in range(self.dimension)]
            for x in range(self.dimension):
                for y in range(self.dimension):
                    temp_grid[x][y] = self.get_reward((x, y))
            delta = 0
            for x in range(self.dimension):
                for y in range(self.dimension):
                    if (x,y) == self.end_loc:
                        continue
                    best_action_val, _ = self.max_action(x, y)
                    temp_grid[x][y] = self.get_reward((x,y)) + DISCOUNT_FACTOR * best_action_val
                    delta = max(delta, abs(temp_grid[x][y] - self.grid[x][y]))
            if delta <= epsilon:
                break
            else:
                self.grid = temp_grid[:]

def policy_simulation(cars, ends, policies, obstacles, dimension):

    avg = []
    
    orientations = EAST, NORTH, WEST, SOUTH = [(1,0), (0,-1),(-1,0),(0,1)]
    turns = LEFT, RIGHT = (+1, -1)

    def turn_heading(heading, inc, headings=orientations):
        return headings[(headings.index(heading) + inc) % len(headings)]

    def turn_right(heading):
        return turn_heading(heading, RIGHT)

    def turn_left(heading):
        return turn_heading(heading, LEFT)
    
    for i in range(len(cars)):
        cost = 0
        for j in range(10):
            pos = cars[i]
            np.random.seed(j)
            swerve = np.random.random_sample(1000000)
            k = 0
            while pos != ends[i]:
                move = policies[i][pos]
                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            move = turn_right(turn_right(move))
                        else:
                            move = turn_right(move)
                    else:
                        move = turn_left(move)
                next_pos = (move[0] + pos[0], move[1] + pos[1])
                if next_pos[0] < 0 or next_pos[0] >= dimension or next_pos[1] < 0 or next_pos[1] >= dimension:
                    next_pos = pos
                if next_pos == ends[i]:
                    cost += 99.0
                elif next_pos in obstacles:
                    cost += -101.0
                else:
                    cost += -1.0
                pos = next_pos
                k += 1
        avg.append(int(cost/10.0))
    return avg

def main():
    fp_in = open("input.txt", "r")

    grid = []
    obstacles = []
    start_loc = []
    end_loc = []

    dimension = int(fp_in.readline()) # size of grid
    number_of_car = int(fp_in.readline())
    number_of_obstacle = int(fp_in.readline())
    
    grid = [[0]*dimension for i in range(dimension)]

    for _ in range(number_of_obstacle):
        coord = fp_in.readline().strip("/r").split(",")
        obstacles.append((int(coord[0]), int(coord[1])))
    
    for _ in range(number_of_car):
        coord = fp_in.readline().strip("/r").split(",")
        start_loc.append((int(coord[0]), int(coord[1])))

    for _ in range(number_of_car):
        coord = fp_in.readline().strip("/r").split(",")
        end_loc.append((int(coord[0]), int(coord[1])))

    policies = []

    for i in range(len(start_loc)):
        x = State(dimension, grid, obstacles, start_loc[i], end_loc[i])
        x.value_iteration()
        policy = x.policy_parser()
        policies.append(policy)

    value = policy_simulation(start_loc, end_loc, policies, obstacles, dimension)

    fp_out = open("output.txt", "w+")
    for sol in value:
        fp_out.write(str(sol)+"\n")
    fp_out.close()

if __name__ == "__main__":
    main()

