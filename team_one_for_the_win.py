import rg

class Robot:

    def act(self, game):
        enemies = []
        friends = []
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                enemies.append(bot)
            else:
                friends.append(bot)

        enemies_distances = dict()
        for enemy in enemies:
            enemies_distances[enemy.location] = [0, enemy]
            for friend in friends:
                enemies_distances[enemy.location][0] += rg.dist(friend.location, enemy.location)

        closest_enemies = sorted(enemies_distances.items(), key=lambda x: x[1][0])
        closest_enemies = closest_enemies[:len(closest_enemies)/2]

        # if there are enemies around, attack them
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]

        loc, (distance, closest_enemy) = closest_enemies[0]
        closest_enemy = closest_enemies[0][1][1]
        for loc, (distance, enemy) in closest_enemies:
            if rg.dist(enemy.location, self.location) < rg.dist(closest_enemy.location, self.location):
                closest_enemy = enemy

        return ['move', rg.toward(self.location, closest_enemy.location)]

