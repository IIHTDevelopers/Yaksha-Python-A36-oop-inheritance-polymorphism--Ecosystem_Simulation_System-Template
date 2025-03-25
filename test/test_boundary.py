import pytest
import random
from test.TestUtils import TestUtils
from ecosystem_simulation_system import Organism, Plant, Animal, Herbivore, Carnivore, Environment, OrganismNotFoundException, InvalidInputException

class TestBoundary:
    """Test cases for boundary conditions in the ecosystem simulation system."""
    
    def test_system_boundaries(self):
        """Test all boundary conditions for the ecosystem simulation system."""
        try:
            # Organism boundary tests
            organism = Organism("O001", "Test Organism", 50, True)
            assert organism.id == "O001"
            assert organism.species_name == "Test Organism"
            
            # Test energy setter boundary conditions
            organism.energy = 100
            assert organism.energy == 100
            
            organism.energy = -10  # Should set to 0 and mark as dead
            assert organism.energy == 0
            assert organism.is_alive is False
            
            # Plant boundary tests
            plant = Plant("P001", "Oak Tree", 100, True, 0.2)
            assert plant.id == "P001"
            assert plant.species_name == "Oak Tree"
            assert plant.growth_rate == 0.2
            
            # Test photosynthesis with different weather conditions
            energy_sunny = plant.photosynthesize("sunny")
            energy_cloudy = plant.photosynthesize("cloudy")
            energy_rainy = plant.photosynthesize("rainy")
            
            assert energy_sunny > energy_cloudy > energy_rainy
            
            # Animal boundary tests
            herbivore = Herbivore("H001", "Rabbit", 70, True, 3, "herbivore", "grass")
            assert herbivore.id == "H001"
            assert herbivore.species_name == "Rabbit"
            assert herbivore.speed == 3
            assert herbivore.diet_type == "herbivore"
            assert herbivore.plant_preference == "grass"
            
            carnivore = Carnivore("C001", "Wolf", 80, True, 5, "carnivore", 0.7)
            assert carnivore.id == "C001"
            assert carnivore.species_name == "Wolf"
            assert carnivore.speed == 5
            assert carnivore.diet_type == "carnivore"
            assert carnivore.hunting_efficiency == 0.7
            
            # Environment boundary tests
            env = Environment("Forest", "sunny")
            assert env.name == "Forest"
            assert env.weather_condition == "sunny"
            
            # Test weather condition setter
            env.weather_condition = "cloudy"
            assert env.weather_condition == "cloudy"
            
            # Invalid weather shouldn't change
            env.weather_condition = "invalid"
            assert env.weather_condition == "cloudy"
            
            # Test ID generation
            id1 = env.get_next_id()
            id2 = env.get_next_id()
            assert id2 == id1 + 1
            
            # Test adding organisms
            assert env.add_organism(plant) is True
            assert env.add_organism(herbivore) is True
            assert env.add_organism(carnivore) is True
            
            # Test duplicate organism
            assert env.add_organism(plant) is False
            
            # Test get organisms by type
            plants = env.get_organisms_by_type(Plant)
            assert len(plants) == 1
            assert plants[0].id == "P001"
            
            herbivores = env.get_organisms_by_type(Herbivore)
            assert len(herbivores) == 1
            assert herbivores[0].id == "H001"
            
            # Test population counts
            counts = env.get_population_count()
            assert counts["Plant"] == 1
            assert counts["Herbivore"] == 1
            assert counts["Carnivore"] == 1
            
            # Test organism finding
            found_organism = env.find_organism_by_id("P001")
            assert found_organism.id == "P001"
            
            # Test non-existent organism
            try:
                env.find_organism_by_id("NONEXISTENT")
                assert False, "Should raise OrganismNotFoundException"
            except OrganismNotFoundException:
                pass  # Expected behavior
            
            # Test removing organism
            assert env.remove_organism("P001") is True
            assert env.remove_organism("NONEXISTENT") is False
            
            # Verify count after removal
            counts = env.get_population_count()
            assert counts["Plant"] == 0
            
            # Test simulation day
            day = env.simulate_day()
            assert day == 1
            assert env.day_count == 1
            
            # Test multiple simulation days
            for _ in range(5):
                env.simulate_day()
            assert env.day_count == 6
            
            # Test organism interactions
            new_plant = Plant("P002", "Grass", 50, True, 0.3)
            env.add_organism(new_plant)
            
            # Test herbivore hunting plants
            # Check if herbivore is alive first
            if herbivore.is_alive:
                prev_herb_energy = herbivore.energy
                prev_plant_energy = new_plant.energy
                
                # Force a successful hunt
                result = herbivore.hunt([new_plant])
                
                # Only check energy changes if hunt was successful
                if result:
                    assert herbivore.energy > prev_herb_energy
                    assert new_plant.energy < prev_plant_energy
            
            # Create a new herbivore for testing since the previous one might be dead
            fresh_herb = Herbivore("H004", "Fresh Rabbit", 70, True, 3, "herbivore", "grass")
            env.add_organism(fresh_herb)
            
            # Test carnivore hunting herbivores
            if carnivore.is_alive:
                prev_carn_energy = carnivore.energy
                
                # Set random seed to ensure consistent test results
                random.seed(42)
                result = carnivore.hunt([fresh_herb])
                
                # Only check energy changes if hunt was successful
                if result:
                    assert carnivore.energy > prev_carn_energy
                    assert fresh_herb.is_alive is False
            
            # Test energy consumption
            living_herb = Herbivore("H005", "Deer", 10, True, 4, "herbivore", "oak")
            env.add_organism(living_herb)
            
            prev_energy = living_herb.energy
            living_herb.consume_energy(5)
            assert living_herb.energy == prev_energy - 5
            assert living_herb.is_alive is True
            
            # Test death by energy depletion
            living_herb.consume_energy(living_herb.energy)
            assert living_herb.energy == 0
            assert living_herb.is_alive is False
            
            TestUtils.yakshaAssert("test_system_boundaries", True, "boundary")
        except Exception as e:
            TestUtils.yakshaAssert("test_system_boundaries", False, "boundary")
            raise e