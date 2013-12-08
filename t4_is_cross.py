import rg


class Robot:
    def act(self, game):
        ennemies_around = []
        toward_center_location = rg.toward(self.location, rg.CENTER_POINT)
        
        for location, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(location, self.location) <= 1:
                    ennemies_around.append(location)

            if location == toward_center_location:
                if bot.player_id == self.player_id:
                    return ['guard']
                    

        if len(ennemies_around) > 2:
            return ['suicide']
        if len(ennemies_around) > 0:
            return ['attack', ennemies_around[0]]

        for location, bot in game.robots.iteritems():
            if bot.player_id == self.player_id:
                if self.give_way(location, toward_center_location):
                    print location, toward_center_location, self.location
                    return ['guard']

        return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        
        
    def give_way(self, other, toward_center_location):
        x, y = self.location
        x1, y1 = toward_center_location
        if x1 == x:
            return False
        xo, yo = other
        if x1 in [x-1, x+1]:
            return True
        
