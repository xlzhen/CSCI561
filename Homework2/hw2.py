'''
    Xiaoling Zheng
    CS 561 hw 2
    Oct.22 2018
    
    Description: an implementation of maxmax game program (comparing to minimax); an inefficient but working copy.
'''

import copy

def add_utilities(days, sev_digit):
    days['mondays'] += int(sev_digit[0])
    days['tuesdays'] += int(sev_digit[1])
    days['wednesdays'] += int(sev_digit[2])
    days['thursdays'] += int(sev_digit[3])
    days['fridays'] += int(sev_digit[4])
    days['saturdays'] += int(sev_digit[5])
    days['sundays'] += int(sev_digit[6])
    
    util = int(sev_digit[0]) + int(sev_digit[1]) + int(sev_digit[2]) + int(sev_digit[3]) + int(sev_digit[4]) + int(sev_digit[5]) + int(sev_digit[6])
    return util

class game_engine:
    def __init__(self, SPLA, LAHSA):
        self.SPLA = SPLA
        self.LAHSA = LAHSA
    
    def add_details(self, pool, SPLA_occupied, LAHSA_occupied):
        self.state = game_state(pool)
        self.state.add_SPLA(SPLA_occupied)
        self.state.add_LAHSA(LAHSA_occupied)
    
    def maxmax(self):
        moves = self.state.available_SPLA() # SPLA
        if moves:
            next_move = moves[0] # temp
            util = 0 # temp
            for move in moves:
                if self.SPLA.evaluate_step(self.state.SPLA_util, self.state.SPLA_days, move[13:20]):
                    temp = self.state.next_state_SPLA(move)
                    SPLA, LAHSA = self.max_LAHSA(temp)
                    if SPLA > util:
                        util = SPLA
                        next_move = move
        return next_move

    def max_SPLA(self, state):
        moves = state.available_SPLA() # SPLA
        if moves:
            util = 0
            util_2 = 0
            for move in moves:
                if self.SPLA.evaluate_step(state.SPLA_util, state.SPLA_days, move[13:20]):
                    temp = state.next_state_SPLA(move)
                    SPLA, LAHSA = self.max_LAHSA(temp)
                    if SPLA > util:
                        util = SPLA
                        util_2 = LAHSA
            return util, util_2
        else:
            return state.SPLA_util, state.LAHSA_util

    

    def max_LAHSA(self, state):
        moves = state.available_LAHSA()
        if moves:
            util = 0
            util_2 = 0
            for move in moves:
                if self.LAHSA.evaluate_step(state.LAHSA_util, state.LAHSA_days, move[13:20]):
                    temp = state.next_state_LAHSA(move)
                    SPLA, LAHSA = self.max_SPLA(temp)
                    if LAHSA > util_2:
                        util = SPLA
                        util_2 = LAHSA
            return util, util_2
        else:
            moves_ = state.available_SPLA()
            if moves_:
                for applicant in state.available_SPLA():
                    if self.SPLA.evaluate_step(state.SPLA_util, state.SPLA_days, applicant[13:20]):
                        state.SPLA_util += add_utilities(state.SPLA_days, applicant[13:20])
                        state._pools.remove(applicant)
            return state.SPLA_util, state.LAHSA_util


class game_state:
    def __init__(self, pools):
        self._pools = pools
        
        self.SPLA_days = {}
        self.SPLA_days['mondays'] = 0
        self.SPLA_days['tuesdays'] = 0
        self.SPLA_days['wednesdays'] = 0
        self.SPLA_days['thursdays'] = 0
        self.SPLA_days['fridays'] = 0
        self.SPLA_days['saturdays'] = 0
        self.SPLA_days['sundays'] = 0
        
        self.LAHSA_days = {}
        self.LAHSA_days['mondays'] = 0
        self.LAHSA_days['tuesdays'] = 0
        self.LAHSA_days['wednesdays'] = 0
        self.LAHSA_days['thursdays'] = 0
        self.LAHSA_days['fridays'] = 0
        self.LAHSA_days['saturdays'] = 0
        self.LAHSA_days['sundays'] = 0
        
        self.SPLA_occupied = []
        self.LAHSA_occupied = []
        
        self.SPLA_util = 0
        self.LAHSA_util = 0


    def add_SPLA(self, SPLA_occupied):
        self.SPLA_occupied = SPLA_occupied
        for occupied in self.SPLA_occupied:
            self.SPLA_util = add_utilities(self.SPLA_days, occupied[13:20]) + self.SPLA_util

    def add_LAHSA(self, LAHSA_occupied):
        self.LAHSA_occupied = LAHSA_occupied
        for occupied in self.LAHSA_occupied:
            self.LAHSA_util = add_utilities(self.LAHSA_days, occupied[13:20]) + self.LAHSA_util

    def next_state_SPLA(self, applicant):
        
        if self._pools == []:
            return False
        
        new_state = game_state(copy.deepcopy(self._pools))
        
        new_state.SPLA_days = copy.deepcopy(self.SPLA_days)
        new_state.LAHSA_days = copy.deepcopy(self.LAHSA_days)
        new_state.SPLA_occupied = copy.deepcopy(self.SPLA_occupied)
        new_state.LAHSA_occupied = copy.deepcopy(self.LAHSA_occupied)
        new_state.SPLA_util = copy.deepcopy(self.SPLA_util)
        new_state.LAHSA_util = copy.deepcopy(self.LAHSA_util)
        
        self.take_step(new_state._pools, applicant, new_state.SPLA_occupied)
        
        new_state.SPLA_util = add_utilities(new_state.SPLA_days, applicant[13:20]) + new_state.SPLA_util
        
        return new_state
    
    def next_state_LAHSA(self, applicant):
        
        if self._pools == []:
            return False
        
        new_state = game_state(copy.deepcopy(self._pools))
        new_state.SPLA_days = copy.deepcopy(self.SPLA_days)
        new_state.LAHSA_days = copy.deepcopy(self.LAHSA_days)
        new_state.SPLA_occupied = copy.deepcopy(self.SPLA_occupied)
        new_state.LAHSA_occupied = copy.deepcopy(self.LAHSA_occupied)
        new_state.SPLA_util = copy.deepcopy(self.SPLA_util)
        new_state.LAHSA_util = copy.deepcopy(self.LAHSA_util)
        
        self.take_step(new_state._pools, applicant, new_state.LAHSA_occupied)

        new_state.LAHSA_util = add_utilities(new_state.LAHSA_days, applicant[13:20]) + new_state.LAHSA_util
        
        return new_state
    
    def available_SPLA(self): # return current available SPLA
        pools = []
        for applicant in self._pools:
            if applicant[10:13] == "NYY":
                pools.append(applicant)
        return pools


    def available_LAHSA(self): # return current available LAHSA
        pools = []
        for applicant in self._pools:
            if applicant[5] == "F" and int(applicant[7:9]) > 17 and applicant[9] == "N":
                pools.append(applicant)
        return pools

    def available_applicants(self):
        return self._pools # return all applicants

    def take_step(self, pools, applicant, occupied):
        occupied.append(applicant)
        if applicant in self._pools:
            pools.remove(applicant)

class MaxUtilities_player:
    def __init__(self, capacity):
        self._capacity = capacity
   
    def evaluate_step(self, util, days, seven_digit):
        if util >= self._capacity * 7: return False
        
        if seven_digit[0] == 1 and days['mondays'] == self._capacity or seven_digit[1] == 1 and days['tuesdays'] == self._capacity or seven_digit[2] == 1 and days['wednesdays'] == self._capacity or seven_digit[3] == 1 and days['thursdays'] == self._capacity or seven_digit[4] == 1 and days['fridays'] == self._capacity or seven_digit[5] == 1 and days['saturdays'] == self._capacity or seven_digit[6] == 1 and days['sundays'] == self._capacity:
            return False
        
        return True

def main():
    fp_in = open("input.txt", "r")
    
    number_of_beds_in_shelter = int(fp_in.readline())
    number_of_spaces_in_parking_lot = int(fp_in.readline())
    
    number_of_applicants_LAHSA = int(fp_in.readline())
    chosen_LAHSA_id = []
    for i in range(0,number_of_applicants_LAHSA):
        chosen_LAHSA_id.append(int(fp_in.readline()))
    number_of_applicants_SPLA = int(fp_in.readline())
    chosen_SPLA_id = []
    for i in range(0,number_of_applicants_SPLA):
        chosen_SPLA_id.append(int(fp_in.readline()))

    total_number_of_applicants = int(fp_in.readline())
    all_applicants_info = []
    for i in range(0, total_number_of_applicants):
        all_applicants_info.append(str(fp_in.readline()).strip('\n').strip('\r'))
    fp_in.close()

    pool_info = []
    chosen_LAHSA_info = []
    chosen_SPLA_info = []

    for info in all_applicants_info:
        if int(info[:5]) in chosen_LAHSA_id:
            chosen_LAHSA_info.append(info)
        elif int(info[:5]) in chosen_SPLA_id:
            chosen_SPLA_info.append(info)
        elif info[10:13] == "NYY":
            pool_info.append(info)
        elif info[5] == "F" and int(info[7:9]) > 17 and info[9] == "N":
            pool_info.append(info)

    Game = game_engine(MaxUtilities_player(number_of_spaces_in_parking_lot), MaxUtilities_player(number_of_beds_in_shelter))

    Game.add_details(pool_info, chosen_SPLA_info, chosen_LAHSA_info)

    next_SPLA = Game.maxmax()

    fp_out = open("output.txt", "w+")
    fp_out.write(str(next_SPLA[:5])+"\n")
    fp_out.close()


if __name__ == "__main__":
    main()
