import CSPInst
import time


def runAlgorithm(func, k: int):
    start = time.time()
    results = func(k)
    end = time.time()
    print("***answers are in the order of most preferred to least preferred***")
    for result in results:
        print("answer: ", result)
    print("time took: {}".format(end - start))


def main():

    varCount = int(input("enter the number of variables: "))
    tightness = float(input("enter the tightness: "))
    alpha = float(input("enter the constant alpha: "))
    rCon = float(input("enter the constant r: "))
    np = int(int(input("enter the max dependencies: ")))
    k_pareto = int(int(input("number of k pareto solutions: ")))

    searchingStrategy = input("enter the searching strategy (BT, FC, FLA): ")
    runArcConsistency: bool = input("do you want to run arc consistency(yes/no): ").lower() == "yes"

    # initialing the RB model
    RB_generator = CSPInst.RBModel(
        varCount=varCount,
        tightness=tightness,
        alpha=alpha,
        rCon=rCon,
        np=np
    )

    RB_generator.printModelState()

    variables, domain, constraints, dependencies, cp_table = RB_generator.getModelDetails()

    # constructing a CSP instance
    CSP_instance = CSPInst.CSPInstance(
        {var: list(domain) for var in variables},
        constraints,
        dependencies,
        cp_table
    )

    if runArcConsistency:
        print("running arc consistency ...")
        CSP_instance.arcConsistency()

    if searchingStrategy == "BT":
        runAlgorithm(CSP_instance.backTrackSearch, k_pareto)
    elif searchingStrategy == "FC":
        runAlgorithm(CSP_instance.forwardChecking, k_pareto)
    elif searchingStrategy == "FLA":
        runAlgorithm(CSP_instance.fullLookAhead, k_pareto)
    else:
        print("invalid searching algorithm.")


if __name__ == "__main__":
    main()

