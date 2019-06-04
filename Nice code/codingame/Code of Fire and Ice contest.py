# Declaring helping names:
import sys
import math
import time
# MAP 
HEIGHT = 12
WIDTH = 12

# Ownership
ME = 0
ENEMY = 1
NOBODY = 2
VOID = 3

# Buildings
HQ = 0
MINE = 1
TOWER = 2


class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
class Neighbour(Position):
    def __init__(self, row, col, of):
        Position.__init__(self, row, col)
        self.of = of
        self.neighbours = []
        if row!=0 and of.row != row-1 and of.col != col:
            self.neighbours.append(Position(row-1, col))
        if row!=HEIGHT-1 and of.row != row+1 and of.col != col:
            self.neighbours.append(Position(row+1, col))
        if col!=0 and of.row != row and of.col != col-1:
            self.neighbours.append(Position(row, col-1))
        if col!=WIDTH-1 and of.row != row and of.col != col+1:
            self.neighbours.append(Position(row, col+1))
class Square(Position):
    def __init__(self, row, col):
        Position.__init__(self, row, col)
        self.neighbours = []
        if row!=0:
            self.neighbours.append(Neighbour(row-1, col,Position(row,col)))
        if row!=HEIGHT-1:
            self.neighbours.append(Neighbour(row+1, col,Position(row,col)))
        if col!=0:
            self.neighbours.append(Neighbour(row, col-1, Position(row,col)))
        if col!=WIDTH-1:
            self.neighbours.append(Neighbour(row, col+1, Position(row,col)))
class Tile(Square):
    def __init__(self, row, col, owner = None, occupied = None, worth = 0, train_worth = 0, danger = 0):
        Square.__init__(self, row, col)
        self.owner = owner
        self.occupied = occupied
        self.worth = worth
        self.train_worth = train_worth
        self.danger = danger
        
        
    def normalize_worth(self):
        if self.owner == VOID:
            self.worth = -100000
        elif self.owner == NOBODY:
            self.worth = 50
        elif self.owner == ME:
            self.worth = 10
        elif self.owner == ENEMY:
            self.worth = 100
        else:
            print("Error worth in tile", file = sys.stderr)
    def normalize_train_worth(self):
        if self.owner == VOID or self.owner == ME:
            self.train_worth = -1000000
        elif self.owner == ENEMY or self.owner == NOBODY:
            self.train_worth = 0
        else:
            print("Error Train_worth in tile", file = sys.stderr)
        pass
    
class djikstraTile(Square):
    def __init__(self, row, col, cost, owner):
        Square.__init__(self, row, col)   
        self.cost = cost
        self.shortest_cost = 900 #it's like infinity xd
        self.previous_tile = None
        self.owner = owner
class Unit(Square):
    def __init__(self, row, col, id, level, owner):
        Square.__init__(self, row, col)
        self.id = id
        self.level = level
        self.owner = owner
class Building(Square):
    def __init__(self, row, col, type, owner):
        Square.__init__(self, row, col)
        self.type = type
        self.owner = owner

class Game:
    def __init__(self):
        self.units = []
        self.buildings = []
        self.tiles = []
        for row in range(HEIGHT):
            self.tiles.append([])
        self.actions = []
        self.minespots = []
        self.d_tiles = []
        self.turns = 0
        self.gold = 0
        self.income = 0
        self.enemyGold = 0
        self.enemyIncome = 0
        self.highestUnitID = 0
        self.start_time = time.time()
    def getEnemyHQ(self):
        for b in self.buildings:
            if b.type == HQ and b.owner == ENEMY:
                return b
       
    def normalize_worth_tiles(self):
        tmp_tiles = []
        for row in range(HEIGHT):
            for col in range(WIDTH):
                tmp_tiles.append(self.tiles[row][col])
        for tile in tmp_tiles:
            tile.normalize_worth()
            
    def normalize_train_worth_tiles(self):
        tmp_tiles = []
        for row in range(HEIGHT):
            for col in range(WIDTH):
                tmp_tiles.append(self.tiles[row][col])
        for tile in tmp_tiles:
            tile.normalize_train_worth()
            
    def init_input(self):
        numberMineSpots = int(input())
        for amount  in range(numberMineSpots):
            col,row = [int(j) for j in input().split()]
            self.minespots.append(Position(row, col))
            
    def first_turn_update(self):
        self.gold = int(input())
        self.income = int(input())
        self.enemyGold = int(input())
        self.enemyIncome = int(input())
        for row in range(HEIGHT):
            line = input()
            for col in range(WIDTH):
                letter = line[col]
                if letter == "#":
                    self.tiles[row].append(Tile(row, col, VOID))
                elif letter == "O":
                    self.tiles[row].append(Tile(row, col, ME))
                elif (letter == "X" or letter == "x"):
                    self.tiles[row].append(Tile(row, col, ENEMY))
                elif (letter == "." or letter == "o"):
                    self.tiles[row].append(Tile(row, col, NOBODY))
                else:
                    print("Unidentified Input in line/row first input", file = sys.stderr)
        self.normalize_worth_tiles()
        self.normalize_train_worth_tiles()
        buildingCount = int(input())
        for i in range(buildingCount):
            owner, buildingType, col, row =[int(j) for j in input().split()]
            self.buildings.append(Building(row, col, buildingType, owner))
        unitCount = int(input())
        self.highestUnitID = 0
        for i in range(unitCount):
            owner, unitId, level, col, row = [int(j) for j in input().split()]
            self.units.append(Unit(row, col, unitId, level, owner))
            if unitId > self.highestUnitID:
                self.highestUnitID = unitId
            
    def update(self):
        self.units.clear()
        self.buildings.clear()
        self.actions.clear()
        
        self.gold = int(input())
        self.income = int(input())
        self.enemyGold = int(input())
        self.enemyIncome = int(input())
        for row in range(HEIGHT):
            line = input()
            for col in range(WIDTH):
                self.tiles[row][col].occupied = None
                letter = line[col]
                if letter == "#":
                    self.tiles[row][col].owner = VOID
                elif letter == "O":
                    self.tiles[row][col].owner = ME
                elif (letter == "X" or letter == "x"):
                    self.tiles[row][col].owner = ENEMY
                elif (letter == "." or letter == "o"):
                    self.tiles[row][col].owner = NOBODY
                else:
                    print("Unidentified Input in line/row first input", file = sys.stderr)
            
        self.normalize_worth_tiles()
        self.normalize_train_worth_tiles()
        buildingCount = int(input())
        for i in range(buildingCount):
            owner, buildingType, col, row = [int(j) for j in input().split()]
            self.buildings.append(Building(row, col, buildingType, owner))
            self.tiles[row][col].occupied = self.buildings[-1]
        self.highestUnitID = 0
        unitCount = int(input())
        for i in range(unitCount):
            owner, unitId, level, col, row = [int(j) for j in input().split()]
            self.units.append(Unit(row, col, unitId, level, owner))
            self.tiles[row][col].occupied = self.units[-1]
            if unitId > self.highestUnitID:
                self.highestUnitID = unitId
                
    def can_spawn(self, level, tile):
        print("Can spawn executed", tile.row, tile.col, file=sys.stderr)
        if tile.owner == NOBODY:
            return True
        elif tile.owner == ENEMY:
            if level == 3:
                return True
            else:
                for unit in self.units:
                    if unit.row == tile.row and unit.col == tile.col:
                        if level > unit.level:
                            return True
                        else:
                            return False
                for building in self.buildings:
                    if building.type == TOWER and (abs(building.row-tile.row) + abs(building.col-tile.col) <=1):
                        return False
                return True               
        else:
            print("CAN SPAWN GOT WEIRD INPUT", tile.owner,tile.row, " ", tile.col, file=sys.stderr)        
    def djikstra(self):
        self.d_tiles.clear()
        for row in range(HEIGHT):
            self.d_tiles.append([])
            for col in range(WIDTH):
                cost = 10
                for unit in self.units:
                    if unit.row == row and unit.col == col and self.tiles[row][col] == ENEMY:
                        if unit.level == 1:
                            cost = 20
                        if unit.level in [2,3] and self.tiles[row][col] == ENEMY:
                            cost = 30
                for building in self.buildings:
                    if building.type == TOWER and building.owner == ENEMY and self.tiles[row][col] == ENEMY:
                        if abs(building.row - row) + abs(building.col - col) <=1:
                            cost = 30
                owner = self.tiles[row][col].owner
                
                self.d_tiles[row].append(djikstraTile(row, col, cost, owner))
        # Creating list with d_tiles :)
        visited = []
        unvisited = []
        E_HQ = self.getEnemyHQ()
        self.d_tiles[E_HQ.row][E_HQ.col].shortest_cost = 10
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.d_tiles[row][col].owner!=VOID:
                    unvisited.append(self.d_tiles[row][col])
        
        unvisited.sort(key = lambda x: self.d_tiles[x.row][x.col].shortest_cost)
        while(unvisited[0].owner!=ME):
            t = unvisited[0]
            for neighbour in t.neighbours:
                if not neighbour in visited and not self.d_tiles[neighbour.row][neighbour.col].owner == VOID:
                    nghbour = self.d_tiles[neighbour.row][neighbour.col]
                    new_cost = nghbour.cost + t.shortest_cost
                    if new_cost < nghbour.shortest_cost:
                        nghbour.shortest_cost = new_cost
                        nghbour.previous_tile = Position(t.row, t.col)
            visited.append(t)
            unvisited.remove(t)
            unvisited.sort(key = lambda x: self.d_tiles[x.row][x.col].shortest_cost)
        cost_needed = unvisited[0].shortest_cost
        if self.gold >= cost_needed:
            
            obj = unvisited[0].previous_tile

            b = self.getEnemyHQ()
            while (obj.row!= b.row and obj.col != b.col):
                #get obj
                for level in range(1,4):
                    if self.can_spawn(level, self.tiles[obj.row][obj.col]):
                        self.actions.append(f'TRAIN {level} {obj.col} {obj.row}')
                #find next target
                obj = self.d_tiles[obj.row][obj.col].previous_tile
            self.actions.append(f'TRAIN 1 {b.col} {b.row}')
            self.actions.append("MSG DJIKSTRA LOLOL")
            
                
                
                
        
    
    def can_move(self, unit, tile):
        if tile.owner == VOID:
            return False
        if tile.owner == ME and tile.occupied:
            return False
        if unit.level == 3:
            return True
        if tile.owner == NOBODY:
            return True
        if tile.owner == ENEMY:
            for building in self.buildings:
                if (building.type == TOWER and (abs(building.row - tile.row) + abs(building.col - tile.col) <=1)):
                    return False
            if tile.occupied:
                for Eunit in self.units:
                    if (Eunit.row == tile.row and Eunit.col == tile.col):
                        if Eunit.level >= unit.level:
                            return False
                return True
            else:
                return True
                
    def move(self, unit):
        possibilities =[]
        for neighbour  in unit.neighbours:
            self.tiles[neighbour.row][neighbour.col].normalize_worth()
            if self.can_move(unit,self.tiles[neighbour.row][neighbour.col]):
                for neighbour2 in neighbour.neighbours:
                    if not self.tiles[neighbour2.row][neighbour2.col].owner == VOID:
                        self.tiles[neighbour.row][neighbour.col].worth+= self.tiles[neighbour2.row][neighbour2.col].worth//3
                possibilities.append(self.tiles[neighbour.row][neighbour.col])
        if len(possibilities) != 0:
            possibilities.sort(key = lambda x : x.worth, reverse = True)
            return possibilities[0]
        return "NO POSSIBILITIES"
    def move_units(self):
        for unit in self.units:
            if unit.owner == ME:
                objective = self.move(unit)
                if objective == "NO POSSIBILITIES":
                    enemy_hq = self.getEnemyHQ()

                    self.actions.append(f'MOVE {unit.id} {enemy_hq.col} {enemy_hq.row}')
                    continue
                else:
                    self.tiles[objective.row][objective.col].occupied = self.tiles[unit.row][unit.col].occupied
                    if self.tiles[objective.row][objective.col].occupied:
                        print(objective.col, objective.row, "IS OCCUPIED BITCH", file=sys.stderr)
                    self.tiles[unit.row][unit.col].occupied = None
                    self.tiles[objective.row][objective.col].owner = ME
                    unit.row = objective.row
                    unit.col = objective.col
                    self.actions.append(f'MOVE {unit.id} {objective.col} {objective.row}')
    
    def calculate_best_train_option(self):
        self.normalize_train_worth_tiles()
        #find options
        possibilities = []
        tmp_tiles = []
        for row in range(HEIGHT):
            for col in range(WIDTH):
                tmp_tiles.append(self.tiles[row][col])
        i = 0
        for tile in tmp_tiles:
            #print("checking", i,"tile", tile.row, tile.col,tile.owner, file=sys.stderr)
            if tile.row == 0 and tile.col == 5:
                print("5,0 tile :)",tile.owner, file=sys.stderr)
            if tile.owner == NOBODY or tile.owner == ENEMY:
                connected = False
                for neighbour in tile.neighbours:
                    if self.tiles[neighbour.row][neighbour.col].owner == ME:
                        connected = True
                if connected:
                    possibilities.append(self.tiles[tile.row][tile.col])
            i+=1
            
        print(len(possibilities), "DLUGOSC POSSIBILITIES", file=sys.stderr)
        for possibility in possibilities:
            print("one of possibilities",possibility.col, possibility.row, file = sys.stderr)
        for place in possibilities:
            if place.owner == NOBODY:
                place.train_worth +=40
                for neighbour in place.neighbours:
                    if self.tiles[neighbour.row][neighbour.col].owner == NOBODY:
                        place.train_worth+=30
                    elif self.tiles[neighbour.row][neighbour.col].owner == ENEMY:
                        place.train_worth+=40
                    elif self.tiles[neighbour.row][neighbour.col].owner == ME:
                        place.train_worth+=10
                        for unit in self.units:
                            if unit.row == neighbour.row and unit.col == neighbour.col:
                                place.train_worth -= 25
            elif place.owner == ENEMY:
                occupied = False
                place.train_worth+=100
                for building in self.buildings:
                    if building.type == TOWER and building.row == place.row and building.col == place.col:
                        place.train_worth-=150
                        occupied = True
                for unit in self.units:
                    if unit.row == place.row and unit.col == place.col:
                        if unit.level == 1:
                            place.train_worth-=75
                            occupied = True
                        if unit.level == 2 or unit.level == 3:
                            place.train_worth -=150
                            occupied = True
                for neighbour in place.neighbours:
                    if self.tiles[neighbour.row][neighbour.col].owner == NOBODY:
                        place.train_worth+=20
                    elif self.tiles[neighbour.row][neighbour.col].owner == ENEMY:
                        for building in self.buildings:
                            if (building.type == TOWER and building.row == neighbour.row and neighbour.col == building.col and building.owner == ENEMY):
                                place.train_worth-=150
                        if not occupied:
                            place.train_worth+50
                        place.train_worth+=20
                    elif self.tiles[neighbour.row][neighbour.col].owner == ME:
                        place.train_worth+=15
        if len(possibilities) == 0:
            return "NO POSSIBILITIES"
        else:
            possibilities.sort(key = lambda x : x.train_worth, reverse = True)
            print("train possibility", possibilities[0].col, possibilities[0].row, file = sys.stderr)
            print([i.worth for i in possibilities], file=sys.stderr)
            return possibilities[0]

    def train_units(self):
        still_train = True
        while(still_train):
            objective = self.calculate_best_train_option()
            if objective == "NO POSSIBILITIES":
                print("there was no possibilities", file=sys.stderr)
                still_train = False
                break
            else:
                print(objective.row, objective.col, "Error A1", file = sys.stderr)
                for level in range(1,4):
                    if self.can_spawn(level, objective):
                        if level == 1:
                            if self.gold >=10:
                                self.gold -=10
                                self.tiles[objective.row][objective.col].owner = ME
                                self.actions.append(f'TRAIN {level} {objective.col} {objective.row}')
                                self.units.append(Unit(objective.row, objective.col, self.highestUnitID+1,level, ME))
                                break
                            else:
                                still_train = False
                                break
                        elif level == 2:
                            if self.gold >=20 and self.income >5:
                                self.gold -=20
                                self.income -= 5
                                self.tiles[objective.row][objective.col].owner = ME
                                self.actions.append(f'TRAIN {level} {objective.col} {objective.row}')
                                self.units.append(Unit(objective.row, objective.col, self.highestUnitID+1,level, ME))
                                break
                            else:
                                still_train = False
                                break
                        elif level == 3:
                            if self.gold>=30 and self.income >25:
                                self.gold -= 30
                                self.income -= 20
                                self.tiles[objective.row][objective.col].owner = ME
                                self.actions.append(f'TRAIN {level} {objective.col} {objective.row}')
                                self.units.append(Unit(objective.row, objective.col, self.highestUnitID+1,level, ME))
                                break
                            
                            else:
                                still_train = False
                                break
    def build_output(self):
        
        self.move_units()
        #self.djikstra()
        self.train_units()
    def output(self):
        if self.actions:
            #self.actions.append("MSG --- %s seconds ---" % (round(time.time() - self.start_time, 2)))
            print(';'.join(self.actions))
        else:
            print('WAIT') 
            
g = Game()
g.init_input()
g.first_turn_update()
g.build_output()
g.output()

while True:

    g.start_time = time.time()
    g.update()
    g.build_output()
    g.output()


        
