'''
I'm using pokemon as my example. Why? Because I like pokemon, lol. Just a simplified battle simulation class with attacking/healing. No types or special moves.
'''
class Pokemon:
    def __init__(self, name, max_hp):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.fainted = False

    def take_damage(self, amount):
        '''Take away hp when pkmn takes damage
        '''
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.fainted = True

    def heal(self, amount):
        '''Healing! Can go up to maxhp
        '''
        if not self.fainted:
            self.hp = min(self.max_hp, self.hp + amount)

    def attack(self, attack_name, damage):
        '''Attacking with a move! Keeping things basic
        '''
        return f"{self.name} used {attack_name}. It caused {damage} damage!"