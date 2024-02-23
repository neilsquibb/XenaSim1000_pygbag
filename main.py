import pgzrun
import os
from pygame.transform import flip
from pgzhelper import *

# GAME WINDOW OBJECTS & GLOBAL VARIABLES
# Game window position on screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game window properties
TITLE = "Xena Simulator 1000"
WIDTH = 1200
HEIGHT = 800
    
# ARENA CLASSES
# Arena parent class
class Block(Actor):
    def __init__(self, name, position, tile_pic,):
        super().__init__(tile_pic)
        self.name = name
        self.pos = position
        self.image = tile_pic

# ARENA OBJECTS & GLOBAL VARIABLES
# Border objects & global variables
border = Rect(0, 50, 1200, 700)

# Wall objects & global variables
walls = {
    # Invible wall that stops enemies from passing over the arena halfway
    'wallIvisible' : [(600, 400), "invis_test3"],
    # Regular walls
    'wallLeft' : [(50, 400), "wall1"],
    'wallRight': [(1150, 400), "wall2"],
    'wallTop' : [(600, 100), "wall1"],
    'wallBottom' : [(600, 700), "wall1"],
    'wallCenterTop' : [(600, 300), "wall3"],
    'wallCenterBottom' : [(600, 500), "wall3"],
}

# For loop iterates over walls dictionary and turns it into an object that can build a wall for each entry 
wall_objects = {key: Block(name=key, position=value[0], tile_pic=value[1]) for key, value in walls.items()}

# Converted to list, sliced wallInvisible off list, and converted back to dictionary, so the player doesn't get stopped by invisible wall
walls_list = list(walls.items())
walls_list_sliced = walls_list[1:]
walls_dict_sliced = dict(walls_list_sliced)
wall_objects_sliced = {key: Block(name=key, position=value[0], tile_pic=value[1]) for key, value in walls_dict_sliced.items()}

# ZONE CLASSES
# Zone parent classes
class Zone(Actor):
    def __init__(self, tile_pic, x, y):
        super().__init__(tile_pic)
        self.image = tile_pic
        self.pos = (x, y)

class Bar(Actor):
    def __init__(self, pip_image, zone):
        super().__init__(pip_image)
        self.image = "pipbar6"
        self.pos = (0, 0)
        self.pipbar_state = 6
        self.zone = zone
    
# Zone child classes
class Pipbar(Bar):
    def __init__(self, pip_image, zone):
        super().__init__(pip_image, zone)
        self.pips = ["pipbar0", "pipbar1", "pipbar2", "pipbar3", "pipbar4", "pipbar5", "pipbar6"]
        
        self.alert_sound_played = False
        self.scoff_sound_played = False

    def update(self):
        # Clock ticks for Pipbar
        self.pip_interval = 5.0       
        # If xena inside of Pipbar zone
        if xena.colliderect(self.zone):
            if self.scoff_sound_played == False:
                sounds.scoff.play()
                self.scoff_sound_played = True
            
            self.pip_interval = 1.0
            clock.unschedule(self.pip_remove)
            if self.pipbar_state == 0:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 1:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 2:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 3:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 4:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 5:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 6:
                pass
                
        # If xena outside of Pipbar zone
        else:
            self.scoff_sound_played = False        
            self.pip_interval = 4.0
            clock.unschedule(self.pip_add)        
            if self.pipbar_state == 6:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 5:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 4:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 3:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 2:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 1: 
                clock.schedule(self.pip_remove, self.pip_interval)
                if self.alert_sound_played == False and game_state.game_over == False:
                    sounds.alert.play(-1)
                    self.alert_sound_played = True
            if self.pipbar_state == 0:
                sounds.alert.stop()
                self.alert_sound_played = False
                
    # Add and remove pips from Pipbar
    def pip_add(self):
        if self.pipbar_state < 6:
            self.pipbar_state += 1
        self.image = self.pips[self.pipbar_state]
        clock.unschedule(self.pip_add)

    def pip_remove(self):
        if self.pipbar_state > 0:
            self.pipbar_state -= 1
        self.image = self.pips[self.pipbar_state]
        clock.unschedule(self.pip_remove)

class Poopbar(Bar):
    def __init__(self, pip_image, zone):
        super().__init__(pip_image, zone)
        self.pips = ["poopbar0", "poopbar1", "poopbar2", "poopbar3", "poopbar4", "poopbar5", "poopbar6", "poopbar7"]
        self.image = pip_image
        self.pipbar_state = 0
        self.scale = 1
        self.alert_sound_played = False

    def update(self):
        # Clock ticks for Poopbar
        self.pip_interval = 3.0
        if self.pipbar_state == 0:
            clock.schedule(self.pip_add, self.pip_interval)
        if self.pipbar_state == 1:
            clock.schedule(self.pip_add, self.pip_interval)
        if self.pipbar_state == 2:
            clock.schedule(self.pip_add, self.pip_interval)
        if self.pipbar_state == 3:
            clock.schedule(self.pip_add, self.pip_interval)
        if self.pipbar_state == 4:
            clock.schedule(self.pip_add, self.pip_interval)
        if self.pipbar_state == 5:
            clock.schedule(self.pip_add, self.pip_interval)
        if self.pipbar_state == 6:
            clock.schedule(self.pip_add, self.pip_interval)
            if self.alert_sound_played == False and game_state.game_over == False:
                sounds.alert.play(-1)
                self.alert_sound_played = True            
        if self.pipbar_state == 7:
            sounds.alert.stop()
            self.alert_sound_played = False  
                
    # Add pips from Poopbar
    def pip_add(self):
        if self.pipbar_state < 7:
            self.pipbar_state += 1
        self.image = self.pips[self.pipbar_state]
        clock.unschedule(self.pip_add)

    def pip_reset(self):
        self.pipbar_state = 0
        self.scale = self.scale

class Speedbar(Bar):
    def __init__(self, pip_image, zone):
        super().__init__(pip_image, zone)
        self.pips = ["speedbar0", "speedbar1", "speedbar2", "speedbar3", "speedbar4", "speedbar5", "speedbar6"]
        self.image = "speedbar6"
        self.scoff_sound_played = False

    def update(self):
        # Clock ticks for Speedbar
        self.pip_interval = 3.0       
        # If xena inside of Speedbar zone
        if xena.colliderect(self.zone):
            if self.scoff_sound_played == False:
                sounds.scoff.play()
                self.scoff_sound_played = True
        
            self.pip_interval = 0.5
            clock.unschedule(self.pip_remove)
            if game_state.game_over == False:
                score.score += 1/60
            if self.pipbar_state == 0:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 1:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 2:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 3:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 4:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 5:
                clock.schedule(self.pip_add, self.pip_interval)
            if self.pipbar_state == 6:
                pass
        # If xena outside of Speedbar zone
        else:
            self.scoff_sound_played = False   
            self.pip_interval = 10.0
            clock.unschedule(self.pip_add)        
            if self.pipbar_state == 6:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 5:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 4:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 3:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 2:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 1:
                clock.schedule(self.pip_remove, self.pip_interval)
            if self.pipbar_state == 0:
                pass
                
    # Add and remove pips from Speedbar
    def pip_add(self):
        if self.pipbar_state < 6:
            self.pipbar_state += 1
            xena.speed += 1
        self.image = self.pips[self.pipbar_state]
        clock.unschedule(self.pip_add)

    def pip_remove(self):
        if self.pipbar_state > 0:
            self.pipbar_state -= 1
            xena.speed -= 1
        self.image = self.pips[self.pipbar_state]
        clock.unschedule(self.pip_remove)

# ZONE OBJECTS & GLOBAL VARIABLES
bed = Zone("bed", 100, 125) # top left
bed_speedbar = Speedbar("speedbar6", bed)
bed_speedbar.pos = (100, 80)

food = Zone("food", 1100, 125) # top right
food_pipbar = Pipbar("pipbar6", food)
food_pipbar.pos = ((WIDTH - 100), 70)

water = Zone("water", 100, 675) # bottom left
water_pipbar = Pipbar("pipbar6", water)
water_pipbar.pos = ((0 + 100), (HEIGHT - 70))

litter = Zone("litter", 1100, 675) # bottom right
litter_poopbar = Poopbar("poopbar0", litter)
litter_poopbar.pos = ((WIDTH - 100), (HEIGHT - 95))
litter_poopbar.scale = 0.75

# CHARACTER CLASSES
# Character parent class
class Character(Actor):
    def __init__(self, normal, stroke, invulnerable):
        super().__init__(normal)
        self.pos = (0, 0)
        self.x_speed = 10
        self.y_speed = 10
        self.normal = normal
        self.stroke = stroke
        self.invulnerable = invulnerable
    
    def update(self):
        pass

    # Character states
    def state_normal(self):
        self.image = self.normal
        self.scale = self.scale
    
    def state_stroke(self):
        self.image = self.stroke
        self.scale = self.scale
        self.saved_x_speed = self.x_speed
        self.saved_y_speed = self.y_speed
        self.x_speed = 0
        self.y_speed = 0
        clock.schedule_unique(self.state_invulnerable, 3.0)

    def state_invulnerable(self):
        self.image = self.invulnerable
        self.scale = self.scale
        self.x_speed = self.saved_x_speed
        self.y_speed = self.saved_y_speed
        clock.schedule_unique(self.state_normal, 3.0)

# Character child classes
class Player(Character):
    def __init__(self, normal, stroke, invulnerable, scared, dead, x, y):
        super().__init__(normal, stroke, invulnerable)
        self.speed = 10
        self.dead = dead
        self.scared = scared
        self.x = x
        self.y = y
        self.angry_sound_played = False
        
    def update(self):
        super().update()
        # Player movement        
        self.saved_x = self.x
        self.saved_y = self.y
        
        if game_state.game_over == False:

            if not self.image == self.stroke or self.image == self.dead:
                    if keyboard.left or keyboard.a:
                        self.x -= self.speed
                    elif keyboard.right or keyboard.d:
                        self.x += self.speed
                    elif keyboard.up or keyboard.w:
                        self.y -= self.speed
                    elif keyboard.down or keyboard.s:
                        self.y += self.speed

            # Player collision with border
            if self.x < 25 or self.x > 1175 or self.y < 75 or self.y > 725:
                self.x = self.saved_x
                self.y = self.saved_y

            # Player collision with walls
            for item in wall_objects_sliced:
                if wall_objects_sliced[item].colliderect(self):
                    self.x = self.saved_x
                    self.y = self.saved_y 
                        
            # Player collision with enemy
            if self.image == self.normal and self.colliderect(neil):
                sounds.stroke.play(3)
                self.state_stroke()
            
            if self.image == self.normal and self.colliderect(april):
                sounds.stroke.play(3)
                self.state_stroke()

            if game_state.game_over == False:
                if neil.image == neil.angry or april.image == april.angry:
                    self.state_scared()
                    clock.schedule(self.state_normal, anger_time)
                    if self.angry_sound_played == False:
                        sounds.angry.play()
                        self.angry_sound_played = True
                else:
                    sounds.angry.stop()
                    self.angry_sound_played = False
            else:
                sounds.angry.stop()
                
            if neil.image == neil.angry and self.colliderect(neil):
                clock.unschedule(self.state_normal)
                clock.unschedule(self.state_scared)
                game_state.game_over = True
                game_state.game_over_type = 1
                sounds.angry.stop()

            if april.image == april.angry and self.colliderect(april):
                clock.unschedule(self.state_normal)
                clock.unschedule(self.state_scared)
                game_state.game_over = True
                game_state.game_over_type = 1
                sounds.angry.stop()
            
    # Player specific states
    def state_scared(self):
        self.image = self.scared
        
    def state_dead(self):
        clock.unschedule(self.state_normal)
        self.image = self.dead
        self.x_speed = 0
        self.y_speed = 0

class Menu_Player(Character):
    def __init__(self, normal, stroke, invulnerable, x, y):
        super().__init__(normal, stroke, invulnerable)
        self.speed = 10
        self.x = x
        self.y = y

    def update(self):
        super().update()
        # Menu_Player movement        
        self.saved_x = self.x
        self.saved_y = self.y


        if not self.image == self.stroke or self.image == self.dead:
                if keyboard.left or keyboard.a:
                    self.x -= self.speed
                elif keyboard.right or keyboard.d:
                    self.x += self.speed
                elif keyboard.up or keyboard.w:
                    self.y -= self.speed
                elif keyboard.down or keyboard.s:
                    self.y += self.speed


class Enemy(Character):
    def __init__(self, normal, stroke, invulnerable, angry):
        super().__init__(normal, stroke, invulnerable)
        self.scale = 1
        self.angry = angry

    def update(self):
        super().update()
        self.x += self.x_speed
        self.y += self.y_speed

        # Enemy collision with wall
        collision_tolerance = 10
        for key in wall_objects.keys():
            if wall_objects[key].colliderect(self):
                if abs(wall_objects[key].top - self.bottom) < collision_tolerance:
                    self.y_speed *= -1
                    sounds.bounce.play()
                if abs(wall_objects[key].bottom - self.top) < collision_tolerance:
                    self.y_speed *= -1
                    sounds.bounce.play()
                if abs(wall_objects[key].right - self.left) < collision_tolerance:
                    self.x_speed *= -1
                    sounds.bounce.play()
                if abs(wall_objects[key].left - self.right) < collision_tolerance:
                    self.x_speed *= -1
                    sounds.bounce.play()

        # Enemy collision with border
        if self.right >= WIDTH or self.left <= 0:
            self.x_speed *= -1

        if self.bottom >= 750 or self.top <= 50:
            self.y_speed *= -1
        
        # Enemy collision with player
        if game_state.game_over == False:

            if not xena.image == xena.invulnerable:
                    if self.image == self.normal and self.colliderect(xena):  
                        self.state_stroke()

        # Enemy state angry if poop not created in litter zone
        if litter_poopbar.image == "poopbar7" and self.image == self.normal:
            if xena.x > 950 and xena.y > 550:
                sounds.poop2.play()
                if game_state.game_over == False:
                    score.score += 50
            else:
                self.state_angry()
                sounds.poop1.play()
                if game_state.game_over == False:
                    score.score -= 25

    # Enemy specific states
    def state_angry(self):
        self.image = self.angry
        clock.schedule(self.speed_down, 8.0)
        clock.schedule_unique(self.state_normal, anger_time)

    def speed_down(self):
        pass

# CHARACTER OBJECTS & GLOBAL VARIABLES
# Player objects & global variables
xena = Player("xena", "xena_stroke", "xena_invulnerable", "xena_scared", "xena_dead", x=100, y=100)

xena_menu = Menu_Player("xena", "xena_stroke", "xena_invulnerable", x=100, y=100)

# Enemies objects & global variables
anger_time = 10.0

neil = Enemy("neil", "neil_stroke", "neil_invulnerable", "neil_angry")
neil.scale = 1.5
neil.pos = (300, 400)
neil.x_speed = 0.75
neil.y_speed = 1.25

april = Enemy("april", "april_stroke", "april_invulnerable", "april_angry")
april.pos = (900, 600)
april.x_speed = 1.875
april.y_speed = 2.5

# EVENT OBJECTS & GLOBAL VARIABLES
poop = Actor("poop", (1000, 675))

# SCORE CLASSES
class Score():
    def __init__(self):
        self.score = 1
        self.prev_highscore = 0

    def update(self):
        self.highscore_read()
        if game_state.game_over == False:
            self.score += 1 / 60

    def draw(self):
        screen.draw.text('Score: ' + str(round(self.score)), center = (600, 25), fontsize = 50, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")
        screen.draw.text('Highscore: ' + str(round(self.prev_highscore)), center = (600, 775), fontsize = 50, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")
        
        if game_state.game_over == True:
            if self.score > self.prev_highscore:
                screen.draw.text('New Highscore!\n' + str(round(self.score)), center = (600, 200), fontsize = 100, color = "yellow", fontname = "munro-small", owidth = 1, ocolor = "black")
                clock.schedule(self.highscore_write, 5.0)

    def highscore_read(self):
        highscore_file = open("highscore.txt", "r")
        for line in highscore_file.readlines():
            self.prev_highscore = int(line)
        highscore_file.close()

    def highscore_write(self):
        if game_state.game_over == True:
            if self.score >= self.prev_highscore:
                highscore_file = open("highscore.txt", "w")
                highscore_file.write(str(round(self.score)))
                highscore_file.close()

# GAME STATE OBJECTS & GLOBAL VARIABLES
score = Score()

# GAME STATE PARENT CLASSES
class GameState():
    def __init__(self):
        self.title_screen = True
        self.title_screen_complete = False

        self.game_running = False
        
        self.game_over = False
        self.game_over_type = 0
        self.game_over_complete = False

        self.spacebar_count = 0
        
        self.game_start_sound_played = False
        self.game_over_sound_played = False
        self.button_sound_played = False

        self.menu_music_played = False
        self.highscore_achieved_music_played = False


    def update(self):
        # Title screen
        if self.title_screen == True:
            if self.menu_music_played == False:
                sounds.menu_music.play(-1)
                self.menu_music_played = True          
        clock.schedule(self.title_screen_complete_check, 5)

        # Game is playing
        if self.game_running == True:
            self.menu_music_played = False
            self.button_sound_played = False
            self.button_sound_played = False

        # Game over screen
        if self.game_over == True:
            xena.state_dead()
            animate(menu_background, tween='linear', duration=3, on_finished=None, pos=(600, 400))
            if self.game_over_sound_played == False:
                sounds.hit.play()
                clock.schedule(game_over_sound, 2)
                self.game_over_sound_played = True
            clock.schedule(self.game_over_complete_check, 5)
        
    def draw(self):
        if self.title_screen == True:
            screen.draw.text("a Neil J Squibb production", center = ((WIDTH / 2), (HEIGHT / 3 - 100)), fontsize = 50, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")
            screen.draw.text("XENA SIMULATOR", center = ((WIDTH / 2), (HEIGHT / 3)), fontsize = 175, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")
            screen.draw.text("1000", center = ((WIDTH / 2), (HEIGHT / 3 + 75)), fontsize = 150, color = "pink", fontname = "munro-small", owidth = 1, ocolor = "black")
            screen.draw.text("beta", center = ((WIDTH / 2), (HEIGHT / 3 + 75)), fontsize = 50, color = "red", fontname = "munro-small", owidth = 1, ocolor = "black")
            screen.draw.text("W = UP, S = DOWN, A = LEFT, D = RIGHT", center = ((WIDTH / 2), (HEIGHT / 3 + 200)), fontsize = 75, color = "lightblue", fontname = "munro-small", owidth = 1, ocolor = "black")
            
        if self.title_screen_complete == True:
            if self.title_screen == True:   
                screen.draw.text("press SPACE to start", center = ((WIDTH / 2), (HEIGHT / 2 + 200)), fontsize = 100, color = "yellow", fontname = "munro-small", owidth = 1, ocolor = "black")

        if self.game_over == True:
            screen.draw.text("GAME OVER", center = ((WIDTH / 2), (HEIGHT / 2 - 15)), fontsize = 150, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")

            # Game over from collision with angry enemy
            if self.game_over_type == 1:
                screen.draw.text("You were beaten to death\nfor pooping on the carpet", center = ((WIDTH / 2), (HEIGHT - 250)), fontsize = 75, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")

            # Game over from hunger
            if self.game_over_type == 2:
                screen.draw.text("You died of starvation\nwith an empty tum", center = ((WIDTH / 2), (HEIGHT - 250)), fontsize = 75, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")
            
            # Game over from thirst
            if self.game_over_type == 3:
                screen.draw.text("You died of thirst\nwith a dry dry tongue", center = ((WIDTH / 2), (HEIGHT - 250)), fontsize = 75, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")

            if self.game_over_type == 4:
                screen.draw.text("Wow,\nyou died of thrist and starvation.\n You are an aweful Xena", center = ((WIDTH / 2), (HEIGHT - 250)), fontsize = 75, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")

            # Placeholder restart note
            if self.game_over_complete == True:
                screen.draw.text("Currently, you must quit and\nrestart the game to try again.\nAn in game restart option will\nbe available in a later version.\nYour highscore will be still be saved.", center = ((WIDTH / 2), (200)), fontsize = 50, color = "yellow", background = "red", fontname = "munro-small", owidth = 1, ocolor = "black")

    def start_game(self):
        self.game_running = True

    def title_screen_complete_check(self):
        self.title_screen_complete = True
        
        if self.title_screen_complete == True:
            if keyboard.space:
                sounds.menu_music.stop()
                animate(menu_background, tween='linear', duration=5, on_finished=None, pos=(600, -900))
                self.title_screen = False
                self.title_screen_complete = False
                self.spacebar_count += 1
                clock.schedule(self.start_game, 4)
                if self.button_sound_played == False:
                    sounds.button.play()
                    self.button_sound_played = True
                if self.game_start_sound_played == False:
                    sounds.game_start.play()
                    self.game_start_sound_played = True
        if self.spacebar_count > 1:
            self.title_screen_complete = False

    def game_over_complete_check(self):
        self.game_over_complete = True


        """if self.game_over_complete == True:
            if keyboard.space:
                self.title_screen = True
                self.title_screen_complete = False
                self.game_running = False
                self.game_over = False
                self.game_over_complete = False
                self.spacebar_count += 1
        if self.spacebar_count > 1:
                self.title_screen = True
                self.title_screen_complete = False
                self.game_running = False
                self.game_over = False
                self.game_over_complete = False"""

    """def highscore_achieved(self):
        if self.highscore_achieved_music_played == False:
            sounds.highscore.play()
            self.highscore_achieved_music_played = True"""
                

# GAME STATE OBJECTS & GLOBAL VARIABLES
game_state = GameState()

menu_background = Actor("menu_background", (600, 400))

# MISC CLOCK FUNCTIONS
def game_over_sound():
    sounds.game_over.play()
    sounds.angry.stop()

# GAME LOOP
# Game loop global functions
def update():
    # Update arena

    # Update zones
    if game_state.game_running == True:
        bed_speedbar.update()
        food_pipbar.update()
        water_pipbar.update()
        litter_poopbar.update()

    # Update characters
    if game_state.game_running == True:
        neil.update()
        april.update()
        xena.update()

    if game_state.title_screen == True:
        xena_menu.update()

    # Update events

    # Update score
    if game_state.game_running == True:
        score.update()

    # Update GameState events
    game_state.update()
    
def draw():
    # Draw game window
    screen.fill((180, 200, 225))
    
    # Draw arena
    screen.draw.rect(border, (0, 0, 0))

    
    for key in wall_objects.keys():
        wall_objects[key].draw()
    
    # Draw zones
    if game_state.game_running == True:
        bed.draw()
        bed_speedbar.draw()
        screen.draw.text("BED", center = ((0 + 100), (0 + 25)), fontsize = 50, color = "black", fontname = "munro-small")

        food.draw()
        screen.blit(flip(food_pipbar._surf, True, False), food_pipbar.topleft)
        screen.draw.text("FOOD", center = ((WIDTH - 100), (0 + 25)), fontsize = 50, color = "black", fontname = "munro-small")

        water.draw()
        water_pipbar.draw()
        screen.draw.text("LITTER", center = ((WIDTH - 100), (HEIGHT - 35)), fontsize = 50, color = "black", fontname = "munro-small")

        litter.draw()
        litter_poopbar.draw()
        screen.draw.text("WATER", center = ((0 + 100), (HEIGHT - 35)), fontsize = 50, color = "black", fontname = "munro-small")

    # Draw enemies
    if game_state.game_running == True:
        neil.draw()
        april.draw()

    # Draw background
    menu_background.draw()

    # Draw player
    if game_state.game_running == True:
        xena.draw()

    if game_state.title_screen == True:
        xena_menu.draw()

    # Draw events
    # Create poop at Xena's position when poopbar is full
    if litter_poopbar.image == "poopbar7":
        poop.pos = ((xena.x + 10), (xena.y +5))
        litter_poopbar.image = "poopbar0"
    if litter_poopbar.pipbar_state == 7:
        poop.draw()
        clock.schedule(litter_poopbar.pip_reset, anger_time)
      
    # Draw events text
    if game_state.game_running == True and game_state.game_over == False:
        if food_pipbar.image == "pipbar1" and not water_pipbar.image == "pipbar1":
            screen.draw.text("!! STARVATION IMMINENT !!", center = ((WIDTH / 2), (HEIGHT / 2 - 15)), fontsize = 100, color = "red", fontname = "munro-small", owidth = 1, ocolor = "black")
            screen.draw.text("get to the food zone\nand get a scoff on", center = ((WIDTH / 2), (HEIGHT - 250)), fontsize = 50, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")
        if water_pipbar.image == "pipbar1" and not food_pipbar.image == "pipbar1":
            screen.draw.text("!! TERMINAL DEHYDRATION\nIMMINENT !!", center = ((WIDTH / 2), (HEIGHT / 2 - 15)), fontsize = 100, color = "red", fontname = "munro-small", owidth = 1, ocolor = "black")
            screen.draw.text("get to the water zone\nand get slurping", center = ((WIDTH / 2), (HEIGHT - 250)), fontsize = 50, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")
        if water_pipbar.image == "pipbar1" and food_pipbar.image == "pipbar1":
            screen.draw.text("!! STARVATION AND\nTERMINAL DEHYDRATION\nIMMINENT !!", center = ((WIDTH / 2), (HEIGHT / 2 - 15)), fontsize = 100, color = "red", fontname = "munro-small", owidth = 1, ocolor = "black")
            screen.draw.text("well...\nguess you're screwed", center = ((WIDTH / 2), (HEIGHT - 250)), fontsize = 50, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")
        else:
            if litter_poopbar.image == "poopbar5" or litter_poopbar.image == "poopbar6" or litter_poopbar.image == "poopbar7":
                screen.draw.text("!! POOP IMMINENT !!", center = ((WIDTH / 2), (HEIGHT / 2 - 15)), fontsize = 100, color = "red", fontname = "munro-small", owidth = 1, ocolor = "black")
                screen.draw.text("get to the litter zone\nready to lay one", center = ((WIDTH / 2), (HEIGHT - 250)), fontsize = 50, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")
            elif neil.image == neil.angry or april.image == april.angry:
                screen.draw.text("!! RUN !!", center = ((WIDTH / 2), (HEIGHT / 2 - 15)), fontsize = 100, color = "red", fontname = "munro-small", owidth = 1, ocolor = "black")
                screen.draw.text("or face their wrath", center = ((WIDTH / 2), (HEIGHT - 250)), fontsize = 50, color = "white", fontname = "munro-small", owidth = 1, ocolor = "black")

    # Draw Score
    if game_state.game_running == True:
        score.draw()
        
    # Draw GameState events
    if game_state.game_over == False:
        if food_pipbar.pipbar_state == 0 and not water_pipbar.pipbar_state == 0:
            game_state.game_over = True
            game_state.game_over_type = 2
        if water_pipbar.pipbar_state == 0 and not food_pipbar.pipbar_state == 0:
            game_state.game_over = True
            game_state.game_over_type = 3
        if water_pipbar.pipbar_state == 0 and food_pipbar.pipbar_state == 0:
            game_state.game_over = True
            game_state.game_over_type = 4

    game_state.draw()

    # Draw version
    screen.draw.text("!!BETA!! file: xenasim1000_betaV0-1, version: beta version 0.1", topleft = (0, 0), fontsize = 25, color = "lightgreen", fontname = "munro-small", owidth = 1, ocolor = "black")

pgzrun.go()