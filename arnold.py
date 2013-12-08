# Arnold
# Team 1
# London Python Dojo

import rg
from random import choice


def adjacent(game, location):
    locations = rg.locs_around(location)
    robots = []
    for place in locations:
        try:
            robots.append(game.robots[place])
        except KeyError:
            pass
    return robots


def friend_adjacent(game, location):
    robots = adjacent(game, location)
    return any(hasattr(r, "robot_id") for r in robots)


def enemy_adjacent(game, location):
    robots = adjacent(game, location)
    return any(not hasattr(r, "robot_id") for r in robots)


class Robot:
    def __init__(self):
        self.mayday = {}
    
    def kill_self(self, game):
        if self.robot_id in self.mayday:
            del self.mayday[self.robot_id]
        if enemy_adjacent(game, self.location) and not friend_adjacent(game, self.location):
            return ("suicide", )
        if friend_adjacent(game, self.location):
            locations = rg.locs_around(self.location, ("obstacle"))
            for place in locations:
                if enemy_adjacent(game, place) and not friend_adjacent(game, place):
                    return "move", place
            return "move", choice(locations)
        return ("suicide", )

    def act(self, game):
        if self.robot_id in self.mayday:
            del self.mayday[self.robot_id]
        
        if self.hp < 10:
            return self.kill_self(game)

        enemies = []
        friends = []

        for robot in game.robots.itervalues():
            if hasattr(robot, "robot_id"):
                friends.append(robot)
            else:
                enemies.append(robot)

        targets = []
        for enemy in enemies:
            targets.append((enemy, rg.wdist(self.location, enemy.location)))

        target, distance = min(targets, key=lambda (a, b): b)

        if distance == 1:
            self.mayday[self.robot_id] = target.location
            return ["attack", target.location]
        if self.mayday:
            targets = [(t, rg.wdist(self.location, t)) for t in self.mayday.values()]
            target, _ = min(targets, key=lambda (a, b): b)
            if rg.wdist(self.location, target) == 1:
                return ["attack", target]
            return ["move", rg.toward(self.location, target)]
        return ["move", rg.toward(self.location, target.location)]
