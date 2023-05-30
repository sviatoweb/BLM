import random

class Havka():
    def __init__(self) -> None:
        self.recharge = 40
        self.eaten = 0
    def got_eaten(self, day):
        self.eaten = day
    def is_ready(self, day):
        return (day - self.eaten) >= 10

class Cluster():
    def __init__(self,grid, cords, radius) -> None:
        self.cords = cords
        self.radius = radius
        self.cur = 0
        self.limit = int((2*radius+1)**2)
        self.spawn(grid)

    def spawn(self, grid):
        for loc_rad in range(1,self.radius+1):
            for i in range(self.cords[0]-loc_rad,self.cords[0]+loc_rad+1):
                for j in range(self.cords[1]-loc_rad,self.cords[1]+loc_rad+1):
                    try:
                        if random.random() < 1/loc_rad-0.03 and grid[i][j] == 0:
                            grid[i][j] = Havka()
                            self.cur += 1
                    except IndexError:
                        continue

class Havka_world():
    def __init__(self, size, num_clusters_p_q) -> None:
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.num_clusters = num_clusters_p_q
        self.generate_main()
        self.generate_quadr(2*self.size//25, self.size//2, 2*self.size//25, self.size//2)
        self.generate_quadr(2*self.size//25, self.size//2, self.size//2, self.size - 2*self.size//25 - 1)
        self.generate_quadr(self.size//2, self.size - 2*self.size//25 - 1, 2*self.size//25, self.size//2)
        self.generate_quadr(self.size//2, self.size - 2*self.size//25 - 1, self.size//2, self.size - 2*self.size//25 - 1)
        self.generate_singles()
        self.day = 11
    def generate_main(self):
        radius = self.size//25
        for tup in [(radius, radius),
                    (self.size-radius-1, radius),
                    (radius, self.size-radius-1),
                    (self.size-radius-1, self.size-radius-1)]:
            Cluster(self.grid, tup, radius)
        Cluster(self.grid,(self.size//2, self.size//2), self.size//20)
    def generate_quadr(self, x_min, x_max, y_min, y_max):
        for _ in range(self.num_clusters):
            y = random.randint(y_min, y_max)
            x = random.randint(x_min, x_max)
            Cluster(self.grid,(y, x), random.randint(self.size//70,self.size//35))
    def generate_singles(self):
        for _ in range((self.size**2)//100):
            x = random.randint(0,self.size - 1)
            y = random.randint(0,self.size - 1)
            if self.grid[y][x] == 0:
                self.grid[y][x] = Havka()