class Bullet:
    def __init__(self, x, y, x_change, y_change, image, state, direction, index, time_when_shoot):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.image = image
        self.state = state
        self.direction = direction
        self.index = index
        self.time_when_shoot = time_when_shoot