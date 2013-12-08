import rg
import random

one = 0

class Robot:
    def act(self, game):
        enemies = []
        friends = []
        for location, robot in game.robots.items():
            if robot['player_id'] != self.player_id:
                enemies.append(location)
            else:
                friends.append(location)
 
        nearby_bad_guys = 0
        last_bad_guy = None
        around = rg.locs_around(self.location, filter_out=('invalid', 'obstacle', 'spawn'))
        for loc in around:
            if loc in enemies:
                nearby_bad_guys += 1
                last_bad_guy = loc

        if nearby_bad_guys > 2:
            return ['suicide']
        elif last_bad_guy:
            return ['attack', last_bad_guy]
        else:
            return ['move', random.choice(around)]
