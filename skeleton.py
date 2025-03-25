"""
Ecosystem Simulation

This module implements a simplified ecosystem simulation for EcoLearn Foundation
to demonstrate inheritance and polymorphism through object-oriented programming.

TODO: Implement all the classes and methods following the specifications
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
    
    organism_count = 0  # Class variable to track total organisms
    
    def __init__(self, id, species_name, energy, is_alive):
        """
        Initialize an Organism with required attributes.
        
        Args:
            id: Unique identifier for the organism
            species_name: Species name of the organism
            energy: Current energy level
            is_alive: Whether the organism is alive
            
        TODO:
        - Validate parameters (id must be a non-empty string)
        - Initialize protected attributes with single underscore prefix
          (_id, _species_name, _energy, _is_alive)
        - Increment organism_count class variable
        """
        # WRITE YOUR CODE HERE
        pass
    
    def __del__(self):
        """
        Clean up resources when the object is destroyed.
        
        TODO:
        - Decrement organism_count class variable
        """
        # WRITE YOUR CODE HERE
        pass
    
    # TODO: Implement property getters and setters for:
    # id, species_name, energy, is_alive
    # NOTE: The energy setter should ensure energy is never negative and update is_alive if energy reaches 0
    
    def consume_energy(self, amount):
        """
        Consume energy for activities.
        
        Args:
            amount: Amount of energy to consume
            
        Returns:
            bool: True if organism is still alive, False otherwise
            
        TODO:
        - Decrease energy by the specified amount
        - Return whether the organism is still alive
        """
        # WRITE YOUR CODE HERE
        pass
    
    def interact(self, other_organism):
        """
        Interact with another organism.
        
        Args:
            other_organism: The organism to interact with
            
        Returns:
            bool: True if interaction had an effect, False otherwise
            
        TODO:
        - Base implementation does nothing (to be overridden by subclasses)
        - Return False
        """
        # WRITE YOUR CODE HERE
        pass
    
    def display_info(self):
        """
        Display organism information.
        
        Returns:
            str: Formatted string with organism information
            
        TODO:
        - Return a formatted string with id, species_name, energy, and status
        """
        # WRITE YOUR CODE HERE
        pass


class Plant(Organism):
    """Class representing plant organisms."""
    
    def __init__(self, id, species_name, energy, is_alive, growth_rate):
        """
        Initialize a Plant with required attributes.
        
        Args:
            id: Unique identifier for the plant
            species_name: Species name of the plant
            energy: Current energy level
            is_alive: Whether the plant is alive
            growth_rate: Rate at which the plant grows (0.1-0.5)
            
        TODO:
        - Call the parent class constructor with appropriate arguments
        - Initialize the _growth_rate attribute
        """
        # WRITE YOUR CODE HERE
        pass
    
    # TODO: Implement property getter for growth_rate
    
    def photosynthesize(self, weather_condition):
        """
        Generate energy through photosynthesis based on weather.
        
        Args:
            weather_condition: Current weather (sunny, cloudy, rainy)
            
        Returns:
            float: Amount of energy gained
            
        TODO:
        - Define weather factors dictionary: sunny (1.0), cloudy (0.6), rainy (0.3)
        - Calculate energy gain based on growth_rate and weather factor
        - Increase the plant's energy by the calculated amount
        - Return the amount of energy gained
        """
        # WRITE YOUR CODE HERE
        pass
    
    def interact(self, other_organism):
        """
        Plants can be eaten by herbivores.
        
        Args:
            other_organism: The organism to interact with
            
        Returns:
            bool: True if interaction had an effect, False otherwise
            
        TODO:
        - Check if other_organism is a Herbivore and both organisms are alive
        - If so, transfer energy from plant to herbivore (max 25 units)
        - Return True if energy was transferred, False otherwise
        """
        # WRITE YOUR CODE HERE
        pass
    
    def display_info(self):
        """
        Display plant-specific information.
        
        Returns:
            str: Formatted string with plant information
            
        TODO:
        - Get the base information from the parent class
        - Add growth_rate information to the string
        - Return the complete string
        """
        # WRITE YOUR CODE HERE
        pass


class Animal(Organism):
    """Base class representing animal organisms."""
    
    def __init__(self, id, species_name, energy, is_alive, speed, diet_type):
        """
        Initialize an Animal with required attributes.
        
        Args:
            id: Unique identifier for the animal
            species_name: Species name of the animal
            energy: Current energy level
            is_alive: Whether the animal is alive
            speed: Movement speed of the animal
            diet_type: Type of diet (herbivore, carnivore)
            
        TODO:
        - Call the parent class constructor with appropriate arguments
        - Initialize additional attributes (_speed, _diet_type, _food_eaten)
        - Set _food_eaten to 0
        """
        # WRITE YOUR CODE HERE
        pass
    
    # TODO: Implement property getters for:
    # speed, diet_type, food_eaten
    
    def hunt(self, prey_organisms):
        """
        Base hunt method to be overridden by derived classes.
        
        Args:
            prey_organisms: List of potential prey organisms
            
        Returns:
            bool: True if hunt was successful, False otherwise
            
        TODO:
        - This method should be overridden by subclasses
        - Base implementation does nothing
        """
        # WRITE YOUR CODE HERE
        pass
    
    def display_info(self):
        """
        Display animal-specific information.
        
        Returns:
            str: Formatted string with animal information
            
        TODO:
        - Get the base information from the parent class
        - Add speed and diet_type information to the string
        - Return the complete string
        """
        # WRITE YOUR CODE HERE
        pass


class Herbivore(Animal):
    """Class representing herbivore animals."""
    
    def __init__(self, id, species_name, energy, is_alive, speed, diet_type, plant_preference):
        """
        Initialize a Herbivore with required attributes.
        
        Args:
            id: Unique identifier for the herbivore
            species_name: Species name of the herbivore
            energy: Current energy level
            is_alive: Whether the herbivore is alive
            speed: Movement speed of the herbivore
            diet_type: Should be "herbivore"
            plant_preference: Preferred plant type to eat
            
        TODO:
        - Call the parent class constructor with appropriate arguments
        - Initialize the _plant_preference attribute
        """
        # WRITE YOUR CODE HERE
        pass
    
    # TODO: Implement property getter for plant_preference
    
    def hunt(self, prey_organisms):
        """
        Herbivores 'hunt' by foraging for plants.
        
        Args:
            prey_organisms: List of potential prey (plants)
            
        Returns:
            bool: True if hunt was successful, False otherwise
            
        TODO:
        - Check if herbivore is alive, if not, return False
        - Filter prey_organisms to only include living Plant objects
        - If no plants available, return False
        - Find plants matching preference if possible
        - Choose a target plant (preferred if available, otherwise random)
        - Transfer energy from plant to herbivore (max 25 units)
        - Increment food_eaten counter
        - Return True for successful hunt
        """
        # WRITE YOUR CODE HERE
        pass
    
    def interact(self, other_organism):
        """
        Herbivores eat plants.
        
        Args:
            other_organism: The organism to interact with
            
        Returns:
            bool: True if interaction had an effect, False otherwise
            
        TODO:
        - Check if other_organism is a Plant and both organisms are alive
        - If so, transfer energy from plant to herbivore (max 25 units)
        - Increment food_eaten counter
        - Return True if energy was transferred, False otherwise
        """
        # WRITE YOUR CODE HERE
        pass
    
    def display_info(self):
        """
        Display herbivore-specific information.
        
        Returns:
            str: Formatted string with herbivore information
            
        TODO:
        - Get the base information from the parent class
        - Add plant_preference information to the string
        - Return the complete string
        """
        # WRITE YOUR CODE HERE
        pass


class Carnivore(Animal):
    """Class representing carnivore animals."""
    
    def __init__(self, id, species_name, energy, is_alive, speed, diet_type, hunting_efficiency):
        """
        Initialize a Carnivore with required attributes.
        
        Args:
            id: Unique identifier for the carnivore
            species_name: Species name of the carnivore
            energy: Current energy level
            is_alive: Whether the carnivore is alive
            speed: Movement speed of the carnivore
            diet_type: Should be "carnivore"
            hunting_efficiency: Success rate for hunting (0.3-0.7)
            
        TODO:
        - Call the parent class constructor with appropriate arguments
        - Initialize the _hunting_efficiency attribute
        """
        # WRITE YOUR CODE HERE
        pass
    
    # TODO: Implement property getter for hunting_efficiency
    
    def hunt(self, prey_organisms):
        """
        Hunt for herbivores.
        
        Args:
            prey_organisms: List of potential prey (herbivores)
            
        Returns:
            bool: True if hunt was successful, False otherwise
            
        TODO:
        - Check if carnivore is alive, if not, return False
        - Filter prey_organisms to only include living Herbivore objects
        - If no herbivores available, return False
        - Choose a random herbivore as target
        - Calculate hunt success chance based on efficiency and speed ratio
        - Determine if hunt is successful based on random chance
        - If successful, transfer energy from prey to carnivore and kill prey
        - If unsuccessful, consume 5 energy units for the attempt
        - For successful hunts, increment food_eaten counter
        - Return True for successful hunt, False otherwise
        """
        # WRITE YOUR CODE HERE
        pass
    
    def interact(self, other_organism):
        """
        Carnivores hunt herbivores.
        
        Args:
            other_organism: The organism to interact with
            
        Returns:
            bool: True if interaction had an effect, False otherwise
            
        TODO:
        - Check if other_organism is a Herbivore and both organisms are alive
        - Calculate hunt success chance based on hunting_efficiency
        - If successful, transfer energy from prey to carnivore and kill prey
        - Increment food_eaten counter for successful hunts
        - Return True if energy was transferred, False otherwise
        """
        # WRITE YOUR CODE HERE
        pass
    
    def display_info(self):
        """
        Display carnivore-specific information.
        
        Returns:
            str: Formatted string with carnivore information
            
        TODO:
        - Get the base information from the parent class
        - Add hunting_efficiency information to the string
        - Return the complete string
        """
        # WRITE YOUR CODE HERE
        pass


class Environment:
    """Class representing the ecosystem environment."""
    
    def __init__(self, name, weather_condition):
        """
        Initialize an Environment with required attributes.
        
        Args:
            name: Name of the environment
            weather_condition: Current weather condition
            
        TODO:
        - Initialize private attributes with double underscore prefix
          (__name, __weather_condition, __organisms, __day_count, __next_id)
        - Set __organisms to an empty list
        - Set __day_count to 0
        - Set __next_id to 1
        """
        # WRITE YOUR CODE HERE
        pass
    
    # TODO: Implement property getters and setters for:
    # name, weather_condition, organisms, day_count
    # NOTE: organisms property should return a copy of the list
    
    def get_next_id(self):
        """
        Get next available ID for a new organism.
        
        Returns:
            int: Next available ID
            
        TODO:
        - Get the current ID value
        - Increment the internal ID counter
        - Return the ID value
        """
        # WRITE YOUR CODE HERE
        pass
    
    def add_organism(self, organism):
        """
        Add an organism to the environment.
        
        Args:
            organism: Organism to add
            
        Returns:
            bool: True if addition successful, False otherwise
            
        TODO:
        - Check if organism already exists in the environment
        - If not, add the organism to the __organisms list
        - Return True if added, False otherwise
        """
        # WRITE YOUR CODE HERE
        pass
    
    def remove_organism(self, organism_id):
        """
        Remove an organism from the environment.
        
        Args:
            organism_id: ID of the organism to remove
            
        Returns:
            bool: True if removal successful, False otherwise
            
        TODO:
        - Find the organism with the given ID
        - If found, remove it from the __organisms list
        - Return True if removed, False otherwise
        """
        # WRITE YOUR CODE HERE
        pass
    
    def find_organism_by_id(self, organism_id):
        """
        Find an organism by ID.
        
        Args:
            organism_id: ID of the organism to find
            
        Returns:
            Organism: The found organism
            
        Raises:
            OrganismNotFoundException: If organism not found
            
        TODO:
        - Search for the organism with the given ID
        - If found, return the organism
        - If not found, raise OrganismNotFoundException
        """
        # WRITE YOUR CODE HERE
        pass
    
    def get_organisms_by_type(self, organism_class):
        """
        Get all organisms of a specific type.
        
        Args:
            organism_class: Class of organisms to get
            
        Returns:
            list: List of organisms of the specified type
            
        TODO:
        - Filter __organisms list to only include instances of the specified class
        - Return the filtered list
        """
        # WRITE YOUR CODE HERE
        pass
    
    def get_population_count(self):
        """
        Get population counts by organism type.
        
        Returns:
            dict: Dictionary with counts by organism type
            
        TODO:
        - Count living organisms of each type (Plant, Herbivore, Carnivore)
        - Return dictionary with counts
        """
        # WRITE YOUR CODE HERE
        pass
    
    def simulate_day(self):
        """
        Simulate one day in the ecosystem.
        
        Returns:
            int: Current day count
            
        TODO:
        - Increment day count
        - Randomly change weather sometimes (30% chance)
        - Plants photosynthesize
        - Carnivores hunt herbivores
        - Herbivores forage for plants
        - All organisms consume daily energy
          (Plants: 1, Animals: 2 + speed * 0.1)
        - Return current day count
        """
        # WRITE YOUR CODE HERE
        pass


def main():
    """Main function to run the ecosystem simulation."""
    # TODO: Implement the main function to:
    # 1. Create a pre-made environment called "Forest Ecosystem"
    # 2. Add initial organisms:
    #    - Plants: Oak Tree, Pine Tree, Grass
    #    - Herbivore: Rabbit
    #    - Carnivore: Wolf
    # 3. Implement a menu-driven interface with options:
    #    1. Add Organism to Environment
    #    2. Simulate One Day
    #    3. Simulate Multiple Days
    #    4. Display All Organisms
    #    0. Exit
    # WRITE YOUR CODE HERE
    pass


if __name__ == "__main__":
    main()