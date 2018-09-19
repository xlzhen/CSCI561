#    Xiaoling Zheng
#    CSCI.561 hw1b
#    Sept. 17 2018
#
#    Description: An invariant of N-queens problem; sovlved by DFS with greedy approach prunings 
#

from heapq import heappush, heappop
import itertools

TIME_STEP = 12

class BestValue:
    def __init__(self, dimension, table, index_list, rows, rows_ind):
        self._dimension = dimension
        self._table = table
        self._index_list = index_list
        self._solution = 0                              # store optimal solution
        self._board = [-5 for i in range(dimension)]    # board track officer placement
        self._rows = rows                               # self._rows[i] store max value of row[i]
        self._rows_ind = rows_ind                       # self._rows_ind stores order of expanding for dfs, greedy approach for better pruning

    def _isvalid(self, i, j):                           # function validate a point on board
        for k in range(i):
            if self._board[k] == j or abs(i - k) == abs(self._board[k] - j):   # if it conflicts with any other (same row, same column, same diagonal), return false; else return true
                return False
        return True
        
    def _recursive_dfs(self, indexes, depth, row, max_points, index_len):
        if depth == index_len:                          # if find a possible solution
            if self._solution < row:
                self._solution = row                    # if has higher value than previous local optimum solution, update self._solution to new local optimum
            return                                      # end of one recursion
        for i in self._rows_ind[depth]:                 # iterate indexes in descending order of time passes a column, greedy approach for better pruning
            if self._isvalid(indexes[depth], i) and max_points > self._solution:   # validate a potential point; cut the search if max_points is (max potential points) less than local optimum solution
                self._board[indexes[depth]] = i         # place point on board; update board information
                self._recursive_dfs(indexes, depth+1, row + self._table[indexes[depth]][i], max_points - self._rows[indexes[depth]] + self._table[indexes[depth]][i], index_len)
                                                        # recursive dfs, deeper level (depth + 1), accumulated gained points (row + value of placed location), further constrained max_points (greedy approach, better for pruning)

    def run_solver(self):
        '''
            driver of the class BestValue, which iterate through possible solutions with recursive dfs, plus greedy and pruning
        '''
        #sort order of indexes in self._index_list
        heapmin = []
        index_len = len(self._index_list[0])
        for indexes in self._index_list:
            max = 0
            for j in indexes:
                max -= self._rows[j]
                heappush(heapmin, (max, indexes))
        #sort order of indexes in self._index_list

        #call dfs for each possible combination of indexes
        for i in range(len(self._index_list)):
            indexes = heappop(heapmin)
            max_pos = 0 - indexes[0]
            self._recursive_dfs(indexes[1], 0, 0, max_pos, index_len)
            self._board = [-5 for i in range(self._dimension)]
        #call dfs for each possible combination of indexes

        return self._solution

def main():
    fp_in = open("input.txt", "r")
    # read file, store values into variable; populate table
    dimension = int(fp_in.readline())
    num_of_officer = int(fp_in.readline())
    num_of_scooter = int(fp_in.readline())

    table = []
    rows_ind = []
    heapmin = []
    
    for i in range(dimension):
        table.append([0]*dimension)
        rows_ind.append([0]*dimension)
        heapmin.append([])

    for x in range(num_of_scooter):
        for line in range(TIME_STEP):
            x_coord, y_coord = fp_in.readline().split(",")
            table[int(x_coord)][int(y_coord)] += 1
    # read file, store values into variable; populate table
    fp_in.close()

    rows = []
    # find maximum value across each row; for faster pruning
    for i in range(dimension):
        rows.append(max(table[i]))
    # find maximum value across each row; for faster pruning

    # find descending index values for each row; for faster pruning
    for i in range(dimension):
        for j in range(dimension):
            heappush(heapmin[i], (0 - table[i][j], (i, j)))

    for i in range(dimension):
        for j in range(dimension):
            rows_ind[i][j] = heappop(heapmin[i])[1][1]
    # find descending index values for each row; for faster pruning

    index_list = list(itertools.combinations([x for x in range(dimension)], num_of_officer))
    # generate permutation of possible column sols

    location_solver = BestValue(dimension, table, index_list, rows, rows_ind)
    sol = location_solver.run_solver()

    # write to output.txt
    fp_out = open("output.txt", "w+")
    fp_out.write(str(sol)+"\n")
    fp_out.close()
    # write to output.txt

if __name__ == "__main__":
    main()


