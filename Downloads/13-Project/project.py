# Gahee Kim
# Game Project
# Titan Slayer

import arcade
import math

# CONSTANTS
SPRITE_SCALING = 1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Pixels to keep as minimum margin between character and edge of screen
VIEWPORT_MARGIN = 192
RIGHT_MARGIN = 260
TILE_SIZE = 64
SCALED_TILE_SIZE = TILE_SIZE * SPRITE_SCALING
MAP_HEIGHT = 7

# Physics
MOVEMENT_SPEED = 4
JUMP_SPEED = 8
GRAVITY = 0.5
attack_SPEED = 5

def get_map(filename):
    """
    This function loads an array based on a map stored as a list of
    numbers separated by commas.
    """
    # Open the file
    map_file = open(filename)

    # Create an empty list of rows that will hold our map
    map_array = []

    # Read in a line from the file
    for line in map_file:

        # Strip the whitespace, and \n at the end
        line = line.strip()

        # This creates a list by splitting line everywhere there is a comma.
        map_row = line.split(",")

        # The list currently has all the numbers stored as text, and we want it
        # as a number. (e.g. We want 1 not "1"). So loop through and convert
        # to an integer.
        for index, item in enumerate(map_row):
            map_row[index] = int(item)

        # Now that we've completed processing the row, add it to our map array.
        map_array.append(map_row)

    # Done, return the map.
    return map_array


class Enemy(arcade.Sprite):
    """ This class holds enemy information """
    def __init__(self, filename, scale):
        
        # Call Parent Class
        super().__init__(filename, scale)
        self.enemy_sprite = None
        self.enemy_health = 0
        
    def attributes(self, center_x, center_y, change_x, range_x, health):
        """ Controls enemy's mindless movement """
        self.center_x = center_x * SCALED_TILE_SIZE
        self.center_y = center_y * SCALED_TILE_SIZE
        self.change_x = change_x
        self.range_x = range_x
        self.boundary_left = self.center_x - (range_x * SCALED_TILE_SIZE)
        self.boundary_right = self.center_x + (range_x * SCALED_TILE_SIZE)
        self.enemy_health = health
    
    def enemy_update(self):
        """ Updates enemy's movement """
        # If the enemy hit the left boundary, reverse
        if self.left < self.boundary_left:
            self.change_x *= -1
        # If the self hit the right boundary, reverse
        elif self.right > self.boundary_right:
            self.change_x *= -1
            
    def shooting_update(self, player_sprite, bullet_list, frame_count):
        """ Lets enemies shoot at player """
        self.bullet_list = bullet_list
        
        # Bullet comes from enemy's center
        start_x = self.center_x
        start_y = self.center_y
        
        # Bullet aims at player
        dest_x = player_sprite.center_x
        dest_y = player_sprite.center_y
        
        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)        
        
        # Shoot every 150 frames change of shooting each frame
        if frame_count % 150 == 0:
            bullet = arcade.Sprite("sprites/bullet.png", 0.5)
            bullet.center_x = start_x
            bullet.center_y = start_y 
                
            # Angle the bullet sprite
            bullet.angle = math.degrees(angle)
                
            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * 5
            bullet.change_y = math.sin(angle) * 5
    
            self.bullet_list.append(bullet)
            

class MenuView(arcade.View):
    """ Start Menu Application Class """
    def on_draw(self):
        """ Display on screen """
        arcade.start_render()
        
        # Sounds
        # SOURCE: zatplat.com
        self.select = arcade.load_sound("sounds/quick sound.mp3")
        
        # Set image 
        background = arcade.load_texture("sprites/mainscreen.png")
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, background)

    def on_key_press(self, key, modifiers):
        """ When key is pressed, advance to next screen """
        if key == arcade.key.S:
            arcade.play_sound(self.select)
            game_view = GameView()
            self.window.show_view(game_view)
        if key == arcade.key.I:
            arcade.play_sound(self.select)
            instruction_view = InstructionView()
            self.window.show_view(instruction_view)
        
        
class InstructionView(arcade.View):
    """ Instruction Application Class """
    def __init__(self):
        
        # Call parent class
        super().__init__()
        
        # Load instructions
        self.screen = 1
        self.page_1 = arcade.load_texture("bg images/instructions_2.png")
        self.page_2 = arcade.load_texture("bg images/instructions_1.png")
        self.page_3 = arcade.load_texture("bg images/instructions_3.png")
        self.page_4 = arcade.load_texture("bg images/instructions_4.png")
        
        # Sounds
        # SOURCE: zatplat.com
        self.select = arcade.load_sound("sounds/quic sound 2.mp3")        
        
    def on_draw(self):
        """ Draw instruction pages """
        arcade.start_render()
        
        # Control what shows on screen
        if self.screen == 0:
            menu_view = MenuView()
            self.window.show_view(menu_view)            
        if self.screen == 1:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.page_1)
        if self.screen == 2:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.page_2)
        if self.screen == 3:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.page_3)
        if self.screen == 4:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.page_4) 
            
        if self.screen >= 5:
            game_view = GameView()
            self.window.show_view(game_view)        

    def on_key_press(self, key, modifiers):
        """ When key is pressed, advance to next screen """
        if key == arcade.key.RIGHT:
            arcade.play_sound(self.select)
            self.screen += 1
        if key == arcade.key.LEFT:
            arcade.play_sound(self.select)
            self.screen -= 1


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        
        # Reset the viewport
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        
        self.score = 0
        
        self.end_screen = arcade.load_texture("bg images/end_screen.png")
        
        # Sounds
        # SOURCE: zatplat.com
        self.select = arcade.load_sound("sounds/quick sound.mp3")        

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        
        # Draw text
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.end_screen)
        output_total = f"{self.score}"
        arcade.draw_text(output_total, 600, 310, arcade.color.WHITE, 54)        

    def on_key_press(self, key, modifiers):
        """ If the user presses space button, re-start the game. """
        if key == arcade.key.SPACE:
            arcade.play_sound(self.select)
            menu_view = MenuView()
            self.window.show_view(menu_view)
            
            
class GameView(arcade.View):
    """ Game Application """
    def __init__(self):
        
        # Call parent class
        super().__init__()

        # Used for scrolling map
        self.view_left = 0
        self.view_bottom = 0
        
        # Set background and headings
        self.background = arcade.load_texture("sprites/level_1.png")
        self.heart = arcade.load_texture("sprites/heart.png")
        self.score_enemy = arcade.load_texture("sprites/scoretext.png")
        self.bullets_text = arcade.load_texture("sprites/bulletstext.png")
        self.boss_text = arcade.load_texture("sprites/bosstext.png")
        arcade.set_background_color((138, 204, 255))
        
        # Lists
        self.wall_list = arcade.SpriteList()
        self.titan_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.door_opened_list = arcade.SpriteList()
        self.health_potion_list = arcade.SpriteList()
        self.strength_potion_list = arcade.SpriteList()
        self.lava_list = arcade.SpriteList()
        self.gun_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.police_list = arcade.SpriteList()
        self.boss_list = arcade.SpriteList
        
        # PLAYER
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.AnimatedTimeSprite()
        self.attack_list = arcade.SpriteList()
        self.player_sprite.textures = []
        self.player_attack_dmg = 1
        self.player_faces_left = 0
        self.bullet_list = arcade.SpriteList()
        self.bullet_amount = 0
        self.lives = 5
        self.score = 0
        self.attack_cooldown = 0.0
        self.dmg_cooldown = 0.0
        self.potion_time = 0.0
        self.enemies_left = 0
        self.enemy_shoot_cooldown = 0.0
        self.frame_count = 0

        # Set up player
        self.player_sprite.center_x = 4 * SCALED_TILE_SIZE
        self.player_sprite.center_y = -7 * SCALED_TILE_SIZE
        self.player_list.append(self.player_sprite)
        self.player_sprite.textures.append(arcade.load_texture("sprites/spritesheet.png", x = 0, y = 0, width = 64, height = 64))
        
        #---SOUNDS---
        # SOURCE: Super Mario Bros.
        self.coin_sound = arcade.load_sound("sounds/smb_coin.wav")
        self.jump_sound = arcade.load_sound("sounds/smb_jump-small.wav")
        self.getting_gun = arcade.load_sound("sounds/gunget.wav")
        self.game_over = arcade.load_sound("sounds/smb3_player_down.wav")
        self.strength_sound = arcade.load_sound("sounds/smb3_power-up.wav") 
        self.health_sound = arcade.load_sound("sounds/smw2_1-up.wav") 
        self.pew = arcade.load_sound("sounds/ssbm_peach_05.wav") 
        self.attack_sound = arcade.load_sound("sounds/ssbm_peach_04.wav")
        self.ow = arcade.load_sound("sounds/ssbm_peach_16.wav") 
        self.next_level_sound = arcade.load_sound("sounds/smb2_bonus_chance_start.wav")
        self.boss_sound = arcade.load_sound("sounds/smb2_bonus_chance_win.wav")
        # SOURCE: Minecraft
        self.fire_sound = arcade.load_sound("sounds/fire.ogg")
        self.door_sound = arcade.load_sound("sounds/open2.ogg") ##
        self.titan_hurt_sound = arcade.load_sound("sounds/hurt3.ogg") 
        self.titan_death_sound = arcade.load_sound("sounds/death2.ogg") 
        self.police_hurt_sound = arcade.load_sound("sounds/hurt4.ogg")
        self.police_death_sound = arcade.load_sound("sounds/death5.ogg")
        # SOURCE: zatplat.com
        self.win = arcade.load_sound("sounds/win.mp3")
        
        # Load levels
        self.level = 1
        self.load_level(self.level)
        
    def load_level(self, level):
        """ Create maps based on level """
        #---LEVEL 1---
        if self.level == 1:
            map_array = get_map("maps/level_1.csv")
            
            # Create Enemies
            self.enemies_left = 4
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(14, -7, 1, 2, 6) 
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(22, -6, 1, 1, 6) 
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(39, -7, 1, 2, 6) 
            self.titan_list.append(titan) 
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(50, -10, 1, 4, 6) 
            self.titan_list.append(titan)
            
        #---LEVEL 2 ---
        if self.level == 2:
            map_array = get_map("maps/level_2.csv")
            
            # Create Enemies
            self.enemies_left = 5
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(22, -6, 1, 1, 6)
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(16, -4, 1, 2, 6) 
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(39, -7, 1, 2, 6) 
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(27, -10, 1, 2, 6) 
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(50, -7, 1, 2, 6) 
            self.titan_list.append(titan)          
        
        #---LEVEL 3---
        if self.level == 3:
            map_array = get_map("maps/level_3.csv")
            
            # Create Enemies
            self.enemies_left = 6
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(14, -9, 1, 1, 6)
            self.titan_list.append(titan)  
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(24, -6, 3, 2, 8)
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(32, -7, 1, 2, 6)
            self.titan_list.append(titan)
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(31, -7, 3, 3, 8)
            self.titan_list.append(titan)
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(39, -7, 3, 2, 6) 
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(50, -7, 1, 2, 8) 
            self.titan_list.append(titan)
        
        #---LEVEL 4---
        if self.level == 4:
            map_array = get_map("maps/level_4.csv")
            
            # Create Enemies
            self.enemies_left = 8
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(24, -8, 3, 2, 8)
            self.titan_list.append(titan)
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(31, -7, 3, 3, 8)
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(8, -7, 1, 4, 6)
            self.titan_list.append(titan)
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(8, -7, 3, 4, 8)
            self.titan_list.append(titan)            
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(51, -4, 1, 1, 6)
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(45, -7, 1, 1, 6)
            self.titan_list.append(titan)
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(42.5, -6, 3, 1.5, 8)
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(59.5, -5, 1, 1.5, 6)
            self.titan_list.append(titan)
         
        #---LEVEL 5---  
        if self.level == 5:
            map_array = get_map("maps/level_5.csv")
            
            # Create Enemies
            self.enemies_left = 8
            police = Enemy("sprites/police.png", SPRITE_SCALING)
            police.attributes(23.5, -7.6, 0, 0, 6)
            self.police_list.append(police)
            police = Enemy("sprites/police.png", SPRITE_SCALING)
            police.attributes(10, -7.6, 2, 1, 6)
            self.police_list.append(police)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(13.5, -9, 1, 1.5, 6)
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(19, -8, 1, 1, 6)
            self.titan_list.append(titan)
            police = Enemy("sprites/police.png", SPRITE_SCALING)
            police.attributes(31, -7.6, 2, 3, 6)
            self.police_list.append(police)
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(31, -7, 3, 3, 8)
            self.titan_list.append(titan)
            police = Enemy("sprites/police.png", SPRITE_SCALING)
            police.attributes(44, -5.6, 2, 1, 6)
            self.police_list.append(police)
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(51, -4, 3, 1, 8)
            self.titan_list.append(titan)            
        
        #---LEVEL 6---
        if self.level == 6:
            map_array = get_map("maps/level_6.csv")
            
            # Create Enemies
            self.enemies_left = 7
            police = Enemy("sprites/police.png", SPRITE_SCALING)
            police.attributes(11, -5.6, 2, 1, 6)
            self.police_list.append(police) 
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(18, -4, 3, 2, 8)
            self.titan_list.append(titan)
            titan = Enemy("sprites/titan.png", SPRITE_SCALING)
            titan.attributes(17, -4, 1, 2, 6)
            self.titan_list.append(titan)
            police = Enemy("sprites/police.png", SPRITE_SCALING)
            police.attributes(16, -7.6, 2, 4, 6)
            self.police_list.append(police)
            police = Enemy("sprites/police.png", SPRITE_SCALING)
            police.attributes(19, -7.6, -2, 4, 6)
            self.police_list.append(police)
            titan = Enemy("sprites/abnormal.png", SPRITE_SCALING)
            titan.attributes(23, -7, 3, 4, 6)
            self.titan_list.append(titan)
            
            # BOSS
            titan = Enemy("sprites/bert.png", SPRITE_SCALING * 1.5)
            titan.attributes(45, -5.2, 5, 6, 30)
            self.titan_list.append(titan)        
    
        for row_index in range(len(map_array)):
            for column_index in range(len(map_array[row_index])):
                wall = arcade.Sprite()
                coin = arcade.Sprite()
                titan = arcade.Sprite()
                door_opened = arcade.Sprite()
                door = arcade.Sprite()
                health_potion = arcade.Sprite()
                lava = arcade.Sprite()
                strength_potion = arcade.Sprite()
                gun = arcade.Sprite()
        
                item = map_array[row_index][column_index]
        
                # Wall items
                if item == 1:
                    wall.texture = arcade.load_texture("sprites/spritesheet.png", x = 64, y = 512, width = 64, height = 64)
                elif item == 2:
                    wall.texture = arcade.load_texture("sprites/spritesheet.png", x = 64, y = 448, width = 64, height = 64)
                elif item == 3:
                    wall.texture = arcade.load_texture("sprites/spritesheet.png", x = 0, y = 512, width = 64, height = 64)
                elif item == 4:
                    wall.texture = arcade.load_texture("sprites/spritesheet.png", x = 128, y = 512, width = 64, height = 64)
                elif item == 5:
                    wall.texture = arcade.load_texture("sprites/spritesheet.png", x = 0, y = 448, width = 64, height = 64)
                elif item == 6:
                    wall.texture = arcade.load_texture("sprites/spritesheet.png", x = 128, y = 448, width = 64, height = 64)
        
                if item >= 1 and item < 7:
                    # Calculate where the sprite goes
                    wall.left = column_index * SCALED_TILE_SIZE
                    wall.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE
        
                    # Add the sprite
                    self.wall_list.append(wall)
                
                # Special Items
                if item == 7:
                    coin.texture = arcade.load_texture("sprites/spritesheet.png", x = 64, y = 256, width = 64, height = 64)
                    coin.left = column_index * SCALED_TILE_SIZE + 15
                    coin.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE - 15
                    self.coin_list.append(coin)
                    
                if item == 8:
                    door_opened.texture = arcade.load_texture("sprites/spritesheet.png", x = 128, y = 576, width = 64, height = 64)
                    door_opened.left = column_index * SCALED_TILE_SIZE
                    door_opened.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE
                    self.door_opened_list.append(door_opened)  
                    door.texture = arcade.load_texture("sprites/spritesheet.png", x = 192, y = 640, width = 64, height = 64)
                    door.left = column_index * SCALED_TILE_SIZE
                    door.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE
                    self.door_list.append(door)
                
                if item == 9:
                    health_potion.texture = arcade.load_texture("sprites/spritesheet.png", x = 128, y = 256, width = 64, height = 64)
                    health_potion.left = column_index * SCALED_TILE_SIZE + 16
                    health_potion.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE - 15
                    self.health_potion_list.append(health_potion)
                
                if item == 10:
                    lava.texture = arcade.load_texture("sprites/spritesheet.png", x = 192, y = 448, width = 64, height = 64)
                    lava.left = column_index * SCALED_TILE_SIZE
                    lava.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE - 22
                    self.lava_list.append(lava)
                
                if item == 11:
                    strength_potion.texture = arcade.load_texture("sprites/spritesheet.png", x = 192, y = 256, width = 64, height = 64)
                    strength_potion.left = column_index * SCALED_TILE_SIZE + 16
                    strength_potion.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE - 15
                    self.strength_potion_list.append(strength_potion)
                
                if item == 12:
                    gun.texture = arcade.load_texture("sprites/spritesheet.png", x = 128, y = 640, width = 64, height = 64)
                    gun.left = column_index * SCALED_TILE_SIZE 
                    gun.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE - 25
                    self.gun_list.append(gun)                
    
        # Create out platformer physics engine with gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list, gravity_constant=GRAVITY)
        
    def on_draw(self):
        """ Render screen and draw everything """
        arcade.start_render()
        
        # Draw all sprites
        self.wall_list.draw()
        self.titan_list.draw()
        self.coin_list.draw()
        self.health_potion_list.draw()
        self.strength_potion_list.draw()
        self.door_list.draw()
        self.bullet_list.draw()
        self.gun_list.draw()
        self.player_list.draw()
        self.attack_list.draw()
        self.lava_list.draw()
        self.enemy_bullet_list.draw()
        self.police_list.draw()

        # Draw the opened door once all enemies are gone
        if self.enemies_left == 0:
            self.door_opened_list.draw()
        
        # Draw text on screen, scrolling it with the viewport
        arcade.draw_lrwh_rectangle_textured(self.view_left, SCREEN_HEIGHT - 60 + self.view_bottom, 64, 64, self.heart)
        arcade.draw_lrwh_rectangle_textured(450 + self.view_left, SCREEN_HEIGHT - 110 + self.view_bottom, 302, 126, self.score_enemy)
        
        lives_text = f": {self.lives}"
        arcade.draw_text(lives_text,  60 + self.view_left, SCREEN_HEIGHT - 53 + self.view_bottom,
                         arcade.csscolor.WHITE, 35)
        score_text = f"{self.score}"
        arcade.draw_text(score_text, SCREEN_WIDTH - 45 + self.view_left, SCREEN_HEIGHT - 40 + self.view_bottom,
                         arcade.csscolor.WHITE, 27)
        enemies_left_text = f"{self.enemies_left}"
        arcade.draw_text(enemies_left_text, SCREEN_WIDTH - 48 + self.view_left, SCREEN_HEIGHT - 83 + self.view_bottom,
                         arcade.csscolor.WHITE, 27)
        if self.bullet_amount >= 1:
            arcade.draw_lrwh_rectangle_textured(450 + self.view_left, SCREEN_HEIGHT - 150 + self.view_bottom, 302, 126, self.bullets_text)
            bullets_left = f"{self.bullet_amount}"
            arcade.draw_text(bullets_left, SCREEN_WIDTH - 48 + self.view_left, SCREEN_HEIGHT - 120 + self.view_bottom,
                         arcade.csscolor.WHITE, 27)
        if self.player_sprite.center_x >= 37 * SCALED_TILE_SIZE and self.level == 6:
            arcade.draw_lrwh_rectangle_textured(250 + self.view_left, SCREEN_HEIGHT - 550 + self.view_bottom, 302, 126, self.boss_text)
        
    def update(self, delta_time):
        """ Movement and game logic """
        # Call update on all sprites
        self.player_list.update()
        self.player_list.update_animation()
        self.coin_list.update()
        self.titan_list.update()
        self.attack_list.update()
        self.bullet_list.update()
        self.door_list.update()
        self.door_opened_list.update()
        self.wall_list.update()
        self.health_potion_list.update()
        self.strength_potion_list.update()
        self.lava_list.update()
        self.police_list.update()
        self.enemy_bullet_list.update()
        self.dmg_cooldown += delta_time
        self.attack_cooldown += delta_time
        self.potion_time += delta_time
        self.frame_count += 1

        # ENEMY UPDATES
        for titan in self.titan_list:
            titan.enemy_update()
        for police in self.police_list:
            police.enemy_update()
            police.shooting_update(self.player_sprite, self.enemy_bullet_list, self.frame_count)
        
        # If enemy touches a player, remove one life
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.titan_list)
        if self.dmg_cooldown >= 2:
            for titan in enemy_hit_list:
                arcade.play_sound(self.ow)
                self.lives -= 1
                if self.score >= 5:
                    self.score -= 5
                self.dmg_cooldown = 0
            
        # If enemy's health hits 0, remove
        for titan in self.titan_list:
            if titan.enemy_health <= 0:
                arcade.play_sound(self.titan_death_sound)
                titan.remove_from_sprite_lists()
                self.enemies_left -= 1
        for police in self.police_list:
            if police.enemy_health <= 0:
                arcade.play_sound(self.police_death_sound)
                police.remove_from_sprite_lists()
                self.enemies_left -= 1 
                
        enemy_bullet_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list)
        
        if self.dmg_cooldown >= 2:
            for bullet in enemy_bullet_hit_list:
                arcade.play_sound(self.ow)
                self.lives -= 1
                
                if len(enemy_bullet_hit_list) > 0:
                    bullet.remove_from_sprite_lists()                
                
                if self.score >= 5:
                    self.score -= 5
                self.dmg_cooldown = 0
            
        for bullet in self.enemy_bullet_list:
            enemy_bullet_wall_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
            
            if len(enemy_bullet_wall_list) > 0:
                bullet.remove_from_sprite_lists()               
            
            #If the bullet flies off-screen, remove it.
            if bullet.bottom > 0 or bullet.top < -1200 or bullet.right < 0 or bullet.left > (800 + self.view_left):
                bullet.remove_from_sprite_lists() 
        
        # Play sound if in boss arena
        if self.player_sprite.center_x == 37 * SCALED_TILE_SIZE and self.level == 6:
            arcade.play_sound(self.boss_sound)
        
        # LAVA UPDATES
        lava_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.lava_list)
        if self.dmg_cooldown >= 2:
            for lava in lava_hit_list:
                arcade.play_sound(self.fire_sound)
                arcade.play_sound(self.ow)
                self.lives -= 1
                if self.score >= 5:
                    self.score -= 5
                self.dmg_cooldown = 0
    
        # ATTACKS
        for attack in self.attack_list:
            # Check if attack hits an enemy
            attack_hit_list = arcade.check_for_collision_with_list(attack, self.titan_list)
            attack_hit_list_2 = arcade.check_for_collision_with_list(attack, self.police_list)       
            
            # Get rid of attack
            if len(attack_hit_list) > 0:
                attack.remove_from_sprite_lists()
            if len(attack_hit_list_2) > 0:
                attack.remove_from_sprite_lists()
            if self.attack_cooldown >= 1:
                attack.remove_from_sprite_lists()
                self.attack_cooldown = 0
               
            # For every titan we hit, decrease its health
            for titan in attack_hit_list:
                arcade.play_sound(self.titan_hurt_sound)
                titan.enemy_health -= self.player_attack_dmg
            for police in attack_hit_list_2:
                arcade.play_sound(self.police_hurt_sound)
                police.enemy_health -= self.player_attack_dmg
            
        # GUN UPDATES
        gun_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.gun_list)
        for gun in gun_hit_list:
            gun.remove_from_sprite_lists()
            arcade.play_sound(self.getting_gun)
            
            # Add 10 bullets for every gun we touch
            self.bullet_amount += 10
        
        for bullet in self.bullet_list:
            # Check if bullet hits enemy
            bullet_hit_list = arcade.check_for_collision_with_list(bullet, self.titan_list)
            bullet_hit_list_2 = arcade.check_for_collision_with_list(bullet, self.police_list)
            bullet_wall_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
            
            #For every titan we hit, decrease health
            for titan in bullet_hit_list:
                arcade.play_sound(self.titan_hurt_sound)
                titan.enemy_health -= self.player_attack_dmg
            for police in bullet_hit_list_2:
                arcade.play_sound(self.police_hurt_sound)
                police.enemy_health -= self.player_attack_dmg
                    
            # Get rid of attack
            if len(bullet_hit_list) > 0:
                bullet.remove_from_sprite_lists()
            if len(bullet_hit_list_2) > 0:
                bullet.remove_from_sprite_lists()
            if len(bullet_wall_list) > 0:
                bullet.remove_from_sprite_lists()            
            
            #If the bullet flies off-screen, remove it.
            if bullet.bottom > 0 or bullet.top < -1200 or bullet.right < 0 or bullet.left > (800 + self.view_left):
                bullet.remove_from_sprite_lists()         

        # Score count/coin collisions list
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            arcade.play_sound(self.coin_sound)
            coin.remove_from_sprite_lists()
            self.score += 1
        
        # If player hits a potion, add to its stats
        health_potion_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.health_potion_list)
        for health_potion in health_potion_hit_list:
            arcade.play_sound(self.health_sound) 
            health_potion.remove_from_sprite_lists()
            self.lives += 1
        strength_potion_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.strength_potion_list)
        for strength_potion in strength_potion_hit_list:
            arcade.play_sound(self.strength_sound)             
            strength_potion.remove_from_sprite_lists()
            self.potion_time = 0
            self.player_attack_dmg *= 2
        if self.potion_time >= 10:
            self.player_attack_dmg = 1
        
        # Door updates
        door_opened_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.door_opened_list)
        
        # If all enemies are gone, "open" the door.
        if self.enemies_left == 0:
            for door in self.door_list:
                arcade.play_sound(self.door_sound)
                door.kill()
            if self.level <= 5:
                # When player touches opened door
                for door_opened in door_opened_hit_list:
                    for i in range(7):
                        for wall in self.wall_list:
                            wall.kill()                 
                        for coin in self.coin_list:
                            coin.kill()
                        for door_opened in self.door_opened_list:
                            door_opened.kill()
                        for lava in self.lava_list:
                            lava.kill()
                        for gun in self.gun_list:
                            gun.kill()
                        for strength_potion in self.strength_potion_list:
                            strength_potion.kill()
                        for health_potion in self.health_potion_list:
                            health_potion.kill()
                            
                    # Advance to next level
                    self.level += 1
                    arcade.play_sound(self.next_level_sound)
                    self.load_level(self.level)
                    self.player_sprite.center_x = 4 * SCALED_TILE_SIZE
                    self.player_sprite.center_y = -8 * SCALED_TILE_SIZE
                    
            if self.level == 6:
                for door_opened in door_opened_hit_list:
                    arcade.play_sound(self.win)
                    self.player_sprite.center_x = 216
                    self.player_sprite.center_y = 382
                    game_over_view = GameOverView()
                    game_over_view.score = self.score
                    self.window.show_view(game_over_view)                     
        
        # If player dies move to game over page
        if self.lives <= 0:
            arcade.play_sound(self.game_over)
            self.player_sprite.center_x = 216
            self.player_sprite.center_y = 382          
            game_over_view = GameOverView()
            game_over_view.score = self.score
            self.window.show_view(game_over_view) 
            
        # --- Manage Scrolling ---
        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom - 1)   
            
        # Restrict character from going beyond window borders
        if self.player_sprite.center_x < 4 * SCALED_TILE_SIZE:
            self.player_sprite.center_x = 4 * SCALED_TILE_SIZE
        if self.player_sprite.center_x > 63 * SCALED_TILE_SIZE:
            self.player_sprite.center_x = 63 * SCALED_TILE_SIZE
        
        # Update physics engine
        self.physics_engine.update()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """
        # Create an attack
        attack = arcade.Sprite("sprites/invisible.png", SPRITE_SCALING)
        bullet = arcade.Sprite("sprites/bullet.png", SPRITE_SCALING)
        
        # LEFT BUTTON PRESSED: ATTACK
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Position the attack at the player's current location
            arcade.play_sound(self.attack_sound)
            start_y = self.player_sprite.center_y
            if self.player_faces_left == 1:
                start_x = self.player_sprite.center_x - 60
            elif self.player_faces_left == 0:
                start_x = self.player_sprite.center_x + 60
            attack.center_x = start_x
            attack.center_y = start_y
            
            # Get from the mouse the destination location for the attack
            dest_x = x + self.view_left
            dest_y = y + self.view_bottom
    
            # Do math to calculate how to get the attack to the destination.
            # Calculation the angle in radians between the start points
            # and end points.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)            
            attack.angle = math.degrees(angle)
            attack.change_x = math.cos(angle) * 0
            attack.change_y = math.sin(angle) * 0
            attack.center_y = start_y
            
            # Add the attack to the appropriate lists
            self.attack_list.append(attack)
        
        # RIGHT BUTTON PRESSED: BULLET
        if self.bullet_amount >= 1:
            if button == arcade.MOUSE_BUTTON_RIGHT:
                arcade.play_sound(self.pew)
                start_x = self.player_sprite.center_x
                start_y = self.player_sprite.center_y
                bullet.center_x = start_x
                bullet.center_y = start_y
                dest_x = x + self.view_left
                dest_y = y + self.view_bottom
                x_diff = dest_x - bullet.center_x
                y_diff = dest_y - bullet.center_y
                angle = math.atan2(y_diff, x_diff)             
                bullet.angle = math.degrees(angle)
                bullet.change_x = math.cos(angle) * 5
                bullet.change_y = math.sin(angle) * 5            
                self.bullet_list.append(bullet)
                self.bullet_amount -= 1
                self.attack_cooldown = 0
            
    def on_key_press(self, key, modifiers):
        """ Allows user to control player WASD """
        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                arcade.play_sound(self.jump_sound)
                self.player_sprite.change_y = JUMP_SPEED
                self.player_sprite.textures = []
                self.player_sprite.textures.append(arcade.load_texture("sprites/spritesheet.png", x = 0, y = 0, width = 64, height = 64))      
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
            self.player_sprite.textures = []
            for i in range(4):
                self.player_sprite.textures.append(arcade.load_texture("sprites/spritesheet.png", x = i*64, y = 128, width = 64, height = 64))
                self_player_faces_left = 1
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
            self.player_sprite.textures = []
            for i in range(4):
                self.player_sprite.textures.append(arcade.load_texture("sprites/spritesheet.png", x = i*64, y = 192, width = 64, height = 64))
                self_player_faces_left = 0
                
    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a button.
        """
        if key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
            self.player_sprite.textures = []
            self.player_sprite.textures.append(arcade.load_texture("sprites/spritesheet.png", x = 0, y = 0, width = 64, height = 64))
        if key == arcade.key.A:
            self.player_faces_left = 1
        elif key == arcade.key.D:
            self.player_faces_left = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Titan Slayer")
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()