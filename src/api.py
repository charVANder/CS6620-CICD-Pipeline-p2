'''This will hold the REST API routes for the app.
Basically the api stuff separate from the pokemon stuff from the last assignment.
I am planning to just use my original constructor from the last assignment.
(doing it this way ended up taking longer than I thought, lol. Next time I will just start from scratch)
'''
from flask import Flask, jsonify, request
from pokemon import Pokemon

pokemon_storage = {} # creating in-memory pokemon storage (not using a database bc this is a simpler assignment)
next_id = 1

def create_app():
    app = Flask(__name__)
    init_data() # intializing the pokemon storage w/ sample data

    ## Creating some other functions to help make this smoother
    def find_pkmn_by_id(pokemon_id):
        return pokemon_storage.get(pokemon_id)

    def validate_pkmn_data(data): # adding extra validation (will also have test_api.py)
        required_stuff = ["name", "level"]
        for stuff in required_stuff:
            if stuff not in data:
                return False, f"Missing {stuff}"
            
        if not isinstance(data["name"], str) or len(data["name"].strip()) == 0:
            return False, f"Name needs to be a non-empty string"
        
        if not isinstance(data["level"], int) or data["level"] < 1 or data["level"] > 100:
            return False, f"Level needs to be b/w 1 and 100"
        
        return True, "" # It took FOREVER to realize I forgot this line... 0_o
            
    def convert_to_dict(pokemon, pokemon_id):
        '''Will convert original pkmn to dict for JSON
        '''
        return {
            "id": pokemon_id,
            "name": pokemon.name,
            "hp": pokemon.hp,
            "max_hp": pokemon.max_hp,
            "fainted": pokemon.fainted,
            "level": getattr(pokemon, 'level', 1), # default if not set
            "type": getattr(pokemon, 'type', 'Normal') # default if not set
        }

    ## Routes
    @app.route("/health", methods=["GET"])
    def check_health():
        return jsonify({"Status": "healthy", "Note": "The Pokemon API is running"}), 200
    
    @app.route("/pokemon", methods=["GET"])
    def get_all_pkmn():
        '''To retrieve all pokemon
        '''
        pkmn_list = []
        for pokemon_id, pokemon in pokemon_storage.items():
            pkmn_list.append(convert_to_dict(pokemon, pokemon_id))

        return jsonify({
            "pokemon": pkmn_list,
            "count": len(pkmn_list)
        }), 200
    
    @app.route("/pokemon/<int:pokemon_id>", methods=["GET"])
    def get_pokemon(pokemon_id):
        '''To retrieve a specific pokemon by their id
        '''
        pokemon = find_pkmn_by_id(pokemon_id)
        if pokemon is None:
            return jsonify({"Error": f"Pokemon with ID {pokemon_id} was not found"}), 404
        return jsonify(convert_to_dict(pokemon, pokemon_id)), 200
    
    @app.route("/pokemon", methods=["POST"])
    def create_pokemon():
        '''Creating a pkmn. I'm using my old constructor
        '''
        global next_id
        if not request.is_json:
            return jsonify({"Error": f"Request must be JSON"}), 400
        data = request.get_json()

        is_valid, error_message = validate_pkmn_data(data)
        if not is_valid:
            return jsonify({"Error": error_message}), 400
        
        max_hp = data.get("max_hp", 50 + (data["level"] * 2)) # for simplicity, I made up an easy way to calculate max_hp
        pokemon = Pokemon(data["name"], max_hp) # using old constructor
        pokemon.level = data["level"] # adding the other attributes
        pokemon.type = data.get("type", "Normal")
        pokemon_storage[next_id] = pokemon
        result = convert_to_dict(pokemon, next_id)
        next_id += 1
        return jsonify(result), 201
    
    @app.route("/pokemon/<int:pokemon_id>", methods=["PUT"])
    def update_pokemon(pokemon_id):
        '''Updating a pkmn by ID
        '''
        pokemon = find_pkmn_by_id(pokemon_id)
        if pokemon is None:
            return jsonify({"Error": f"Pokemon with ID {pokemon_id} was not found"}), 404
        if not request.is_json:
            return jsonify({"Error": f"Request must be JSON"}), 400
        data = request.get_json()
        is_valid, error_message = validate_pkmn_data(data)
        if not is_valid:
            return jsonify({"Error": error_message}), 400

        # updating using the original attributes
        pokemon.name = data["name"].strip()
        pokemon.level = data["level"]
        if "type" in data:
            pokemon.type = data["type"]

        return jsonify(convert_to_dict(pokemon, pokemon_id)), 200
    
    @app.route("/pokemon/<int:pokemon_id>", methods=["DELETE"])
    def delete_pokemon(pokemon_id):
        '''Deletes a pokemon by their id
        '''
        if pokemon_id not in pokemon_storage:
            return jsonify({"Error": f"Pokemon with ID {pokemon_id} not found"}), 404
        deleted_pkmn = pokemon_storage.pop(pokemon_id)
        return jsonify({"Note": f"Pokemon '{deleted_pkmn.name}' with ID {pokemon_id} has been deleted"}), 200
    
    ## Creating more routes to make use of my old pokemon methods (this took longer than I thought...might not be necessary next time :p)
    @app.route("/pokemon/<int:pokemon_id>/attack", methods=["POST"])
    def pokemon_attack(pokemon_id):
        pokemon = find_pkmn_by_id(pokemon_id)
        if pokemon is None:
            return jsonify({"Error": f"Pokemon with ID {pokemon_id} was not found"}), 404
        if pokemon.fainted:
            return jsonify({"Error": f"{pokemon.name} has fainted and cannot attack"}), 400
        if not request.is_json:
            return jsonify({"Error": f"Request must be JSON"}), 400
        data = request.get_json()
        if "attack_name" not in data or "damage" not in data:
            return jsonify({"Error": f"Missing 'attack_name' and/or 'damage'"}), 400
        
        attack_result = pokemon.attack(data["attack_name"], data["damage"])
        return jsonify({
            "Note": attack_result,
            "pokemon": convert_to_dict(pokemon, pokemon_id)
        }), 200
    
    @app.route("/pokemon/<int:pokemon_id>/damage", methods=["POST"])
    def pokemon_take_damage(pokemon_id):
        '''Using take_damage method to take damage
        '''
        pokemon = find_pkmn_by_id(pokemon_id)
        if pokemon is None:
            return jsonify({"Error": f"Pokemon with ID {pokemon_id} was not found"}), 404
        if not request.is_json:
            return jsonify({"Error": f"Request must be JSON"}), 400
        data = request.get_json()
        if "amount" not in data:
            return jsonify({"Error": f"Missing 'amount'"}), 400
        if not isinstance(data["amount"], int) or data["amount"] < 0:
            return jsonify({"Error": f"Damage must be a non-negative integer"}), 400
        
        pokemon.take_damage(data["amount"])
        message = f"{pokemon.name} took {data['amount']} damage"
        if pokemon.fainted:
            message += f" and has fainted! :("

        return jsonify({
            "Note": message,
            "pokemon": convert_to_dict(pokemon, pokemon_id)
        }), 200
    
    @app.route("/pokemon/<int:pokemon_id>/heal", methods=["POST"])
    def pokemon_heal(pokemon_id):
        '''Uses old heal method to heal
        '''
        pokemon = find_pkmn_by_id(pokemon_id)
        if pokemon is None:
            return jsonify({"Error": f"Pokemon with ID {pokemon_id} was not found"}), 404
        if pokemon.fainted:
            return jsonify({"Error": f"{pokemon.name} has fainted and cannot be healed"}), 400
        if not request.is_json:
            return jsonify({"Error": f"Request must be JSON"}), 400
        data = request.get_json()
        if "amount" not in data:
            return jsonify({"Error": f"Missing 'amount'"}), 400
        if not isinstance(data["amount"], int) or data["amount"] < 0:
            return jsonify({"Error": f"Heal amount must be a non-negative integer"}), 400
        
        old_hp = pokemon.hp
        pokemon.heal(data["amount"])
        healing = pokemon.hp - old_hp

        return jsonify({
            "Note": f"{pokemon.name} was healed for {healing} HP",
            "pokemon": convert_to_dict(pokemon, pokemon_id)
        }), 200
    
    return app

def init_data():
    '''Sample data will just be 3 simple pokemon that most people know
    '''
    global pokemon_storage, next_id
    
    pikachu = Pokemon("Pikachu", 100)
    pikachu.level = 25
    pikachu.type = "Electric"
    pokemon_storage[1] = pikachu

    charizard = Pokemon("Charizard", 150)
    charizard.level = 50 
    charizard.type = "Fire"
    pokemon_storage[2] = charizard
    
    blastoise = Pokemon("Blastoise", 140)
    blastoise.level = 45
    blastoise.type = "Water"
    pokemon_storage[3] = blastoise

    next_id = 4