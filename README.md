# Python-genetic-algorithm
  The genetic algorithm (GA) can be considered as one of the varieties of random search, which is based on mechanisms resembling natural selection and reproduction.
  Unlike existing techniques, GA starts with a random set of initial solutions called a population. Each element in the population is called a chromosome and represents a solution to the problem as a first approximation. A chromosome is a string of characters of some nature, not necessarily binary. Chromosomes evolve over many iterations called generations. During each iteration, the chromosome is evaluated using some measure of conformity (fitness function), which we will call the correspondence function. To create the next generation, new chromosomes, called offspring, are formed either by crossing two chromosomes - parents from the current population, or by randomly changing (mutating) one chromosome. A new population is formed by (a) selecting according to the matching function of some parents and offspring and (b) removing the remaining ones in order to keep the population size constant.
  Chromosomes with a larger matching function are more likely to be selected (to survive). After several iterations, the algorithm converges to a better chromosome, which is either optimal or close to the optimal solution. Let P (t) and C (t) be the parents and siblings from the current generation t. The general structure of the genetic algorithm is:

begin:
      t:=0;
      set_start_value P(t);
      evaluete P(t) using the match function;
      while (no termination condition) do
        crossing P(t) to obtein C(t);
        evaluete C(t) using the match function;
        choise P(t+1) from P(t) and C(t);
        t:=t+1
       end
 end
 
  Thus, two types of operations are used: 
  1. Genetic operations: crossing and mutation; 
  2. Evolutionary operation: a choice. 
  Genetic operations are reminiscent of the process of gene inheritance when creating a new offspring in each generation. The evolutionary operation, moving from one population to the next, resembles the process of Darwin evolution.
