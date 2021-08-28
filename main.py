import csv
from abc import ABC, abstractmethod


class Cursor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.current_line = None
        self.current_result = None
        self.index = 0
        input_file = open(file_name, "r")
        self.reader = csv.reader(input_file)
        # skip header
        next(self.reader)

    def read_next(self):
        # first execution -> reading the file
        if self.current_result is None:
            try:
                self.current_line = next(self.reader)
                self.index += 1
            except StopIteration:
                self.current_line = None
            return self.current_line
        else:
            if self.index < len(self.current_result):
                res = self.current_result[self.index]
                self.index += 1
                return res
            else:
                return None

    def set_results(self, res):
        # setting a single value
        if isinstance(res, int):
            self.current_result = [res, []]

        # one row
        elif res == [] or isinstance(res[0], int):
            self.current_result = [res, []]

        # two dimensional array
        else:
            self.current_result = res

        self.index = 0

    def print_results(self):
        # single value
        if isinstance(self.current_result[0], int):
            print(self.current_result[0])
        else:
            for line in self.current_result:
                print(*line, sep=", ")


class CsvSomething:

    def __init__(self, file_name):
        self.actions = []
        self.cursor = Cursor(file_name)
        
    def add_action(self, action):
        self.actions.append(action)
        return self

    def run(self):

        for action in self.actions:
            res = action.execute(self.cursor.read_next)
            self.cursor.set_results(res)

        self.cursor.print_results()


class Action(ABC):

    def __init__(self):
        super(Action, self).__init__()

    @abstractmethod
    def execute(self, read_val):
        """
        This abstract method should return an array, two dimensional array or an integer
        :rtype: an array, two dimensional array or an integer
        """
        pass


class Sum(Action):
    def execute(self, read_val):
        res = 0
        val = read_val()
        while val:
            # we got an array
            if isinstance(val, list):
                for i in val:
                    res += int(i)
            # single value
            else:
                res += int(val)
            val = read_val()
        return res


class GetColumn(Action):
    def __init__(self, index):
        super(GetColumn, self).__init__()
        self.index = index

    def execute(self, read_val):
        res = []
        val = read_val()
        while val:
            res.append(val[self.index])
            val = read_val()
        return res


class FilterRows(Action):
    def __init__(self, column, value):
        super(FilterRows, self).__init__()
        self.value = value
        self.column = column

    def execute(self, read_val):
        res = []
        val = read_val()

        while val:
            if int(val[self.column]) == self.value:
                res.append(val)
            val = read_val()
        return res


CsvSomething("Book1.csv").add_action(FilterRows(1, 2)).run()
