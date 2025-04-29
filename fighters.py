import pygame

class Fighter():
    def __init__(self,player,x,y,flip,data,sprite_sheet,animation_steps,sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet,animation_steps)
        self.action = 0 # idle 0 run 1 jump 2 attack_type_1 3 attack_type_2 4 hits 5 die 6
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x,y,80,150))
        self.val_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hits = False
        self.health = 100
        self.alive = True
    def load_images(self,sprite_sheet,animation_steps):
        animation_list = []
        for y,ani in enumerate(animation_steps):
            temp_img_list = []
            # extract images from sprite_sheet #
            for x in range(ani):
                temp_img = sprite_sheet.subsurface(x * self.size,y * self.size,self.size,self.size)
                temp_new = pygame.transform.scale(temp_img,(self.size * self.image_scale ,self.size * self.image_scale))
                temp_img_list.append(temp_new)
            animation_list.append(temp_img_list)
        return animation_list

    # handle animations updates #
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hits == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        # check what action is performed for player 
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0) 
        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        # check for time is enough for each update
        if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hits = False
                    self.attacking = False
                    self.attack_cooldown = 20
    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            # update the frames_index #
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            
    def draw(self,Screen):
        img = pygame.transform.flip(self.image , self.flip , False)
        #pygame.draw.rect(Screen,'red' ,self.rect)
        Screen.blit(img, (self.rect.x - (self.offset[0] * self.image_scale),self.rect.y -(self.offset[1] * self.image_scale)))
        
    def attack(self,target):
        if self.attack_cooldown == 0:
            self.attacking = True
            # call the sound #
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),self.rect.y ,2*self.rect.width,self.rect.height)
            if (attacking_rect.colliderect(target.rect)):
                target.health -= 10
                target.hits = True
            #pygame.draw.rect(Screen,'green',attacking_rect)
    def move(self,screen_width,screen_height,target,round_over):
        speed = 10
        dx = 0
        dy = 0
        gravity = 2
        self.running = False
        self.attack_type = 0
        # get keypressed #
        key = pygame.key.get_pressed()
        # can only do other things if and only if not attacking
        if self.attacking == False and self.alive == True and round_over == False:
            if self.player == 1:      
                # mechanism of movement #
                if key[pygame.K_a]:
                    dx = -speed
                    self.running = True
                elif key[pygame.K_d]:
                    dx = speed
                    self.running = True
                if key[pygame.K_w] and self.jump == False:
                    self.val_y = -30
                    self.jump = True 
                # attack mechanism #
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    # determine the type of the attack #
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    elif key[pygame.K_t]:
                        self.attack_type = 2
            if self.player == 2:      
                # mechanism of movement #
                if key[pygame.K_LEFT]:
                    dx = -speed
                    self.running = True
                elif key[pygame.K_RIGHT]:
                    dx = speed
                    self.running = True
                if key[pygame.K_UP] and self.jump == False:
                    self.val_y = -30
                    self.jump = True 
                # attack mechanism #
                if key[pygame.K_m] or key[pygame.K_n]:
                    self.attack(target)
                    # determine the type of the attack #
                    if key[pygame.K_m]:
                        self.attack_type = 1
                    elif key[pygame.K_n]:
                        self.attack_type = 2
                    
        # apply attack cooldown #
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        # apply gravity
        # we need gravity # 
              
        self.val_y += gravity
        dy += self.val_y
        
        # Ensure that fighers are on the screen #
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.val_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom



        # ensure that players face each others #
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        
            
        # update the move #
        self.rect.x += dx
        self.rect.y += dy
       
    
