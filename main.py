import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Furst Gaym"
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 15
GRAVITY = 1
PLAYER_JUMP_SPEED = 3000
COIN_SCALING = 0.5

class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text = "00:00:00",
            start_x = SCREEN_WIDTH - 100,
            start_y = SCREEN_HEIGHT - 50,
            color = arcade.color.WHITE,
            font_size = 30,
            anchor_x = "center",
        )

        self.scene = None

        self.player_sprite = None

        self.physics_engine = None

        self.camera = None

        self.gui_camera = None

        self.score = 0

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        
       self.total_time = 0.0
       
       self.gui_camera = arcade.Camera(self.width,self.height)

       self.score = 0
       
       self.camera = arcade.Camera(self.width,self.height)
       
       self.scene =arcade.Scene()

       self.scene.add_sprite_list("Player")
       self.scene.add_sprite_list("Walls",use_spatial_hash=True)

       image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
       self.player_sprite = arcade.Sprite(image_source,CHARACTER_SCALING)
       self.player_sprite.center_x = 64
       self.player_sprite.center_y = 128
       self.scene.add_sprite("Player",self.player_sprite)
       
       for x in range(0,1250,125):
        wall = arcade.Sprite(":resources:images/tiles/grassMid.png")
        wall.center_x = x
        wall.center_y = 1
        self.scene.add_sprite("Walls",wall)

        coord_list = [[512,96],[256,96],[768,96]]

        for coordinate in coord_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls",wall)

        for x in range(128,1250,256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png",COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.scene.add_sprite("Coins",coin)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer( self.player_sprite, gravity_constant = GRAVITY,walls = self.scene["Walls"])

    def on_draw(self):
        
         self.clear()

         self.camera.use()

         self.scene.draw()

         self.gui_camera.use()

         score_text = f"Score:{self.score}"
         arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
            )
        
         self.timer_text.draw()

    def on_key_press(self,key,modifiers):

        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED 

    def on_key_release(self,key,modifiers):

        if key == arcade.key.SPACE:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self,delta_time):

        self.total_time += delta_time

        minutes = int(self.total_time) // 60

        seconds = int(self.total_time) % 60

        seconds_100s = int((self.total_time - seconds) * 100)

        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"
        
        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.scene["Coins"])

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1

    def center_camera_to_player(self):
        
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width/2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height/2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x,screen_center_y
        
        self.camera.move_to(player_centered)
        

def main():
    
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()





