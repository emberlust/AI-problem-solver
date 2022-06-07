from search import *

class CarProblem(Problem):
    
    def __init__(self, size):

        self.car = 0

        self.can_hop = [0] * (size * size)

        indexes = []
        #a dummy car
        indexes.append(0)

        #initial indexes are the car numbers in ascending order placed on the last row
        for i in range(size):
            indexes.append(size * (size-1) + i)

        self.initial = tuple(indexes)
  
        f_indexes = []
        #a dummy car
        f_indexes.append(0)

        #final indexes are the car numbers reversed placed on the first row
        for i in range(size):
            f_indexes.append(size - i - 1)

        self.goal = tuple(f_indexes)

        self.size = size

        Problem.__init__(self,self.initial,self.goal)

    def actions(self, state):

        #choosing witch car to move (it just loops between them)
        if self.car == self.size:
            self.car = 1
        else:
            self.car += 1

        car = self.car
        index = state[car]

        car_actions = ['STAY' + str(car),'UP' + str(car), 'DOWN' + str(car), 'LEFT' + str(car), 'RIGHT' + str(car),'HUP' + str(car),'HDOWN' + str(car),'HLEFT' + str(car),'HRIGHT' + str(car)]
        
        #test if car doesnt leave the parking lot when moving
        if index % self.size == 0:
            car_actions.remove('LEFT' + str(car))
        if index < self.size:
            car_actions.remove('UP' + str(car))
        if index % self.size == self.size - 1:
            car_actions.remove('RIGHT' + str(car))
        if index >= self.size * (self.size - 1):
            car_actions.remove('DOWN' + str(car))


        #test if car doesnt leave the parking lot when hopping and also if hopping is valid (a car must stay in place for another one to hop over it)
        if index % self.size <= 1:
            car_actions.remove('HLEFT' + str(car))
        elif self.can_hop[index - 1] != 1:
                 if ('HLEFT' + str(car)) in car_actions:
                    car_actions.remove('HLEFT' + str(car))
        if index < self.size * 2:
            car_actions.remove('HUP' + str(car))
        elif self.can_hop[index - self.size] != 1:
                 if ('HUP' + str(car)) in car_actions:
                    car_actions.remove('HUP' + str(car))
        if index % self.size >= self.size - 2:
            car_actions.remove('HRIGHT' + str(car))
        elif self.can_hop[index + 1] != 1:
                 if ('HRIGHT' + str(car)) in car_actions:
                    car_actions.remove('HRIGHT' + str(car))
        if index > self.size*self.size - 2 * self.size - 1:
            car_actions.remove('HDOWN' + str(car))
        elif self.can_hop[index + self.size] != 1:
                if ('HDOWN' + str(car)) in car_actions:
                    car_actions.remove('HDOWN' + str(car))

        #test if the car doesnt interesct with another when moving
        for idx in range(1,self.size + 1):
            index2 = state[idx]
            if idx == car:
               continue
            if index - 1 == index2:
                if ('LEFT' + str(car)) in car_actions:
                    car_actions.remove('LEFT' + str(car))
            if index - self.size == index2:
                if ('UP' + str(car)) in car_actions:
                    car_actions.remove('UP' + str(car))
            if index + 1 == index2:
                if ('RIGHT' + str(car)) in car_actions:
                    car_actions.remove('RIGHT' + str(car))
            if index + self.size == index2:
                 if ('DOWN' + str(car)) in car_actions:
                    car_actions.remove('DOWN' + str(car))
            ##############################################
            if index - 2 == index2:
                if ('HLEFT' + str(car)) in car_actions:
                    car_actions.remove('HLEFT' + str(car))
            if index - 2 * self.size == index2:
                if ('HUP' + str(car)) in car_actions:
                    car_actions.remove('HUP' + str(car))
            if index + 2 == index2:
                if ('HRIGHT' + str(car)) in car_actions:
                    car_actions.remove('HRIGHT' + str(car))
            if index + 2 * self.size == index2:
                if ('HDOWN' + str(car)) in car_actions:
                    car_actions.remove('HDOWN' + str(car))

        return car_actions


    def result(self,state,action):

        car = self.car
        index = state[car]
        new_state = list(state)
  

        delta = {'STAY' + str(car):0,'UP' + str(car):-self.size,'DOWN' + str(car):self.size,'LEFT' + str(car):-1, 'RIGHT' + str(car):1,'HUP' + str(car):-(2*self.size),'HDOWN' + str(car):(2*self.size),'HLEFT' + str(car):-2, 'HRIGHT' + str(car):2}

        if delta[action] == 0:
            self.can_hop[index] = 1
        else:
            self.can_hop[index] = 0
        new_state[car] = new_state[car] + delta[action]

        return tuple(new_state)

    #test if initial indexes are equal to the goal ones
    def goal_test(self,state):
        return state == self.goal

    #mnht dist
    def h(self,node):

        dist = 0
        for(s,g) in zip(node.state,self.goal):
            if s != g:
                dist += abs(s-g) * 2

        return dist