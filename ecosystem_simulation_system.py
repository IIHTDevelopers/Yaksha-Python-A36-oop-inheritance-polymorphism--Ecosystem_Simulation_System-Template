"""
Ecosystem Simulation

This module implements a simplified ecosystem simulation for EcoLearn Foundation
to demonstrate inheritance and polymorphism through object-oriented programming.
"""

import random


class OrganismNotFoundException(Exception):
    """Exception raised when an organism is not found in the environment."""
    pass


class InvalidInputException(Exception):
    """Exception raised when invalid input is provided."""
    pass


class Organism:
    """Base class representing any organism in the ecosystem."""
    
    organism_count = 0
    
    def __init__(self, id, species_name, energy, is_alive):
        """Initialize an Organism with required attributes."""
        # Validate parameters
        if not isinstance(id, str) or not id:
            raise InvalidInputException("Organism ID must be a non-empty string")
        
        # Initialize attributes
        self._id = id
        self._species_name = species_name
        self._energy = energy
        self._is_alive = is_alive
        
        # Increment organism count
        Organism.organism_count += 1
    
    def __del__(self):
        """Clean up resources when the object is destroyed."""
        Organism.organism_count -= 1
    
    @property
    def id(self): return self._id
    
    @property
    def species_name(self): return self._species_name
    
    @property
    def energy(self): return self._energy
    
    @energy.setter
    def energy(self, value):
        self._energy = max(0, value)
        if self._energy <= 0:
            self._is_alive = False
    
    @property
    def is_alive(self): return self._is_alive
    
    def consume_energy(self, amount):
        """Consume energy for activities."""
        self.energy -= amount
        return self._is_alive
    
    def interact(self, other_organism):
        """Interact with another organism."""
        # Base implementation does nothing
        return False
    
    def display_info(self):
        """Display organism information."""
        status = "Alive" if self._is_alive else "Dead"
        return f"{self._id} | {self._species_name} | Energy: {self._energy} | Status: {status}"


class Plant(Organism):
    """Class representing plant organisms."""
    
    def __init__(self, id, species_name, energy, is_alive, growth_rate):
        """Initialize a Plant with required attributes."""
        super().__init__(id, species_name, energy, is_alive)
        self._growth_rate = growth_rate
    
    @property
    def growth_rate(self): return self._growth_rate
    
    def photosynthesize(self, weather_condition):
        """Generate energy through photosynthesis based on weather."""
        # Different weather conditions affect photosynthesis efficiency
        weather_factors = {
            "sunny": 1.0,
            "cloudy": 0.6,
            "rainy": 0.3
        }
        
        factor = weather_factors.get(weather_condition, 0.5)
        energy_gain = 10 * self._growth_rate * factor
        
        self.energy += energy_gain
        return energy_gain
    
    def interact(self, other_organism):
        """Plants can be eaten by herbivores."""
        if isinstance(other_organism, Herbivore) and self._is_alive:
            energy_transfer = min(25, self._energy)
            other_organism.energy += energy_transfer
            self.energy -= energy_transfer
            return True
        return False
    
    def display_info(self):
        """Display plant-specific information."""
        base_info = super().display_info()
        return f"{base_info} | Growth Rate: {self._growth_rate}"


class Animal(Organism):
    """Base class representing animal organisms."""
    
    def __init__(self, id, species_name, energy, is_alive, speed, diet_type):
        """Initialize an Animal with required attributes."""
        super().__init__(id, species_name, energy, is_alive)
        self._speed = speed
        self._diet_type = diet_type
        self._food_eaten = 0
    
    @property
    def speed(self): return self._speed
    
    @property
    def diet_type(self): return self._diet_type
    
    @property
    def food_eaten(self): return self._food_eaten
    
    def hunt(self, prey_organisms):
        """Base hunt method to be overridden by derived classes."""
        pass
    
    def display_info(self):
        """Display animal-specific information."""
        base_info = super().display_info()
        return f"{base_info} | Speed: {self._speed} | Diet: {self._diet_type}"


class Herbivore(Animal):
    """Class representing herbivore animals."""
    
    def __init__(self, id, species_name, energy, is_alive, speed, diet_type, plant_preference):
        """Initialize a Herbivore with required attributes."""
        super().__init__(id, species_name, energy, is_alive, speed, diet_type)
        self._plant_preference = plant_preference
    
    @property
    def plant_preference(self): return self._plant_preference
    
    def hunt(self, prey_organisms):
        """Herbivores 'hunt' by foraging for plants."""
        if not self._is_alive:
            return False
        
        # Herbivores can only eat plants
        available_plants = [org for org in prey_organisms if isinstance(org, Plant) and org.is_alive]
        
        if not available_plants:
            return False
        
        # Find plants with matching preference if possible
        preferred_plants = [p for p in available_plants 
                           if p.species_name.lower() == self._plant_preference.lower()]
        
        if preferred_plants:
            target_plant = random.choice(preferred_plants)
        else:
            target_plant = random.choice(available_plants)
        
        # Consume plant energy
        energy_gain = min(target_plant.energy, 25)  # Cap energy gain
        self.energy += energy_gain
        target_plant.energy -= energy_gain
        
        self._food_eaten += 1
        return True
    
    def interact(self, other_organism):
        """Herbivores eat plants."""
        if isinstance(other_organism, Plant) and self._is_alive and other_organism.is_alive:
            energy_transfer = min(25, other_organism.energy)
            self.energy += energy_transfer
            other_organism.energy -= energy_transfer
            self._food_eaten += 1
            return True
        return False
    
    def display_info(self):
        """Display herbivore-specific information."""
        base_info = super().display_info()
        return f"{base_info} | Preference: {self._plant_preference}"


class Carnivore(Animal):
    """Class representing carnivore animals."""
    
    def __init__(self, id, species_name, energy, is_alive, speed, diet_type, hunting_efficiency):
        """Initialize a Carnivore with required attributes."""
        super().__init__(id, species_name, energy, is_alive, speed, diet_type)
        self._hunting_efficiency = hunting_efficiency
    
    @property
    def hunting_efficiency(self): return self._hunting_efficiency
    
    def hunt(self, prey_organisms):
        """Hunt for herbivores."""
        if not self._is_alive:
            return False
        
        # Carnivores can only eat herbivores
        available_prey = [org for org in prey_organisms if isinstance(org, Herbivore) and org.is_alive]
        
        if not available_prey:
            return False
        
        # Select a random prey
        target_prey = random.choice(available_prey)
        
        # Hunt success chance depends on efficiency and prey's speed
        success_chance = self._hunting_efficiency * (self._speed / (target_prey.speed + 1))
        
        if random.random() <= success_chance:
            # Successful hunt
            energy_gain = min(target_prey.energy * 0.7, 50)  # Cap energy gain
            self.energy += energy_gain
            target_prey.energy = 0  # Kill the prey
            
            self._food_eaten += 1
            return True
        else:
            # Failed hunt, still consumes energy
            self.consume_energy(5)
            return False
    
    def interact(self, other_organism):
        """Carnivores hunt herbivores."""
        if isinstance(other_organism, Herbivore) and self._is_alive and other_organism.is_alive:
            # Hunt success depends on efficiency
            if random.random() <= self._hunting_efficiency:
                energy_transfer = min(40, other_organism.energy)
                self.energy += energy_transfer
                other_organism.energy = 0  # Kill the prey
                self._food_eaten += 1
                return True
        return False
    
    def display_info(self):
        """Display carnivore-specific information."""
        base_info = super().display_info()
        return f"{base_info} | Hunting Efficiency: {self._hunting_efficiency:.2f}"


class Environment:
    """Class representing the ecosystem environment."""
    
    def __init__(self, name, weather_condition):
        """Initialize an Environment with required attributes."""
        self.__name = name
        self.__weather_condition = weather_condition
        self.__organisms = []
        self.__day_count = 0
        self.__next_id = 1
    
    @property
    def name(self): return self.__name
    
    @property
    def weather_condition(self): return self.__weather_condition
    
    @weather_condition.setter
    def weather_condition(self, condition):
        valid_conditions = ["sunny", "cloudy", "rainy"]
        if condition in valid_conditions:
            self.__weather_condition = condition
    
    @property
    def organisms(self): return self.__organisms.copy()
    
    @property
    def day_count(self): return self.__day_count
    
    def get_next_id(self):
        """Get next available ID for a new organism."""
        id_val = self.__next_id
        self.__next_id += 1
        return id_val
    
    def add_organism(self, organism):
        """Add an organism to the environment."""
        # Check if organism already exists
        if any(org.id == organism.id for org in self.__organisms):
            return False
        
        self.__organisms.append(organism)
        return True
    
    def remove_organism(self, organism_id):
        """Remove an organism from the environment."""
        for i, organism in enumerate(self.__organisms):
            if organism.id == organism_id:
                self.__organisms.pop(i)
                return True
        
        return False
    
    def find_organism_by_id(self, organism_id):
        """Find an organism by ID."""
        for organism in self.__organisms:
            if organism.id == organism_id:
                return organism
        
        raise OrganismNotFoundException(f"Organism with ID {organism_id} not found")
    
    def get_organisms_by_type(self, organism_class):
        """Get all organisms of a specific type."""
        return [org for org in self.__organisms if isinstance(org, organism_class)]
    
    def get_population_count(self):
        """Get population counts by organism type."""
        counts = {
            "Plant": len([o for o in self.__organisms if isinstance(o, Plant) and o.is_alive]),
            "Herbivore": len([o for o in self.__organisms if isinstance(o, Herbivore) and o.is_alive]),
            "Carnivore": len([o for o in self.__organisms if isinstance(o, Carnivore) and o.is_alive])
        }
        
        return counts
    
    def simulate_day(self):
        """Simulate one day in the ecosystem."""
        self.__day_count += 1
        
        # Randomly change weather sometimes
        if random.random() < 0.3:
            weather_options = ["sunny", "cloudy", "rainy"]
            self.__weather_condition = random.choice(weather_options)
        
        # Plants photosynthesize
        for organism in self.__organisms:
            if isinstance(organism, Plant) and organism.is_alive:
                organism.photosynthesize(self.__weather_condition)
        
        # Carnivores hunt
        carnivores = self.get_organisms_by_type(Carnivore)
        herbivores = self.get_organisms_by_type(Herbivore)
        for carnivore in carnivores:
            if carnivore.is_alive:
                carnivore.hunt(herbivores)
        
        # Herbivores forage
        herbivores = [h for h in herbivores if h.is_alive]  # Update to living herbivores only
        plants = self.get_organisms_by_type(Plant)
        for herbivore in herbivores:
            if herbivore.is_alive:
                herbivore.hunt(plants)
        
        # All organisms consume daily energy
        for organism in self.__organisms:
            if organism.is_alive:
                if isinstance(organism, Plant):
                    organism.consume_energy(1)  # Plants consume minimal energy
                elif isinstance(organism, Animal):
                    organism.consume_energy(2 + organism.speed * 0.1)  # Animals consume more
        
        return self.__day_count


def main():
    """Main function to run the ecosystem simulation."""
    # Create a pre-made environment
    forest = Environment("Forest Ecosystem", "sunny")
    
    # Add initial organisms
    try:
        # Plants
        forest.add_organism(Plant("P001", "Oak Tree", 100, True, 0.2))
        forest.add_organism(Plant("P002", "Pine Tree", 90, True, 0.15))
        forest.add_organism(Plant("P003", "Grass", 50, True, 0.3))
        
        # Herbivores
        forest.add_organism(Herbivore("H001", "Rabbit", 70, True, 3, "herbivore", "grass"))
        
        # Carnivores
        forest.add_organism(Carnivore("C001", "Wolf", 80, True, 5, "carnivore", 0.7))
    except Exception as e:
        print(f"Error setting up environment: {e}")
    
    # Menu-based interaction
    while True:
        print("\n===== ECOSYSTEM SIMULATION =====")
        print(f"Environment: {forest.name}")
        print(f"Weather: {forest.weather_condition}")
        print(f"Total Organisms: {len(forest.organisms)}")
        
        counts = forest.get_population_count()
        print("\nPopulation Breakdown:")
        for species, count in counts.items():
            print(f"  {species}: {count}")
        
        print(f"\nSimulation Day: {forest.day_count}")
        
        print("\nMenu:")
        print("1. Add Organism to Environment")
        print("2. Simulate One Day")
        print("3. Simulate Multiple Days")
        print("4. Display All Organisms")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice (0-4): "))
            
            if choice == 1:
                print("\nSelect organism type:")
                print("1. Plant")
                print("2. Herbivore")
                print("3. Carnivore")
                
                org_type = int(input("Enter choice (1-3): "))
                
                # Common attributes
                if org_type == 1:
                    id_prefix = "P"
                    type_name = "Plant"
                elif org_type == 2:
                    id_prefix = "H"
                    type_name = "Herbivore"
                elif org_type == 3:
                    id_prefix = "C"
                    type_name = "Carnivore"
                else:
                    raise InvalidInputException("Invalid organism type")
                
                id_num = forest.get_next_id()
                org_id = f"{id_prefix}{id_num:03d}"
                
                # Get species from predefined list based on type
                if org_type == 1:  # Plant
                    species_list = ["Oak Tree", "Pine Tree", "Grass", "Fern", "Shrub"]
                elif org_type == 2:  # Herbivore
                    species_list = ["Rabbit", "Deer", "Mouse", "Squirrel", "Beaver"]
                else:  # Carnivore
                    species_list = ["Wolf", "Fox", "Hawk", "Snake", "Lynx"]
                
                print("\nSelect species:")
                for i, species in enumerate(species_list, 1):
                    print(f"{i}. {species}")
                
                species_choice = int(input(f"Enter choice (1-{len(species_list)}): "))
                if 1 <= species_choice <= len(species_list):
                    species = species_list[species_choice-1]
                else:
                    raise InvalidInputException("Invalid species selection")
                
                # Energy level
                energy = float(input("Enter energy level (10-100): "))
                if not (10 <= energy <= 100):
                    raise InvalidInputException("Energy must be between 10 and 100")
                
                # Create organism based on type
                try:
                    if org_type == 1:  # Plant
                        growth_rates = [0.1, 0.2, 0.3, 0.4, 0.5]
                        print("\nSelect growth rate:")
                        for i, rate in enumerate(growth_rates, 1):
                            print(f"{i}. {rate}")
                        
                        rate_choice = int(input("Enter choice (1-5): "))
                        if 1 <= rate_choice <= 5:
                            growth_rate = growth_rates[rate_choice-1]
                        else:
                            raise InvalidInputException("Invalid growth rate selection")
                            
                        organism = Plant(org_id, species, energy, True, growth_rate)
                    
                    elif org_type == 2:  # Herbivore
                        speeds = [1, 2, 3, 4, 5]
                        print("\nSelect speed:")
                        for i, speed in enumerate(speeds, 1):
                            print(f"{i}. {speed}")
                        
                        speed_choice = int(input("Enter choice (1-5): "))
                        if 1 <= speed_choice <= 5:
                            speed = speeds[speed_choice-1]
                        else:
                            raise InvalidInputException("Invalid speed selection")
                        
                        preferences = ["Grass", "Oak Tree", "Pine Tree", "Shrub", "Fern"]
                        print("\nSelect plant preference:")
                        for i, pref in enumerate(preferences, 1):
                            print(f"{i}. {pref}")
                        
                        pref_choice = int(input("Enter choice (1-5): "))
                        if 1 <= pref_choice <= 5:
                            preference = preferences[pref_choice-1]
                        else:
                            raise InvalidInputException("Invalid preference selection")
                            
                        organism = Herbivore(org_id, species, energy, True, speed, "herbivore", preference)
                    
                    elif org_type == 3:  # Carnivore
                        speeds = [3, 4, 5, 6, 7]
                        print("\nSelect speed:")
                        for i, speed in enumerate(speeds, 1):
                            print(f"{i}. {speed}")
                        
                        speed_choice = int(input("Enter choice (1-5): "))
                        if 1 <= speed_choice <= 5:
                            speed = speeds[speed_choice-1]
                        else:
                            raise InvalidInputException("Invalid speed selection")
                        
                        efficiencies = [0.3, 0.4, 0.5, 0.6, 0.7]
                        print("\nSelect hunting efficiency:")
                        for i, eff in enumerate(efficiencies, 1):
                            print(f"{i}. {eff}")
                        
                        eff_choice = int(input("Enter choice (1-5): "))
                        if 1 <= eff_choice <= 5:
                            efficiency = efficiencies[eff_choice-1]
                        else:
                            raise InvalidInputException("Invalid efficiency selection")
                            
                        organism = Carnivore(org_id, species, energy, True, speed, "carnivore", efficiency)
                    
                    # Add to environment
                    if forest.add_organism(organism):
                        print(f"{type_name} '{org_id}' added successfully.")
                    else:
                        print(f"Organism with ID {org_id} already exists.")
                
                except Exception as e:
                    print(f"Error adding organism: {e}")
            
            elif choice == 2:
                try:
                    forest.simulate_day()
                    print(f"Day {forest.day_count} simulated successfully.")
                    
                    # Show status of organisms after simulation
                    alive_count = len([o for o in forest.organisms if o.is_alive])
                    dead_count = len(forest.organisms) - alive_count
                    print(f"Living organisms: {alive_count}")
                    print(f"Dead organisms: {dead_count}")
                    
                except Exception as e:
                    print(f"Error during simulation: {e}")
            
            elif choice == 3:
                try:
                    days = int(input("Enter number of days to simulate (1-10): "))
                    if not (1 <= days <= 10):
                        raise InvalidInputException("Days must be between 1 and 10")
                    
                    for _ in range(days):
                        forest.simulate_day()
                    
                    print(f"{days} days simulated successfully.")
                    print(f"Current day: {forest.day_count}")
                    
                    # Show status of organisms after simulation
                    alive_count = len([o for o in forest.organisms if o.is_alive])
                    dead_count = len(forest.organisms) - alive_count
                    print(f"Living organisms: {alive_count}")
                    print(f"Dead organisms: {dead_count}")
                    
                except Exception as e:
                    print(f"Error during simulation: {e}")
            
            elif choice == 4:
                print("\nAll Organisms:")
                for organism in forest.organisms:
                    print(organism.display_info())
            
            elif choice == 0:
                print("Thank you for using the Ecosystem Simulation.")
                break
            
            else:
                print("Invalid choice. Please enter a number between 0 and 4.")
        
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()