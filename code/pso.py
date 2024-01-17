from random_algo import random_algorithm
from railnl import RailNL
import copy 
import random

class Particle:
    def __init__(self, rail_network, herhalingen):
        self.position = self.initialize_position(herhalingen)
        self.velocity = self.initialize_velocity(rail_network)
        self.best_position = copy.deepcopy(self.position)
        self.best_score = rail_network.get_score()
    
    def initialize_position(self, herhalingen): # uses by default RailNL as rail_network
        return random_algorithm(herhalingen)
        

    def initialize_velocity(self, rail_network):    
        num_trajecten = len(rail_network.trajecten)
        
        # initialize velocity
        initial_velocity = []
        for i in range(num_trajecten):
            initial_velocity.append(random.uniform(-0.1, 0.1))	
        
        return initial_velocity
    
def particle_swarm_optimization(num_particles, num_iterations):
    rail_network = RailNL()
    rail_network.load_stations('StationsHolland.csv')
    rail_network.load_connections('ConnectiesHolland.csv')
    
    particles = [Particle(rail_network, 10) for i in range(num_particles)]
    global_best_particle = min(particles, key=lambda particle: particle.best_score)
    
    inertia = 0.7
    cognitive_constant = 1.5
    social_constant = 1.5   
    
    for i in range(num_iterations):
        for particle in particles:
           
            #update velocity
            for j in range(len(particle.velocity)):
                r1 = random.random()
                r2 = random.random()
                cognitive_component = cognitive_constant * r1 * (particle.best_position[j] - particle.position[j])
                social_component = social_constant * r2 * (global_best_particle.best_position[j] - particle.position[j])
                particle.velocity[j] = inertia * particle.velocity[j] + cognitive_component + social_component
                
            #update position
            for i in range(len(particle.position)):
                particle.position[i] += particle.velocity[i]
                
            #evaluate fitness
            current_score = rail_network.get_score()
            
            #update particle best
            if current_score > particle.best_score:
                particle.best_position = copy.deepcopy(particle.position)
                particle.best_score = current_score
                
                #update global best 
                if current_score > global_best_particle.best_score:
                    global_best_particle = copy.deepcopy(particle)
                    
    #after all iterations, return the best particle
    return global_best_particle

if __name__ == "__main__":
    particle_swarm_optimization(10, 10).print_output()
    
   