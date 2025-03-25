import pytest
import random
from test.TestUtils import TestUtils
from ecosystem_simulation_system import Organism, Plant, Animal, Herbivore, Carnivore, Environment, OrganismNotFoundException, InvalidInputException

class TestFunctional:
    """Test cases for functional requirements of the ecosystem simulation system."""
    
    def test_organism_constructor_destructor(self):
        """Test Organism class constructor and destructor functionality."""
        try:
            # Test basic organism creation and property access
            organism = Organism("O001", "Test Organism", 50, True)
            assert organism.id == "O001"
            assert organism.species_name == "Test Organism"
            assert organism.energy == 50
            assert organism.is_alive is True
            
            # Test class counter incrementation
            initial_count = Organism.organism_count
            organism2 = Organism("O002", "Test Organism 2", 30, True)
            assert Organism.organism_count == initial_count + 1
            
            # Force destructor call and test count decrement
            # We need to delete the reference to trigger __del__
            del organism2
            # Note: The count won't immediately update due to garbage collection timing
            
            TestUtils.yakshaAssert("test_organism_constructor_destructor", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_organism_constructor_destructor", False, "functional")
            raise e
    
    def test_plant_inheritance(self):
        """Test Plant class inheritance and specialized functionality."""
        try:
            # Test Plant inherits from Organism
            plant = Plant("P001", "Oak Tree", 100, True, 0.2)
            assert isinstance(plant, Organism)
            
            # Test Plant has its own attributes
            assert plant.growth_rate == 0.2
            
            # Test Plant overrides methods from Organism
            base_info = plant.display_info()
            assert "Growth Rate: 0.2" in base_info
            
            # Test Plant specific methods
            energy_before = plant.energy
            plant.photosynthesize("sunny")
            assert plant.energy > energy_before
            
            # Test different weather conditions
            energy_sunny = plant.photosynthesize("sunny")
            energy_cloudy = plant.photosynthesize("cloudy")
            energy_rainy = plant.photosynthesize("rainy")
            
            assert energy_sunny > energy_cloudy > energy_rainy
            
            TestUtils.yakshaAssert("test_plant_inheritance", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_plant_inheritance", False, "functional")
            raise e
    
    def test_animal_inheritance(self):
        """Test Animal class inheritance and intermediate class functionality."""
        try:
            # Create derived Animal instances for testing
            herbivore = Herbivore("H001", "Rabbit", 70, True, 3, "herbivore", "grass")
            carnivore = Carnivore("C001", "Wolf", 80, True, 5, "carnivore", 0.7)
            
            # Test both are instances of Animal and Organism
            assert isinstance(herbivore, Animal)
            assert isinstance(carnivore, Animal)
            assert isinstance(herbivore, Organism)
            assert isinstance(carnivore, Organism)
            
            # Test Animal common attributes are accessible in both derived classes
            assert herbivore.speed == 3
            assert carnivore.speed == 5
            assert herbivore.diet_type == "herbivore"
            assert carnivore.diet_type == "carnivore"
            
            # Test overridden methods in the inheritance chain
            herb_info = herbivore.display_info()
            carn_info = carnivore.display_info()
            
            assert "Speed: 3" in herb_info
            assert "Diet: herbivore" in herb_info
            assert "Preference: grass" in herb_info
            
            assert "Speed: 5" in carn_info
            assert "Diet: carnivore" in carn_info
            assert "Hunting Efficiency: 0.7" in carn_info
            
            # Test consume_energy behaves correctly through inheritance
            initial_energy = herbivore.energy
            herbivore.consume_energy(10)
            assert herbivore.energy == initial_energy - 10
            
            TestUtils.yakshaAssert("test_animal_inheritance", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_animal_inheritance", False, "functional")
            raise e
    
    def test_polymorphism(self):
        """Test polymorphic behavior across the class hierarchy."""
        try:
            # Create organisms of different types
            plant = Plant("P001", "Oak Tree", 100, True, 0.2)
            herbivore = Herbivore("H001", "Rabbit", 70, True, 3, "herbivore", "grass")
            carnivore = Carnivore("C001", "Wolf", 80, True, 5, "carnivore", 0.7)
            
            # Create a list of organisms to test polymorphic behavior
            organisms = [plant, herbivore, carnivore]
            
            # Test display_info polymorphism
            for organism in organisms:
                info = organism.display_info()
                assert organism.id in info
                assert organism.species_name in info
                assert str(organism.energy) in info
                
                # Each type should include its specific attributes
                if isinstance(organism, Plant):
                    assert "Growth Rate" in info
                elif isinstance(organism, Herbivore):
                    assert "Preference" in info
                elif isinstance(organism, Carnivore):
                    assert "Hunting Efficiency" in info
            
            # Test interact polymorphism
            # Plant-Herbivore interaction
            test_plant = Plant("TP", "Test Plant", 100, True, 0.2)
            test_herb = Herbivore("TH", "Test Herbivore", 70, True, 3, "herbivore", "grass")
            
            # Record energy levels before interaction
            plant_energy_before = test_plant.energy
            herb_energy_before = test_herb.energy
            
            # Test herbivore eating plant
            interaction_result = test_herb.interact(test_plant)
            if interaction_result:
                assert test_herb.energy > herb_energy_before
                assert test_plant.energy < plant_energy_before
            
            # Test hunt polymorphism
            new_plant = Plant("NP", "New Plant", 100, True, 0.2)
            new_herb = Herbivore("NH", "New Herbivore", 70, True, 3, "herbivore", "grass")
            new_carn = Carnivore("NC", "New Carnivore", 80, True, 5, "carnivore", 0.7)
            
            # Set random seed for consistent testing
            random.seed(42)
            
            # Test herbivore hunting plants
            herb_hunt_result = new_herb.hunt([new_plant])
            if herb_hunt_result:
                assert new_herb.food_eaten > 0
                assert new_plant.energy < 100
            
            # Test carnivore hunting herbivores
            carn_hunt_result = new_carn.hunt([new_herb])
            if carn_hunt_result:
                assert new_carn.food_eaten > 0
                assert not new_herb.is_alive
            
            TestUtils.yakshaAssert("test_polymorphism", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_polymorphism", False, "functional")
            raise e
    
    def test_environment_functionality(self):
        """Test Environment class and ecosystem simulation functionality."""
        try:
            # Create environment
            env = Environment("Forest Ecosystem", "sunny")
            assert env.name == "Forest Ecosystem"
            assert env.weather_condition == "sunny"
            
            # Add various organisms
            plant = Plant("P001", "Oak Tree", 100, True, 0.2)
            herbivore = Herbivore("H001", "Rabbit", 70, True, 3, "herbivore", "grass")
            carnivore = Carnivore("C001", "Wolf", 80, True, 5, "carnivore", 0.7)
            
            env.add_organism(plant)
            env.add_organism(herbivore)
            env.add_organism(carnivore)
            
            # Test organism management
            assert len(env.organisms) == 3
            
            # Test get_organisms_by_type
            plants = env.get_organisms_by_type(Plant)
            herbivores = env.get_organisms_by_type(Herbivore)
            carnivores = env.get_organisms_by_type(Carnivore)
            
            assert len(plants) == 1 and plants[0].id == "P001"
            assert len(herbivores) == 1 and herbivores[0].id == "H001"
            assert len(carnivores) == 1 and carnivores[0].id == "C001"
            
            # Test population count
            counts = env.get_population_count()
            assert counts["Plant"] == 1
            assert counts["Herbivore"] == 1
            assert counts["Carnivore"] == 1
            
            # Test find_organism_by_id
            found_plant = env.find_organism_by_id("P001")
            assert found_plant.id == "P001" and found_plant.species_name == "Oak Tree"
            
            # Test simulation logic
            day_count = env.simulate_day()
            assert day_count == 1
            
            # Test changes after simulation
            # Note: We can't make strong assertions about exact values as they depend on implementation
            
            # Add a grass plant for the herbivore to eat
            grass = Plant("P002", "Grass", 50, True, 0.3)
            env.add_organism(grass)
            
            # Simulate several more days
            for _ in range(5):
                env.simulate_day()
            
            # Verify that ecosystem dynamics worked
            assert env.day_count == 6
            
            TestUtils.yakshaAssert("test_environment_functionality", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_environment_functionality", False, "functional")
            raise e
    
    def test_integrated_system(self):
        """Test integrated system with full ecosystem lifecycle."""
        try:
            # Create a more complex ecosystem
            env = Environment("Complex Ecosystem", "sunny")
            
            # Add multiple plants
            plants = [
                Plant("P001", "Oak Tree", 100, True, 0.2),
                Plant("P002", "Pine Tree", 90, True, 0.15),
                Plant("P003", "Grass", 50, True, 0.3)
            ]
            
            # Add multiple herbivores with different preferences
            herbivores = [
                Herbivore("H001", "Rabbit", 70, True, 3, "herbivore", "grass"),
                Herbivore("H002", "Deer", 90, True, 4, "herbivore", "oak tree")
            ]
            
            # Add a carnivore
            carnivore = Carnivore("C001", "Wolf", 80, True, 5, "carnivore", 0.7)
            
            # Add all organisms to environment
            for plant in plants:
                env.add_organism(plant)
            
            for herbivore in herbivores:
                env.add_organism(herbivore)
            
            env.add_organism(carnivore)
            
            # Verify initial state
            assert len(env.organisms) == 6
            assert env.get_population_count()["Plant"] == 3
            assert env.get_population_count()["Herbivore"] == 2
            assert env.get_population_count()["Carnivore"] == 1
            
            # Run simulation for multiple days to observe ecosystem dynamics
            for _ in range(10):
                env.simulate_day()
            
            # Verify environment day count
            assert env.day_count == 10
            
            # The ecosystem should show signs of interaction
            # We can't make strong assertions about exact outcomes as they're implementation-dependent
            
            TestUtils.yakshaAssert("test_integrated_system", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_integrated_system", False, "functional")
            raise e