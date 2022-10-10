class Enemy:
    def __init__(self, x, y, x_change, y_change, image, state, index, health):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.image = image
        self.state = state
        self.index = index
        self.health = health
        self.max_health = health


    def reset_health(self):
        self.health = self.max_health