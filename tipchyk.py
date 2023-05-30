import random
import math
from havka import Havka
from itertools import product

class States:
    hungry = 'hungry'
    horny = 'horny'
    exploring = 'exploring'
    rage = 'rage'
    dead = 'dead'


class Races:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    GREEN = (0, 255, 0)


def get_color(rgb):
    if rgb == Races.BLACK:
        return 'black'
    if rgb == Races.WHITE:
        return 'white'
    if rgb == Races.ORANGE:
        return 'orange'
    if rgb == Races.YELLOW:
        return 'yellow'


class Tip4yk:
    def __init__(self, genom, race, cords, start_energy, start_state = States.hungry) -> None:
        # health, libido, strength, stamina
        self.genom = genom
        self.race = race
        self.cords = cords
        self.state = start_state
        self.energy = self.genom[3] *10/3

    def find_nearby_food(self, world):
        grid = world.havka.grid
        ans = []
        for r in range(1,4):
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    if i == 0 and j == 0:
                        continue
                    try:
                        if isinstance(grid[self.cords[0]+i][self.cords[1]+j], Havka) \
                            and self.cords[0]+i>= 0 and self.cords[1]+j>=0:
                            if grid[self.cords[0]+i][self.cords[1]+j].is_ready(world.havka.day):
                                ans.append((self.cords[0]+i, self.cords[1]+j))
                    except IndexError:
                        continue
        if not ans:
            return None
        return random.choice(ans)

    def find_nearby_enemy(self, grid):
        ans = []
        for r in range(1,5):
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    if i == 0 and j == 0:
                        continue
                    try:
                        if isinstance(grid[self.cords[0]+i][self.cords[1]+j], Tip4yk)\
                            and self.cords[0]+i>= 0 and self.cords[1]+j>=0:
                            if grid[self.cords[0]+i][self.cords[1]+j].race != self.race:
                                ans.append((self.cords[0]+i, self.cords[1]+j))
                    except IndexError:
                        continue
        if not ans:
            return None
        closest_enemy = ans[0]
        for enemy in ans:
            if math.dist(self.cords, enemy) < math.dist(self.cords, closest_enemy):
                closest_enemy = enemy
        return closest_enemy

    def find_nearby_partner(self, grid, partners=False):
        partners_lst = []
        for r in range(1,3):
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    if i == 0 and j == 0:
                        continue
                    try:
                        if isinstance(grid[self.cords[0]+i][self.cords[1]+j], Tip4yk) \
                            and self.cords[0]+i>= 0 and self.cords[1]+j>=0:
                            if grid[self.cords[0]+i][self.cords[1]+j].race == self.race:
                                if partners:
                                    partners_lst.append((self.cords[0]+i, self.cords[1]+j))
                                else:
                                    return self.cords[0]+i, self.cords[1]+j
                    except IndexError:
                        continue
        if partners:
            return partners_lst
        return None

    def move(self, world, new_cords):

        if 0<=new_cords[0]<=len(world.grid)  and 0<=new_cords[1] <= len(world.grid):
            if not isinstance(world.grid[new_cords[0]][new_cords[1]], Tip4yk):
                if isinstance(world.havka.grid[new_cords[0]][new_cords[1]], Havka):
                    if self.state == States.hungry:
                        if world.havka.grid[new_cords[0]][new_cords[1]].is_ready(world.havka.day):
                            self.energy += world.havka.grid[new_cords[0]][new_cords[1]].recharge
                            world.havka.grid[new_cords[0]][new_cords[1]].got_eaten(world.havka.day)
                world.grid[self.cords[0]][self.cords[1]] = 0
                self.cords[0] = new_cords[0]
                self.cords[1] = new_cords[1]
                world.grid[new_cords[0]][new_cords[1]] = self
                self.energy -= 1
            if not isinstance(world.grid[self.cords[0]][self.cords[1]], Havka):
                world.phero.add_phero(self, world)
        else:
            self.random_move(world)


    def random_move(self, world):
        grid = world.grid
        for _ in range(1000):
            new_y = self.cords[0] + random.randint(0, 2) - 1 
            new_x = self.cords[1] + random.randint(0, 2) - 1
            if 0<= new_y<=len(grid) - 1 and 0<= new_x<=len(grid) - 1:
                if (new_y,new_x) != self.cords and not isinstance(grid[new_y][new_x], Tip4yk):
                    self.move(world,(new_y, new_x))
                    break

    def fero_move(self, world):
        grid = world.grid
        best_move = [(), 0]
        color = get_color(self.race)
        for r in range(1, 5):
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    if i == 0 and j == 0:
                        continue
                    if 0 <= self.cords[0]+i < len(grid) and 0 <= self.cords[1]+j < len(grid):
                        if not isinstance(grid[self.cords[0]+i][self.cords[1]+j], Tip4yk)\
                            and world.phero.grid[self.cords[0]+i][self.cords[1]+j][color] > best_move[1]:
                            best_move = [(self.cords[0]+i, self.cords[1]+j), world.phero.grid[self.cords[0]+i][self.cords[1]+j][color]]

        return best_move[0]

    def unfero_move(self, world):
        grid = world.grid
        best_move = [(), 10000000]
        color = get_color(self.race)
        moves = {}
        for r in range(1, 5):
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    if i == 0 and j == 0:
                        continue
                    if 0 <= self.cords[0]+i < len(grid) and 0 <= self.cords[1]+j < len(grid):
                        if not isinstance(grid[self.cords[0]+i][self.cords[1]+j], Tip4yk):
                            if world.phero.grid[self.cords[0]+i][self.cords[1]+j][color] not in moves.keys():
                                moves[world.phero.grid[self.cords[0]+i][self.cords[1]+j][color]] = []
                            moves[world.phero.grid[self.cords[0]+i][self.cords[1]+j][color]].append((self.cords[0]+i, self.cords[1]+j)) 
 
        if moves:
            return random.choice(moves[min(moves.keys())])
        return None

    def die(self, grid):
        grid[self.cords[0]][self.cords[1]] = 0

    def mutate(self, genom):
        mutate_gene = random.choice(genom)
        index_gene = genom.index(mutate_gene)
        if random.random() < self.genom[0] and genom[index_gene] < 30:
            genom[index_gene] += 1
        if random.random() < 0.15 and genom[index_gene] > 0:
            genom[index_gene] -= 1
        return genom

    def short_distance(self, grid, goal_cords):
        possible_x = []
        possible_y = []
        moves = []
        for i in range(-1, 2):
            possible_y.append(self.cords[0]+i)
        for j in range(-1, 2):
            possible_x.append(self.cords[1]+j)

        for p in product(possible_y, possible_x):
            moves.append(p)

        possible_moves = []
        for move in moves:
            if 0 <= move[0] < len(grid) and 0 <= move[1] < len(grid):
                possible_moves.append(move)
        best_move = possible_moves[0]
        for move in possible_moves:
            if math.dist(move, goal_cords) < math.dist(best_move, goal_cords):
                best_move = move
        return best_move

    def sex(self, world):
        ans = []
        grid = world.grid
        for r in range(1,3):
            for i in range(-r,r+1):
                for j in range(-r,r+1):
                    if i == 0 and j == 0:
                        continue
                    try:
                        if isinstance(grid[self.cords[0]+i][self.cords[1]+j], Tip4yk)\
                            and self.cords[0]+i>= 0 and self.cords[1]+j>=0:
                            if grid[self.cords[0]+i][self.cords[1]+j].race == self.race:
                                ans.append(grid[self.cords[0]+i][self.cords[1]+j])
                    except IndexError:
                        continue

        # zrobyty vybir partnera po fitnesu
        if ans:
            # partner = random.choice(ans)
            partner = sorted(ans, key=lambda x: x.genom[0], reverse=True)[0]
            kid_genome = []
            for i, x in enumerate(self.genom):
                kid_genome.append(int((x + partner.genom[i])//2))
            kid_genome = self.mutate(kid_genome)
            kid_cords = list(self.short_distance(grid, partner.cords))
            new_tip = Tip4yk(kid_genome, self.race, kid_cords, 45)
            world.add_tip(new_tip)

    def fight(self, world, enemy_cords):

        grid = world.grid
        # if self.race == Races.WHITE and grid[enemy_cords[0]][enemy_cords[1]].race == Races.BLACK:
        #     return enemy_cords
        sum_gene = self.genom[2] + grid[enemy_cords[0]][enemy_cords[1]].genom[2]
        if random.random() > self.genom[2]/sum_gene:
            return enemy_cords
        return self.cords


    def decide_state(self, world):
        nearby_enemy = self.find_nearby_enemy(world.grid)
        nearby_partners = self.find_nearby_partner(world.grid, partners=True)

        # if random.random() > 0.3 and not nearby_enemy and self.energy > 30:
        #     self.state = States.exploring
        if self.energy < 0:
            self.state = States.dead
            return
        elif self.state == States.hungry:

            if nearby_enemy and self.energy > 50:
                self.state = States.rage
            elif self.energy > 180:
                if nearby_enemy:
                    self.state = States.rage
                elif not nearby_enemy and nearby_partners and self.energy > 230:
                    self.state = States.horny
                else:
                    self.state = States.exploring
            else:
                self.state == States.hungry
        elif self.state == States.exploring:

            if nearby_enemy and self.energy > 40:
                self.state = States.rage
            elif self.energy <= 80:
                self.state = States.hungry
            elif not nearby_enemy and nearby_partners and self.energy > 85:
                self.state = States.horny
            else:
                self.state = States.exploring
        elif self.state == States.rage:
            
            if nearby_enemy and self.energy > 40:
                self.state = States.rage
            elif self.energy <= 80:
                self.state = States.hungry

            else:
                self.state = States.exploring
        elif self.state == States.horny:
            if nearby_enemy and self.energy > 40:
                self.state = States.rage
            elif self.energy <= 80:
                self.state = States.hungry
            else:
                self.state = States.exploring

    def decide_action(self, world):
        if self.state == States.dead:
            self.die(world.grid)
        if self.state == States.hungry:

            nearby = self.find_nearby_food(world)
            if nearby:
                diffy = nearby[0] - self.cords[0]
                diffx = nearby[1] - self.cords[1]
                if diffx < -1:
                    diffx = -1
                if diffx > 1:
                    diffx = 1
                if diffy < -1:
                    diffy = -1
                if diffy > 1:
                    diffy = 1
                self.move(world,(self.cords[0] + diffy, self.cords[1] + diffx))
            else:
                move = self.fero_move(world)
                if move:
                    if int(math.dist(move, self.cords)) == 1:
                        self.move(world, move)
                    else:
                        move = self.short_distance(world.grid, move)
                        self.move(world, move)
                else:
                    self.random_move(world)
                # self.random_move(world)
        if self.state == States.rage:
            grid = world.grid
            nearby_enemy = self.find_nearby_enemy(grid)
            if nearby_enemy:
                if int(math.dist(nearby_enemy, self.cords)) <= 1:
                    loser = self.fight(world, nearby_enemy)
                    if loser:
                        grid[loser[0]][loser[1]].state = States.dead
                        grid[loser[0]][loser[1]] = 0
                else:
                    move = self.short_distance(grid, nearby_enemy)
                    self.move(world, move)
            else:
                self.random_move(world)
        if self.state == States.exploring:
            move = self.unfero_move(world)
            if move:
                if int(math.dist(move, self.cords)) <= 1:
                    self.move(world, move)
                else:
                    move = self.short_distance(world.grid, move)
                    self.move(world, move)
            else:
                self.random_move(world)
        if self.state == States.horny:
            if random.random() < self.genom[1]/30-0.1:
                self.sex(world)
                self.random_move(world)
            else:
                self.random_move(world)


    def run(self, world):
        self.decide_action(world)
        self.decide_state(world)
