import unittest
from src.simulation import Simulation

class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.simulation = Simulation()

    def test_initial_conditions(self):
        # Test initial conditions of the simulation
        self.assertIsNotNone(self.simulation.initial_conditions)

    def test_run_simulation(self):
        # Test the run method of the simulation
        result = self.simulation.run()
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

    def test_time_evolution(self):
        # Test the time evolution of the wave function
        initial_wave_function = self.simulation.get_wave_function()
        self.simulation.run()
        evolved_wave_function = self.simulation.get_wave_function()
        self.assertNotEqual(initial_wave_function, evolved_wave_function)

if __name__ == '__main__':
    unittest.main()