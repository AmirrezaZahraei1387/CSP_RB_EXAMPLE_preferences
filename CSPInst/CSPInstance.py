class CSPInstance:
    """
    creating binary CSP instances by a given set of variables, domain and constraints.
    three different search algorithms are provided to search for one single solution of
    in the CSP model. These include Full-Look-ahead, backtracking and forward-checking.

    assignments are used in all the 3 algorithms. If you see a word assignment you can assume
    it is a dict object of the form {variable: value}.Similarly, the partial assignment put emphasis
    on the fact that the assignment is incomplete.

    A simple arc-consistency is implemented using revision method. You can run it after the
    creation of the model.
    """

    def __init__(self, varsD: dict, constraints: dict, dependencies: dict, cp_tables: dict):
        """
        :param varsD: is a dict object of the form {Var: ["domain of the variable", value1, value2, ...]}
        :param constraints: is a dict object of the form {(Var1, Var2): [(value1, value2), ... ]}
        :param dependencies: defines the dependencies of each variable.
        :param cp_tables: is a cpt instance and for each possible combination of parents values assignments
        defines a preference for the given variable.
        """
        self.__varsD = varsD
        self.__constraints = constraints
        self.__dependencies = dependencies
        self.__cp_tables = cp_tables

    def __getDomain(self, var: object):
        return self.__varsD[var]

    def __isConsistent(self, var: object, value: object, assignments: dict):
        """
        Checks if the assignment of the variable var with value does not violate any
        of the defined constraints or not. If yes return True otherwise it will return
        False.
        """
        assignments[var] = value

        for constraint in self.__constraints:
            if var in constraint:

                other_var = next(x for x in constraint if x != var)

                if other_var in assignments.keys():
                    assin = list(constraint)
                    assin[assin.index(var)] = value
                    assin[assin.index(other_var)] = assignments.get(other_var)

                    if tuple(assin) in self.__constraints[constraint]:
                        assignments.pop(var)
                        return False
        assignments.pop(var)
        return True

    def __getUnassignedVars(self, assignments: dict):
        """
        find the unassigned variables and then return the one with the least
        domain for efficiency.
        """
        unassigned_vars = [var for var in self.__varsD if var not in assignments]
        return min(unassigned_vars, key=lambda var: len(self.__getDomain(var)))

    def __ac3Revision(self, constraint: tuple):
        """
        get a binary constraint and remove the variables that
        violate from their domains. Mainly used for arc_consistency(ac3)
        """
        revised = False

        if constraint not in self.__constraints.keys():
            return False

        for var in constraint:
            other_var = next(x for x in constraint if x != var)
            for value1 in self.__varsD[var]:

                flag = True

                for value2 in self.__varsD[other_var]:
                    x = list(constraint)
                    x[x.index(var)] = value1
                    x[x.index(other_var)] = value2
                    if tuple(x) not in self.__constraints[constraint]:
                        flag = False
                        break
                if flag:
                    self.__varsD[var].remove(value1)
                    # if a revision in the domain is needed it is also needed in the cp-net instance
                    # in other words we need to reduce the preferences.
                    for assign_comb in self.__cp_tables[var]:
                        if value1 in self.__cp_tables[var][assign_comb]:
                            self.__cp_tables[var][assign_comb].remove(value1)   # remove the value from preferences
                    revised = True
        return revised

    def __arc_consistency(self):
        queue = list(self.__constraints.keys())

        while queue:
            constraint = queue.pop(0)
            if self.__ac3Revision(constraint):
                for u in self.__constraints:
                    if u not in queue and u[0] != constraint[1]:
                        queue.append(u)

    def __forward_checking(self, assignments: dict):
        queue = [(constraint[1], constraint[0])
                 for constraint in self.__constraints
                 if constraint[1] not in assignments.keys()]

        notConsistent = False

        while queue and not notConsistent:
            constraint = queue.pop(0)
            if self.__ac3Revision(constraint):
                notConsistent = self.__varsD[constraint[0]]
        return not notConsistent

    def __full_look_ahead(self, assignments: dict):
        queue = [(constraint[1], constraint[0])
                 for constraint in self.__constraints
                 if constraint[1] not in assignments.keys()]

        notConsistent = False

        while queue and not notConsistent:

            constraint = queue.pop(0)

            if self.__ac3Revision(constraint):
                for c in self.__constraints[constraint]:
                    if c[1] == constraint[0] and c[0] != constraint[1] and c not in queue:
                        queue.append(c)

                notConsistent = self.__varsD[constraint[0]]
        return not notConsistent

    def __backTrackWithFullLookAhead(self, results, assignments: dict):
        if len(assignments) == len(self.__varsD):
            return assignments

        var = self.__getUnassignedVars(assignments)

        for value in self.__getDomain(var):
            if self.__isConsistent(var, value, assignments):
                assignments[var] = value

                if self.__full_look_ahead(assignments):
                    result = self.__backTrackWithFullLookAhead(results, assignments)
                    if result is not None:
                        results.append(dict(result))

                del assignments[var]
        return None

    def __backTrackSearchWithForwardChecking(self, results, assignments: dict):

        if len(assignments) == len(self.__varsD):
            return assignments

        var = self.__getUnassignedVars(assignments)

        for value in self.__getDomain(var):
            if self.__isConsistent(var, value, assignments):
                assignments[var] = value

                if self.__forward_checking(assignments):
                    result = self.__backTrackSearchWithForwardChecking(results, assignments)
                    if result is not None:
                        results.append(dict(result))
                del assignments[var]
        return None

    def __backTrackSearch(self, results, assignments):
        """
        the internal method for backtracking.
        Simply traversing the tree completely to find the solution.
        """
        if len(assignments) == len(self.__varsD):
            return assignments

        var = self.__getUnassignedVars(assignments)

        for value in self.__getDomain(var):
            if self.__isConsistent(var, value, assignments):
                assignments[var] = value
                result = self.__backTrackSearch(results, assignments)
                if result is not None:
                    results.append(dict(result))
                del assignments[var]
        return None

    def __scoreSolution(self, result: dict):
        """
        gives a score to a solution(result) based on the directed graph
        cp-net. it helps to distinguish between the most preferable and least preferable
        assignment sequence.
        """
        score = 0

        for var in result:

            seq = []

            for v_parents in self.__dependencies[var]:
                seq.append(result[v_parents])
            seq = tuple(seq)

            pref = self.__cp_tables[var][seq]

            var_score = len(pref) - pref.index(result[var]) - 1
            score += var_score

        return score

    def __socreAll(self, results: list):

        scored_results = dict({})

        for result in results:
            SCORE = self.__scoreSolution(result)

            if SCORE not in scored_results:
                scored_results[SCORE] = []

            scored_results[SCORE].append(result)

        return scored_results

    def __selectKPareto(self, scored_results: dict, k):
        sorted_results_key = sorted(scored_results)

        count = 0
        answers = []

        for key in sorted_results_key:
            for result in scored_results[key]:
                answers.append(result)
                count += 1
                if count == k:
                    return answers

        return answers

# each algorithm will return a set of solutions that has been found
# then we revise them based on the cp-net to send the k most preferred solutions

    def forwardChecking(self, k: int):
        assignments = dict()
        results = []
        self.__backTrackSearchWithForwardChecking(results, assignments)
        return self.__selectKPareto(self.__socreAll(results), k)

    def backTrackSearch(self, k: int):
        assignments = dict()
        results = []
        self.__backTrackSearch(results, assignments)
        return self.__selectKPareto(self.__socreAll(results), k)

    def fullLookAhead(self, k: int):
        assignments = dict()
        results = []
        self.__backTrackWithFullLookAhead(results, assignments)
        return self.__selectKPareto(self.__socreAll(results), k)

    def arcConsistency(self):
        self.__arc_consistency()
