import os
import random
import pyray

class Point:    
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def add(self, other):
        x = self._x + other.get_x()
        y = self._y + other.get_y()
        return Point(x, y)

    def equals(self, other):
        return self._x == other.get_x() and self._y == other.get_y()

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def scale(self, factor):
        return Point(self._x * factor, self._y * factor)
class Color:   
    def __init__(self, red, green, blue, alpha = 255):
        self._red = red
        self._green = green
        self._blue = blue 
        self._alpha = alpha

    def to_tuple(self):
        return (self._red, self._green, self._blue, self._alpha)  
class VideoService:
    def __init__(self, caption, width, height, cell_size, frame_rate, debug = False):
        self._caption = caption
        self._width = width
        self._height = height
        self._cell_size = cell_size
        self._frame_rate = frame_rate
        self._debug = debug

    def close_window(self):
        pyray.close_window()

    def clear_buffer(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        if self._debug == True:
            self._draw_grid()
    
    def draw_actor(self, actor): 
        text = actor.get_text()
        x = actor.get_position().get_x()
        y = actor.get_position().get_y()
        font_size = actor.get_font_size()
        color = actor.get_color().to_tuple()
        pyray.draw_text(text, x, y, font_size, color)
        
    def draw_actors(self, actors): 
        for actor in actors:
            self.draw_actor(actor)
    
    def flush_buffer(self):
        pyray.end_drawing()

    def get_cell_size(self):
        return self._cell_size

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def is_window_open(self):
        return not pyray.window_should_close()

    def open_window(self):
        pyray.init_window(self._width, self._height, self._caption)
        pyray.set_target_fps(self._frame_rate)

    def _draw_grid(self):
        for y in range(0, self._height, self._cell_size):
            pyray.draw_line(0, y, self._width, y, pyray.GRAY)
        for x in range(0, self._width, self._cell_size):
            pyray.draw_line(x, 0, x, self._height, pyray.GRAY)
class KeyboardService:
    
    def __init__(self, cell_size = 1):
        self._cell_size = cell_size

    def get_direction(self):
        dx = 0
        dy = 0

        if pyray.is_key_down(pyray.KEY_LEFT):
            dx = -1
        
        if pyray.is_key_down(pyray.KEY_RIGHT):
            dx = 1
        
        if pyray.is_key_down(pyray.KEY_UP):
            dy = -1
        
        if pyray.is_key_down(pyray.KEY_DOWN):
            dy = 1

        direction = Point(dx, dy)
        direction = direction.scale(self._cell_size)
        
        return direction
class Actor:
    def __init__(self):
        self._text = ""
        self._font_size = 15
        self._color = Color(255, 255, 255)
        self._position = Point(0, 0)
        self._velocity = Point(0, 0)
        self._score = 0

    def get_color(self):
        return self._color

    def get_font_size(self):
        return self._font_size

    def get_position(self):
        return self._position
    
    def get_text(self):
        return self._text

    def get_velocity(self):
        return self._velocity
    
    def move_next(self, max_x, max_y):
        x = (self._position.get_x() + self._velocity.get_x()) % max_x
        y = 570 #(self._position.get_y() + self._velocity.get_y()) % max_y
        self._position = Point(x, y)

    def set_color(self, color):
        self._color = color

    def set_position(self, position):
        self._position = position
    
    def set_font_size(self, font_size):
        self._font_size = font_size
    
    def set_text(self, text):
        self._text = text

    def set_velocity(self, velocity):
        self._velocity = velocity

    def get_score(self):
        return self._score

    def set_score(self, score):
        self._score = score

    def gottem(self, x):
        if x == 0:
            self._score = self._score - 1
        elif x == 1:
            self._score = self._score + 1 
class Artifact(Actor):
    def __init__(self):
        super().__init__()
        self._message = ""
        self._identity = ""
        
    def get_message(self):
        return self._message
    
    def set_message(self, message):
        self._message = message

    def set_identity(self, x):
        self._identity = x

    def get_identity(self):
        return self._identity
    
    def drop(self):
        self._position._y += 1
class Cast:
    def __init__(self):
        self._actors = {}
        
    def add_actor(self, group, actor):
        if not group in self._actors.keys():
            self._actors[group] = []
            
        if not actor in self._actors[group]:
            self._actors[group].append(actor)

    def get_actors(self, group):
        results = []
        if group in self._actors.keys():
            results = self._actors[group].copy()
        return results
    
    def get_all_actors(self):
        results = []
        for group in self._actors:
            results.extend(self._actors[group])
        return results

    def get_first_actor(self, group):
        result = None
        if group in self._actors.keys():
            result = self._actors[group][0]
        return result

    def remove_actor(self, group, actor):
        if group in self._actors:
            self._actors[group].remove(actor)
class Gem(Artifact):
    
    def __init__(self):
        super().__init__()
        self.frame_counter= 0
        self.artifacts =[]
        
    def gem_drop(self):
        self.frame_counter = self.frame_counter + 1
        if self. frame_counter>= 120:
            #reset frame counter back to 0
            self.frame_counter = 0 
            new_artifact= Artifact()
            new_artifact.position= (random.randint(0,1024), 768)
            self.artifacts.apend(new_artifact)
            for artifact in list(self.artifacts):
                artifact.position= (artifact.position.x, artifact.position.y -2)
                if artifact.position.y < -100:
                    self.artifacts.remove(artifact)
                if artifact.bbox.intersects(self.player.bbox):
                    self.artifacts.remove(artifact)
class Director:
    def __init__(self, keyboard_service, video_service):
        self._keyboard_service = keyboard_service
        self._video_service = video_service

    def start_game(self, cast):
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)        

    def _do_updates(self, cast):        
        actor = Actor()
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")   

        banner.set_text("Score: " + str(robot.get_score()))
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)
        
        for artifact in artifacts:
            artifact.drop()
            if robot.get_position().equals(artifact.get_position()):
                robot.gottem((artifact.get_identity()))
                #cast.remove_actor(group, actor)
                
    def _do_outputs(self, cast):
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()

FRAME_RATE = 11
MAX_X = 900
MAX_Y = 600
CELL_SIZE = 15
FONT_SIZE = 30
COLS = 60
ROWS = 40
CAPTION = "Be Greedy"
DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/data/messages.txt"
WHITE = Color(255, 255, 255)
DEFAULT_ARTIFACTS = 100


def main():
    
    # create the cast
    cast = Cast()
    
    # create the banner
    banner = Actor()
    banner.set_text("")
    banner.set_font_size(FONT_SIZE)
    banner.set_color(WHITE)
    banner.set_position(Point(CELL_SIZE, 0))
    cast.add_actor("banners", banner)
    
    # create the robot
    x = int(MAX_X / 2)
    y = int(550)
    position = Point(x, y)

    robot = Actor()
    robot.set_text("#")
    robot.set_font_size(FONT_SIZE)
    robot.set_color(WHITE)
    robot.set_position(position)
    cast.add_actor("robots", robot)
    
    # create the artifacts    
    for n in range(DEFAULT_ARTIFACTS):
        
        x = random.randint(1, COLS - 1)
        #y = random.randint(1, ROWS - 1)
        y = random.randint(1,20)
        
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        
        rocks = Artifact()
        rocks.set_text("o")
        rocks.set_font_size(FONT_SIZE)
        rocks.set_color(color)
        rocks.set_position(position)
        rocks.set_message("-100")
        rocks.set_identity(0)
        cast.add_actor("artifacts", rocks)
        
    for n in range(DEFAULT_ARTIFACTS):

        x = random.randint(1, COLS - 1)
        #y = random.randint(1, ROWS - 1)
        y = random.randint(1,15)
    
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        
        gem = Artifact()
        gem.set_text("*")
        gem.set_font_size(FONT_SIZE)
        gem.set_color(color)
        gem.set_position(position)
        gem.set_message("+100")
        gem.set_identity(1)
        cast.add_actor("artifacts", gem)
    
    # start the game
    keyboard_service = KeyboardService(CELL_SIZE)
    video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)


if __name__ == "__main__":
    main()