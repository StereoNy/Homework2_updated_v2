from runGame import *
from agent import *
from game import ChineseChecker

from math import sin, cos, pi
from gaft import GAEngine
from gaft.components import BinaryIndividual
from gaft.components import Population
from gaft.operators import TournamentSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitBigMutation

# Built-in best fitness analysis.
from gaft.analysis.fitness_store import FitnessStore
from gaft.analysis.console_output import ConsoleOutput

indv_template = BinaryIndividual(ranges=[(0, 0.6),(0,0.01)], eps=0.001)
population = Population(indv_template=indv_template, size=30).init()

# Create genetic operators.
#selection = RouletteWheelSelection()
selection = TournamentSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitBigMutation(pm=0.1, pbm=0.55, alpha=0.6)

# Create genetic algorithm engine.
# Here we pass all built-in analysis to engine constructor.
engine = GAEngine(population=population, selection=selection,
                  crossover=crossover, mutation=mutation,
                  analysis=[ConsoleOutput, FitnessStore])

# Define fitness function.
@engine.fitness_register
def fitness(indv):
    y,z= indv.solution
    print(y,z)
    ccgame = ChineseChecker(10, 4)
    simpleGreedyAgent = SimpleGreedyAgent(ccgame)
    randomAgent = RandomAgent(ccgame)
    teamAgent = TeamNameMinimaxAgent(ccgame)
    teamAgent.HeruDefine(y,z)
    agents_dict_1 = {1: teamAgent, 2: simpleGreedyAgent}
    agents_dict_2 = {1: teamAgent, 2: randomAgent}
    win_times_P1 = 0
    win_times_P2 = 0
    tie_times = 0
    for i in range(10):
        run_result = runGame_vir(ccgame, agents_dict_1)
        #print(run_result)
        if run_result == 1:
            win_times_P1 += 1
        elif run_result == 2:
            win_times_P2 += 1
        elif run_result == 0:
            tie_times += 1
    '''
    run_result = runGame_vir(ccgame, agents_dict_2)
    print(run_result)
    if run_result == 1:
        win_times_P1 += 1
    elif run_result == 2:
        win_times_P2 += 1
    elif run_result == 0:
        tie_times += 1
    '''
    rate = win_times_P1 / 10
    print("win rate:", rate)
    return rate

if '__main__' == __name__:
    print("hello")
    engine.run(ng=10)