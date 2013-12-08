import rg

DESTINATION = (5, 6)

def ideal_destination(current_loc):
    return rg.toward(current_loc, DESTINATION)

class Robot:
    def act(self, game):
        assert len(set(r.player_id for r in game.robots.values())) > 1
        enemies = self.enemies_around_me(game)
        #enemyhp = sum(enemy.hp for enemy in enemies)

        # if we're likely to die anyway, kill ourselves
        if self.hp < 9 * len(enemies):
            return ["suicide"]

        # attack the first weak-looking enemy we can see
        for enemy in enemies:
            if enemy.hp < 10:
                return ["attack", enemy.location]


        # if there are enemies around, attack them
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]

        # if we're at or near the destination, stay put
        if self.location == DESTINATION:
            return ['guard']
        # if we're near the destination and there's a friend there, stay put
        if DESTINATION in game.robots:
            robot_at_destination = game.robots[DESTINATION]
            if robot_at_destination.player_id == self.player_id:
                if rg.wdist(self.location, DESTINATION) == 1:
                    return ['guard']

        # move towarde center
        return self.move(game)#['move', ideal_destination(self.location)]

    def move(self, game):
        our_dest = ideal_destination(self.location)
        for robot in game.robots.values():
	    if robot.player_id == self.player_id and robot.robot_id != self.robot_id:
            	their_dest = ideal_destination(robot.location)
      
            	if their_dest == our_dest:
    		    if self.robot_id % 2 == 0:
                        return ['guard']
         # move toward the center
        return ['move', ideal_destination(self.location)]
  
  
    def robots_around_me(self, game):
        return [robot for robot in game.robots.values() if rg.wdist(self.location, robot.location) == 1]

    def enemies_around_me(self, game):
        return [robot for robot in self.robots_around_me(game) if robot.player_id != self.player_id]

    def friends_around_me(self, game):
        return [robot for robot in self.robots_around_me(game) if robot.player_id == self.player_id]
