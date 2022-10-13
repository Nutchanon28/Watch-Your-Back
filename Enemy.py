class Enemy:
    def __init__(self, x, y, x_change, y_change, image, state, index, health, just_spawned):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.image = image
        self.state = state
        self.index = index
        self.health = health
        self.max_health = health
        self.just_spawned = just_spawned


    def reset_health(self):
        self.health = self.max_health