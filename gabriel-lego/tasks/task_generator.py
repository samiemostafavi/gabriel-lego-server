import Queue
import random

import numpy as np


class BrickCollection(object):
    def __init__(self, collection_dict=dict()):
        super(BrickCollection, self).__init__()
        self.colors = range(7)

        self.collection = []
        for brick, count in collection_dict.iteritems():
            self.collection += ([brick] * count)

    def _put_brick(self, length, color):
        self.collection.append((length, color))

    def put_brick(self, brick):
        self._put_brick(len(brick), brick[0])

    def get_brick(self, length, color):
        assert color in self.colors

        to_remove = -1
        for i, (i_len, i_color) in enumerate(self.collection):
            if i_len == length and i_color == i_color:
                to_remove = i
                break

        if to_remove < 0:
            return None

        self.collection.pop(to_remove)
        return [color] * length

    def get_random_brick(self):
        brick_i = random.randint(0, len(self.collection) - 1)
        length, color = self.collection.pop(brick_i)

        return [color] * length


class TaskGenerator(object):
    def __init__(self, collection):
        super(TaskGenerator, self).__init__()
        self.collection = collection

    @staticmethod
    def check_anchor(anchor, brick, table):
        height, width = table.shape
        # first check: does brick fit in table?
        if anchor + len(brick) - 1 >= width:
            return False

        ret = False
        for i in range(anchor, anchor + len(brick)):
            # second check, does it clash with any other brick
            if table[0][i] != 0:
                return False

            # third check: are there any support points
            if 1 == height:
                ret = True
            elif table[1][i] != 0:
                ret = True

        return ret

    @staticmethod
    def add_brick(table, brick):
        n_table = np.copy(table)
        width = table.shape[1]

        anchor = random.choice([i for i in range(width)
                                if
                                TaskGenerator.check_anchor(i, brick, n_table)])

        for i in range(anchor, anchor + len(brick)):
            n_table[0][i] = brick[i - anchor]

        return n_table

    def generate(self, num_steps, height=8):
        assert num_steps >= 1

        base = self.collection.get_brick(length=6, color=6)

        steps = []
        base_table = np.full((1, len(base)), fill_value=base[0], dtype=int)
        steps.append(base_table)
        table = np.vstack((np.zeros((1, len(base)), dtype=int), base_table))

        current_level = 1
        adding = True
        temp_stack = Queue.LifoQueue()
        while len(steps) < num_steps:
            if adding:
                brick = self.collection.get_random_brick()
                try:
                    table = self.add_brick(table, brick)
                    n_table = np.copy(table)
                    steps.append(n_table)
                    temp_stack.put_nowait((n_table, brick))
                except IndexError:
                    # level is full
                    current_level += 1
                    if current_level == height:
                        adding = False
                        temp_stack.get_nowait()  # pop the latest step
                    else:
                        table = np.vstack((np.zeros((1, len(base)),
                                                    dtype=int), table))
            else:
                try:
                    step, brick = temp_stack.get_nowait()
                    steps.append(step)
                    self.collection.put_brick(brick)
                except Queue.Empty:
                    steps.append(base_table)
                    table = np.vstack(
                        (np.zeros((1, len(base)), dtype=int), base_table))
                    current_level = 1
                    adding = True

        return steps


Life_of_George_Bricks = BrickCollection(
    collection_dict={
        # black bricks
        (1, 6): 8,
        (2, 6): 6,
        (6, 6): 2,
        (4, 6): 4,
        (3, 6): 4,
        # blue bricks
        (1, 5): 8,
        (2, 5): 6,
        (6, 5): 2,
        (4, 5): 4,
        (3, 5): 4,
        # red bricks
        (1, 4): 8,
        (2, 4): 6,
        (6, 4): 2,
        (4, 4): 4,
        (3, 4): 4,
        # yellow bricks
        (1, 3): 8,
        (2, 3): 6,
        (6, 3): 2,
        (4, 3): 4,
        (3, 3): 4,
        # green bricks
        (1, 2): 8,
        (2, 2): 6,
        (6, 2): 2,
        (4, 2): 4,
        (3, 2): 4,
        # white bricks
        (1, 6): 8,
        (2, 6): 6,
        (6, 6): 2,
        (4, 6): 4,
        (3, 6): 4,
    }
)

DefaultGenerator = TaskGenerator(Life_of_George_Bricks)

if __name__ == '__main__':
    for i, t in enumerate(DefaultGenerator.generate(200)):
        print(' ')
        print(i)
        print(t)
