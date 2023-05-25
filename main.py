from random import choices, random, randrange
from typing import Callable, List, Tuple
from organism import Organism


Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[int, int], Population]
SelectionFunc = Callable[[FitnessFunc, Population], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Genome]
MutationFunc = Callable[[Genome, int, float], Genome]


def generate_population(size: int, genome_length: int) -> Population:
    return [Organism(genome_length) for _ in range(size)]


def fitness(organism: Organism):
    return sum(organism._genome)


def selection_pair(fintess_func: FitnessFunc, population: Population):
    return choices(
        population=population,
        weights=[fintess_func(genome) for genome in population],
        k=2
    )


def single_point_crossover(organism_a: Organism, organism_b: Organism) -> Tuple[Genome, Genome]:
    length = len(organism_a._genome)
    new_genome = []
    org = Organism(5)
    for i in range(length):
        new_genome.append(int((organism_a._genome[i]+organism_b._genome[i])/2))
    org._genome = new_genome
    return org


def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome._genome))
        genome._genome[index] = genome._genome[index] if random() > probability else genome._genome[index]+1
        if genome._genome[index] > 10:
            genome._genome[index] = 10
    return genome


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 400) \
        -> Tuple[Population, int]:
    population = populate_func(26, 5)
    populations = [population]
    for i in range(generation_limit):
        print(f'Generation {i}')
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)
        print(f'Best genome: {population[0]}')

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(fitness_func, population)
            new_organism_a = crossover_func(parents[0], parents[1])
            new_organism_b = crossover_func(parents[0], parents[1])

            new_organism_a = mutation_func(new_organism_a)
            new_organism_b = mutation_func(new_organism_b)
            next_generation += [new_organism_a, new_organism_b]

        population = next_generation
        populations.append(population)

    return populations

populations = run_evolution(
    populate_func=generate_population,
    fitness_func=fitness,
    fitness_limit=44,
    selection_func=selection_pair,
    crossover_func=single_point_crossover,
    mutation_func=mutation
)