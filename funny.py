import rg

class Robot:
    def act(self, game):
        our_locations = [x["location"] for x in game['robots'].itervalues() if x.get('robot_id')]
        avg_robot_x = 0
        avg_robot_y = 0
        n_robots = 0
        for x,y in our_locations:
            avg_robot_x += x
            avg_robot_y += y
            n_robots += 1
        avg_robot_x = avg_robot_x / n_robots
        avg_robot_y = avg_robot_y / n_robots
        my_x, my_y = self.location
        delta_x = avg_robot_x - my_x
        delta_y = avg_robot_y - my_y
        if abs(delta_x) > abs(delta_y):
            return ['move', (my_x + (1 if delta_x > 0 else -1 ), my_y)]
        else:
            return ['move', (my_x, my_y + (1 if delta_y > 0 else -1))]
