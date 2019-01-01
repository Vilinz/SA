from random import randint
import math
import random
import matplotlib.pyplot as plt


class SA:
    def __init__(self):
        self.city = {}
        self.current_path = []
        self.new_path = []
        self.ax = 0
        self.T = 40
        self.point = 0

    def read_file(self):
        f = open('kroB101')
        count = 0
        for line in f.readlines():
            if count == 0:
                count += 1
                self.point = int(line.strip())
                continue
            if line.strip() != 'EOF':
                print(line.strip())
                str = line.strip().split(' ')
                index = int(str[0])
                x = int(str[1])
                y = int(str[2])
                point = [x, y]
                self.city[index] = point
        f.close()
        print("Read file end", len(self.city))

    def init_point(self):
        plt.ion()
        fig = plt.figure()
        self.ax = fig.add_subplot(111)
        self.ax.set_title("TSP")

        for i in range(1, self.point + 1):
            self.current_path.append(i)
            self.new_path.append(i)

        for c in self.city:
            plt.scatter(self.city[c][0], self.city[c][1], color='r', linewidths=2, marker=".")

    def update(self):
        x = []
        y = []
        self.ax.lines = []
        self.ax.set_title("TSP  " + "cost: " + str(self.current_cost) + "   T: " + str(self.T))

        for i in self.current_path:
            x.append(self.city[i][0])
            y.append(self.city[i][1])

        for i in range(0, self.point - 1):
            plt.plot((x[i], x[i+1]), (y[i], y[i+1]), color='b')

        plt.plot((x[self.point - 1], x[0]), (y[self.point - 1], y[0]), color='b')

        plt.draw()
        plt.pause(0.0001)
        plt.show()

    def gen_new_path(self, way):
        a1 = randint(0, self.point - 1)
        a2 = randint(0, self.point - 1)
        while a1 == a2:
            a1 = randint(0, self.point - 1)
            a2 = randint(0, self.point - 1)

        self.new_path = self.current_path.copy()
        if a1 > a2:
            temp = a1
            a1 = a2
            a2 = temp

        if way == 'i':
            temp = self.new_path[a2]
            i = a2
            while i > a1:
                self.new_path[i] = self.new_path[i-1]
                i -= 1
            self.new_path[a1] = temp
        elif way == 's':
            temp = self.new_path[a1]
            self.new_path[a1] = self.new_path[a2]
            self.new_path[a2] = temp
        elif way == 'r':
            i = a1
            while i <= a2:
                self.new_path[a2 - (i - a1)] = self.current_path[i]
                i += 1
        else:
            pass

    def path_cost(self, path):
        cost = 0
        for i in range(1, self.point):
            sub_x = self.city[path[i]][0] - self.city[path[i-1]][0]
            sub_y = self.city[path[i]][1] - self.city[path[i-1]][1]
            dis = pow((sub_x*sub_x + sub_y*sub_y), 0.5)
            cost += dis

        sub_x = self.city[path[0]][0] - self.city[path[self.point - 1]][0]
        sub_y = self.city[path[0]][1] - self.city[path[self.point - 1]][1]
        dis = pow((sub_x*sub_x + sub_y*sub_y), 0.5)
        cost += dis
        return cost

    def solution_hill_climbing(self, way):
        repeat = 100000
        print("in")
        while repeat > 0:
            repeat -= 1
            self.gen_new_path(way)
            current_cost = self.path_cost(self.current_path)
            new_cost = self.path_cost(self.new_path)

            if current_cost > new_cost:
                self.current_path = self.new_path.copy()
                self.update()
            current_cost = self.path_cost(self.current_path)
            print("current ", current_cost)
        print("Run end")
        plt.ioff()
        plt.show()

    def solution_annealing(self, way):
        repeat = 500
        while self.T > 0.1:
            i = 0
            c = 0
            while i < repeat:
                i += 1
                c += 1
                self.gen_new_path(way)
                self.current_cost = self.path_cost(self.current_path)
                self.new_cost = self.path_cost(self.new_path)
                if self.new_cost < self.current_cost:
                    self.current_path = self.new_path.copy()
                    if c == 20:
                        c = 0
                        self.update()
                    print("cost update: ", self.current_cost)
                else:
                    num = math.exp((self.current_cost - self.new_cost)/self.T)
                    ran = random.random()
                    if num >= ran:
                        self.current_path = self.new_path.copy()
                        if c == 20:
                            c = 0
                            self.update()
                        print("cost update: ", self.current_cost)
            self.T *= 0.99
        print("Run end")
        plt.ioff()
        plt.show()


def main():
    sa = SA()
    sa.read_file()
    sa.init_point()

    command = input("Print select run mode:\n$ ")
    print("hill climbing ------------ h")
    print("simulated annealing------- a")
    print("we have three ways to generate new neighbor,please choose one way to run\ninsert---------- i\nswap------------ s\nreversal-------- r\n$ ")
    way = input()
    if command == 'h':
        sa.solution_hill_climbing('i')
    elif command == 'a':
        sa.solution_annealing(way)
    else:
        print("command error")


if __name__ == '__main__':
    main()





