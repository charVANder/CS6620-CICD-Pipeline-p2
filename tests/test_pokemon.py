'''
This is the test script for the pokemon.py. Will use simple tests such as testing damage, fainting, healing, healing more than needed, and attacking.
'''
from pokemon import Pokemon

def test_taking_damage():
    '''Creating a pokemon, taking damage, and seeing if its the correct number. I'm going simple with my choices of pkmn.
    '''
    charmander = Pokemon("Charmander", 100)
    charmander.take_damage(99)
    assert charmander.hp == 1

def test_fainting():
    ''' Bulbasaur's turn. Pokemon should faint if their hp hits 0
    '''
    bulbasaur = Pokemon("Bulbasaur", 100)
    bulbasaur.take_damage(100)
    assert bulbasaur.hp == 0
    assert bulbasaur.fainted == True

def test_healing():
    '''Now it's Squirtle's turn. Time to see if healing gives the right hp.
    '''
    squirtle = Pokemon("Squirtle", 100)
    squirtle.take_damage(50)
    squirtle.heal(20)
    assert squirtle.hp == 70

def test_healing_over():
    '''Also need to make sure that healing doesn't go over the max hp of the pkmn
    '''
    squirtle = Pokemon("Squirtle", 100)
    squirtle.heal(20)
    assert squirtle.hp == 100

def test_attack():
    '''Testing an attack. Why Absol you say? Because I think he's cool :p
    '''
    absol = Pokemon("Absol", 100) # i love absol <3
    attack = absol.attack("Night Slash", 85)
    assert attack == "Absol used Night Slash. It caused 85 damage!"