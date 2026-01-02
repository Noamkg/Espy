from interfaces.button_parser import voltage_to_value

LEFT_WALL = 0
RIGHT_WALL = 1 

class Shape:
    def __init__(self):
        pass
    def next(self):
        pass
    def draw(self, oled):
        pass


class Rectangle(Shape):
    def __init__(self, x = 0, y = 0, width = 10, height = 10, x_velocity = 0, y_velocity = 0, color = 1, fill = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.color = color
        self.center_x = self.x + self.width / 2
        self.center_y = self.y + self.height / 2
        self.round_end = False
        self.idle = False
    
    def next(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        #print(self.y_velocity)
        self.center_x = self.x + self.width / 2
        self.center_y = self.y + self.height / 2
        # print(f"location: ({self.x}, {self.y})")
    
    def flip_x(self):
        self.x_velocity *= -1
        
    def flip_y(self):
        self.y_velocity *= -1
    
    def draw(self, oled):
        oled.framebuf.rect(int(self.x), int(self.y), self.width, self.height, self.color, self.fill)
    
    def collision(self, rectangle):
        x_distance = abs(self.center_x - rectangle.center_x)
        y_distance = abs(self.center_y - rectangle.center_y)
        x_min_length = self.width / 2 + rectangle.width / 2
        y_min_length = self.height / 2 + rectangle.height / 2
        #print(f"Checking Collosions\ndistance: ({x_distance}, {y_distance})\tmin_length: ({x_min_length}, {y_min_length})")
        #if self.y_velocity == 1:
        #    print(f"My locations: {(self.center_x, self.center_y)}\t other: {rectangle.center_x, rectangle.center_y}")
        #    print(f"Checking Collosions\ndistance y: {y_distance}\tmin_length: {y_min_length}")
        if x_distance <= x_min_length and y_distance <= y_min_length:
            if abs(x_min_length - x_distance) < abs(y_min_length - y_distance):
         #       print("X Collision")
                self.flip_x()
            else:
          #      print("Y Collision")
                self.flip_y()
    
    def bound_collision(self, bounds_width, bounds_height):
        if self.x <= 0 or self.x + self.width >= bounds_width:
            self.flip_x()
        if self.y <= 0 or self.y + self.height >= bounds_height:
            self.flip_y()
        

class Player(Rectangle):
    def collision(self, other):
        pass
    
    def register_button_pads(self, buttons):
        self.buttons = buttons

    def idle_next(self, bounds_height):
        print("hello")
        print(self.y)
        if self.y <= 0:
            self.y_velocity = 2
        if self.y + self.height >= bounds_height:
            self.y_velocity = -2
        super().next()

    def next(self):
        if voltage_to_value(self.buttons.read()) == 2:  # Down Button Pressed
            self.y_velocity = -2
        if voltage_to_value(self.buttons.read()) == 3:  # Up Button Pressed
            self.y_velocity = 2
        if voltage_to_value(self.buttons.read()) == 0:  # No Button Pressed
            self.y_velocity = 0
        super().next()
        
    def bound_collision(self, bounds_width, bounds_height):
        if self.x <= 0 or self.x + self.width >= bounds_width:
            self.x_velocity = 0
        if self.y <= 0 or self.y + self.height >= bounds_height:
            self.y_velocity = 0
   

class Ball(Rectangle):
    def bound_collision(self, bounds_width, bounds_height):
        if self.x <= 0:
            self.x_velocity = 0
            self.y_velocity = 0
            self.round_end = 1
            self.collision_wall = LEFT_WALL
        if self.x + self.width >= bounds_width:
            self.x_velocity = 0
            self.y_velocity = 0
            self.round_end = 1
            self.collision_wall = RIGHT_WALL
        if self.y <= 0 or self.y + self.height >= bounds_height:
            self.flip_y()