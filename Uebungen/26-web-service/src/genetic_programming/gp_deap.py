# code see https://github.com/DEAP/deap/blob/f4b77759897d0322ab5a6551106b28f6f4401a4e/examples/gp/symbreg.py
# for DEAP see https://deap.readthedocs.io/en/master/ 

#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

# Adapted by Thomas Bierweiler for Hochschule Karlsruhe, Data Engineering

import sys
import operator
import math
import random
import copy

import pandas as pd
import numpy

# toolbox for genetic algorithms
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# symbolic math toolbox
import sympy
from sympy.abc import x

# number of generations
ngen=50
# size of initial population
npop=5000

# read command line input
if len(sys.argv)>1:
    function_id=sys.argv[1]
else:
    function_id=3
print('Function id: {}'.format(function_id))
# read datapoints from file
fname=".\data\datapoints{}.pkl".format(function_id)
df=pd.read_pickle(fname)

def convert_inverse_prim(prim, args):
    """Convert inverse prims.

    Convert inverse prims according to:
    [Dd]iv(a,b) -> Mul[a, 1/b]
    [Ss]ub(a,b) -> Add[a, -b]
    We achieve this by overwriting the corresponding format method of
    the sub and div prim.

    Parameters
    ----------
    prim : deap.gp.Terminal
        A DEAP primitive

    Returns
    -------
    :class: String
        The converted string

    """
    prim = copy.copy(prim)

    converter = {
        'sub': "Add({}, Mul(-1.0,{}))".format,
        'protectedDiv': "(({})/({}))".format,
        'mul': "Mul({},{})".format,
        'add': "Add({},{})".format,
        'pow': "Pow({},{})".format,
    }
    prim_formatter = converter.get(prim.name, prim.format)

    return prim_formatter(*args)

def stringify_for_sympy(individual):
    """Return the expression in a human readable string.

    Parameters
    ----------
    individual : deap.gp.Individual
        A DEAP individual

    Returns
    -------
    :class: String
        The converted string

    """
    string = ""
    stack = []
    for node in individual:
        stack.append((node, []))
        while len(stack[-1][1]) == stack[-1][0].arity:
            prim, args = stack.pop()
            string = convert_inverse_prim(prim, args)
            if len(stack) == 0:
                break  # If stack is empty, all nodes should have been seen
            stack[-1][1].append(string)
    return string

# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
#pset.addPrimitive(protectedDiv, 2)
#pset.addPrimitive(operator.neg, 1)
#pset.addPrimitive(math.cos, 1)
#pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-4,4))
pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSymbReg(individual, points):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    sqerrors=0
    for index, row in df.iterrows():
        try:
            error=func(row['x'])-row['y']
            if math.isnan(error):
                error=1e6
        except:
            error=1e6
        sqerrors+=(error)**2
    return sqerrors / len(points),

toolbox.register("evaluate", evalSymbReg, points=df['x'])
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main():
    # initialize random seed for reproducibility
    random.seed(318)

    pop = toolbox.population(n=npop)
    hof = tools.HallOfFame(1)
    
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, ngen, stats=mstats,
                                   halloffame=hof, verbose=True)
    
    # print log
    print('Best results:')
    sympy_string=stringify_for_sympy(hof.items[0])
    print("Method generated by GP: {}".format(sympy_string))
    sympy_term=sympy.simplify(sympy_string)
    print("Simplified method: {}".format(sympy_term))
    # calculate root mean square error
    # sympy.subs calculates the numerical values for the symbolic expression sympy_term;
    # x is the variable in the symbolic expression
    # dfx is the iterator of the values stored in the dataframe
    estimated=df['x'].apply(lambda dfx: sympy_term.subs(x,dfx))
    estimated=estimated.astype('float')
    rmse=numpy.sqrt(numpy.sum(numpy.square(estimated.to_numpy()-df['y'].to_numpy()))/df.shape[0])
    print("RMSE: {}".format(rmse))
    # save to file
    with open('.\data\sympy_term{}.txt'.format(function_id),"w") as f:
        f.write('{}\n'.format(sympy_term))
        f.write('{}\n'.format(rmse))
    return pop, log, hof

if __name__ == "__main__":
    main()
