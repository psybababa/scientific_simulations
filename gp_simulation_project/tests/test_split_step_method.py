import unittest
from src.split_step_method import SplitStepMethod

class TestSplitStepMethod(unittest.TestCase):

    def setUp(self):
        self.split_step = SplitStepMethod()

    def test_initialization(self):
        self.assertIsNotNone(self.split_step)

    def test_time_evolution(self):
        initial_wave_function = self.split_step.initialize_wave_function()
        evolved_wave_function = self.split_step.time_evolution(initial_wave_function, dt=0.01, steps=100)
        self.assertEqual(evolved_wave_function.shape, initial_wave_function.shape)

    def test_boundary_conditions(self):
        wave_function = self.split_step.initialize_wave_function()
        self.split_step.apply_boundary_conditions(wave_function)
        # Check if boundary conditions are applied correctly (example check)
        self.assertAlmostEqual(wave_function[0], 0)
        self.assertAlmostEqual(wave_function[-1], 0)

if __name__ == '__main__':
    unittest.main()