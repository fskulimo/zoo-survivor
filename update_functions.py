import arcade

def collide_projectiles(projectile_list):
    for projectile in self.projectile_list:
           if len(arcade.check_for_collision_with_list(projectile, hit_list)) > 0:
               projectile.kill()

               # Special case with the splinter projectile -> creates more moving in random directions
               if type(projectile) is Splinter_Projectile:   
                    for i in range (projectile.splinters_left):
                        random_x = random.randrange(-100, 100)
                        random_y = random.randrange(-100, 100)

                        target_x = projectile.center_x + random_x
                        target_y= projectile.center_y + random_y

                        splinter_projectile = Splinter_Projectile("images/banana.png", SPRITE_SCALING_SMALL_BANANA, target_x, target_y, projectile.position, 0)
                        self.projectile_list.append(splinter_projectile)