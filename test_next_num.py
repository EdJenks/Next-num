import unittest
import next_num

class TestNextNumInputs(unittest.TestCase):
    """
    Test invalid inputs
    """
    def test_negative_probabilites_raise_error(self):
        test_distribution = [1, 2, 3, 4, 5]
        test_probabilities = [0.01, -0.3, 0.58, 0.1, 0.01]
        
        with self.assertRaises(ValueError) as NE:
            generator = next_num.RandomGen(test_distribution, test_probabilities)
        self.assertEqual(
            "Probabilites must be positive",
            str(NE.exception)
        )

    def test_incorrect_sum_probabilites_raise_error(self):
        test_distribution = [1, 2, 3, 4, 5]
        test_probabilities = [0.01, 0.29, 0.58, 0.1, 0.01]
        
        with self.assertRaises(ValueError) as NE:
            generator = next_num.RandomGen(test_distribution, test_probabilities)
        self.assertEqual(
            "Probabilites must sum to 1.",
            str(NE.exception)
        )

    def test_large_probabilites_raise_error(self):
        test_distribution = [1, 2, 3, 4, 5]
        test_probabilities = [0.01, 1.3, 0.58, 0.1, 0.01]
        
        with self.assertRaises(ValueError) as NE:
            generator = next_num.RandomGen(test_distribution, test_probabilities)
        self.assertEqual(
            "Probabilites must not be greater than 1.",
            str(NE.exception)
        )
    

class TestNextNumValueGeneration(unittest.TestCase):
    """
    Test the function returns correct values
    """
    def test_returns_values_in_input__list(self):
        test_distribution = [1, 2, 3, 4, 5]
        test_probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
        generator = next_num.RandomGen(test_distribution, test_probabilities)

        for i in range(1000):
            return_value = generator.next_num()
            self.assertTrue(return_value in test_distribution)

if __name__ == "__main__":
    unittest.main()