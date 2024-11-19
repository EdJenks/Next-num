import random
import collections
import bisect
from decimal import *

class RandomGen(object):

    def __init__(self, random_nums, probabilities):
        """
        Initialise values that may be returned by next_num() as an attribute of the class
        Initialise probability of the occurence of a given random_num as an attribute of the class
        """
        self.random_nums = random_nums
        self.probabilities = probabilities

        """
        If this is a production module or a user inputted module - we need to check the validity of the inputs.
        Probabilities should sum to 1 (within float rounding), and should be positive (is 0 allowed? is 1 allowed?).
        """
        if any(probability < 0 for probability in self.probabilities):
             raise ValueError("Probabilites must be positive")
        
        if any(probability > 1 for probability in self.probabilities):
             """
             This should be caught by the first two checks but for completeness
             """
             raise ValueError("Probabilites must not be greater than 1.")
        if (abs(self.return_cumulative_probabilites()[-1] - 1)) > 1e-8:
             raise ValueError("Probabilites must sum to 1.")
        

    def return_cumulative_probabilites(self):
        """
        Return a pseudo cumulative distribution function of the possible numbers' occurances.
        Defining this before the __init__ is a little against the grain, but I'd still rather 
        have this inside the module
        """
        cumulative_value  = 0
        cumulative_probabilites = []
        
        for prob in self.probabilities:
             cumulative_value += prob
             cumulative_probabilites.append(cumulative_value)

        return cumulative_probabilites


    def next_num(self):
        """
        Returns one of the randomNums. When this method is called multiple
        times over a long period, it should return the numbers roughly with
        the initialized probabilities.
        """
        random_probability = random.random()
        cumulative_probabilites = self.return_cumulative_probabilites()
        cumulative_probabilites[-1] = 1.0

        """ 
        There is an edge case here where random.random returns a value higher than our highest cumulative probability,
        just because of floating point number rounding to and from binary memory - fixing the final value of the list like 
        this techincally skewes how 'random' our distribution or picking a number is, as I have artifically enlarged the 
        final number's range of distribution, but this is better than having an error. 
        We could raise an error or skip this number if random.random does return a high decimal and not break our function -
        but these also involve skewing our distribution, which isn't truly random after the floating point rounding anyway,
        so I have decided this is an okay exception to make.
        """
        index_of_random_num = bisect.bisect_left(cumulative_probabilites, random_probability)
        """
        bisect left returns for us here the index of the number to be in the given range of probability in the CDF
        """

        return self.random_nums[index_of_random_num]

"""
Using the module (testing)
"""

if __name__ == "__main__":
    iterations = 100000
    distribution = [-1, 0, 1, 2, 3] 
    probabilities = [0.01, 0.3, 0.58, 0.1, 0.01] 
    next_num_generator = RandomGen(distribution, probabilities)
    count = collections.defaultdict(int)

    for i in range(iterations):
        return_value = next_num_generator.next_num()
        count[return_value] += 1

    print(f"Distribution: {distribution}")
    print(f"Probabilites: {probabilities}")

    for index, num in enumerate(distribution):
        expected = int(iterations * probabilities[index])
        actual = count[num]
        deviation = round(abs(((actual - expected) / expected) * 100), 2)
        print(
            f"{num}: Expected; {expected}, Actual; {actual}, Deviation; {deviation}%"
        )
