import rg
import random

TOP = (9, 2)

class Robot:
    def act(self, game):
        if self.hp <= 10:
            return ['suicide']
        
        try:
            return self.attack(game)
        except ValueError:
            pass
        
        try:
            if game.turn < 70:
                return self.move_northish(game)
            else:
                return self.move_southish(game)
        except ValueError:
            return self.act_random(game)
    
    def move_random(self, game, accept_locations=lambda x: True):
        adj = rg.locs_around(self.location, filter_out=['invalid', 'spawn', 'obstacle'])
        adj = filter(accept_locations, adj)
        
        if not adj:
            raise ValueError("Nowhere to move")
        move = random.choice(adj)

        # move toward the center
        return ['move', move]
    
    def move_northish(self, game):
        if self.location == TOP:
            return self.act_random(game)
        return ['move', rg.toward(self.location, TOP)]
    
    def move_southish(self, game):
        return self.move_random(game, lambda l: l[1] == self.location[1] + 1)
    
    def attack(self, game):
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]
        raise ValueError('Nothing to attack')
    
    def act_random(self, game):
        try:
            return self.move_random(game)
        except ValueError:
            return ['guard']

