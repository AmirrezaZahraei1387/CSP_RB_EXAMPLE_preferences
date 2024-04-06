import math
import random
import itertools


class RBModel:
    """
    the RB model is used to generate CSP instances under
    the control of difficulty to solve the CSP model.
    """

    def __init__(self, varCount: int, tightness: float, alpha: float, rCon: float, np: int):

        self.__varCount = varCount
        self.__tightness = tightness
        self.__alpha = alpha
        self.__rCon = rCon
        self.__np = np

        self.__domainSize = round(self.__varCount ** alpha)
        self.__constraintCount = round(self.__rCon * self.__varCount * math.log(self.__varCount))
        self.__incTupleCount = round(self.__tightness * (self.__domainSize ** 2))

        self.__variables = [f'X{i}' for i in range(self.__varCount)]
        self.__domain = list(range(self.__domainSize))
        self.__constraints: dict = self.__generateConstraints()
        self.__dependencies = self.__generateDependencies()
        self.__cp_tables = self.__generateCPT()

    def __generateConstraints(self):
        """
        generate constraints based on RB model according to the paper
        """
        constraints = {}
        p_d_squared = int(round(self.__tightness * self.__domainSize ** 2))

        for _ in range(self.__constraintCount):

            flag = False

            while True:
                variables = random.sample(self.__variables, 2)

                for v in constraints:
                    if ((variables[0] == v[0] and variables[1] == v[1]) or (variables[0] == v[1] and
                                                                            variables[1] == v[0])):
                        flag = True
                        break
                if flag:
                    flag = False
                    continue
                break

            incompatible_tuples = []
            for _ in range(p_d_squared):
                t = tuple(random.choices(self.__domain, k=2))

                while t in incompatible_tuples:
                    t = tuple(random.choices(self.__domain, k=2))
                incompatible_tuples.append(t)

            constraints.update({tuple(variables): incompatible_tuples})
        return constraints

    def __generateDependencies(self):

        dependencies = dict({})

        for v in self.__variables:
            v_dependencies = list(random.sample(self.__variables, k=random.randint(0, self.__np)))
            try:
                v_dependencies.remove(v)
            except ValueError:
                pass
            dependencies.update({v: v_dependencies})

        return dependencies

    def __generateCPT(self):

        cp_tables = dict({})

        for variable in self.__dependencies:
            depend_num = len(self.__dependencies[variable])
            comb = list(itertools.product(self.__domain, repeat=depend_num))
            cp_tables.update({variable: {}})
            for val in comb:
                cp_tables[variable].update({val: random.sample(self.__domain, len(self.__domain))})

        return cp_tables

    def getModelDetails(self):
        return self.__variables, self.__domain, self.__constraints, self.__dependencies, self.__cp_tables

    def getModelState(self):
        return self.__domainSize, self.__constraintCount, self.__incTupleCount

    def printModelState(self):

        print("variables: ", self.__variables)
        print("domain: ", self.__domain)

        print("constraints: ")
        for variables in self.__constraints:
            print(variables, ":", self.__constraints[variables])

        print("dependencies: ")
        for variable in self.__dependencies:
            print(variable, ":", self.__dependencies[variable])

        print("cp_tables: ")
        for variable in self.__cp_tables:
            print(variable, ":")

            for val, pref in self.__cp_tables[variable].items():
                print(val, ": ", end="")

                for i in range(len(pref) - 1, -1, -1):
                    if i == 0:
                        print(pref[i])
                    else:
                        print(pref[i], "> ", end="")

