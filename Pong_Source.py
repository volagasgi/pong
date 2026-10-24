#-------------------------------------------------------------
# Αυτό είναι το πρώτο μου παιχνίδι σε Python.
# Είναι pong για δύο παίκτες.
#-------------------------------------------------------------
import pygame
# import random

class Player1(pygame.sprite.Sprite):                                                                      # Κλάση Player1 
    def __init__(self, all_sprites, all_players):                                                         # Το δεύτερο arg είναι το sprite group
        super().__init__(all_sprites, all_players)                                                        # Αρχικοποίηση μητρικής κλάσης
        self.image = pygame.image.load('C:/Users/Admin/Desktop/pong/Player1/player1.png').convert_alpha() # Surface Player1
        self.rect = self.image.get_frect(midleft=(-26, screen_height/2))                                  # Rectangle Player1
        self.direction = pygame.math.Vector2(0,0)                                                         # Αρχικοποίηση κατεύθυνσης με [0,0]
        self.speed = 200                                                                                  # Αρχικοποίηση ταχύτητας

    def update(self, dt):
        keys = pygame.key.get_pressed()                                                                   # Είσοδος πλήκτρων
        self.direction.y = int(keys[pygame.K_s] - keys[pygame.K_w])                                       # Αλλαγή κατεύθηνσης ανάλογα με την είσοδο
        # self.direction.normalize() if self.direction else self.direction                                # Αν είχα κίνηση σε 2D κρατάει σταθερή ταχήτητα
        self.rect.center += self.direction*self.speed*dt                                                  # Αλλαγή θέσης

class Player2(pygame.sprite.Sprite):                                                                      # Κλάση Player2
    def __init__(self, all_sprites, all_players):                                                         # Το δεύτερο arg είναι το sprite group
        super().__init__(all_sprites, all_players)                                                        # Αρχικοποίηση μητρικής κλάσης
        self.image = pygame.image.load('C:/Users/Admin/Desktop/pong/Player2/player2.png').convert_alpha() # Surface Player2
        self.rect = self.image.get_frect(midright=(screen_width + 25, screen_height/2))                   # Rectangle Player2
        self.direction = pygame.math.Vector2()                                                            # Αρχικοποίηση κατεύθυνσης με [0,0]
        self.speed = 200                                                                                  # Αρχικοποίηση ταχύτητας
        
    def update(self, dt):
        keys = pygame.key.get_pressed()                                                                   # Είσοδος πλήκτρων
        self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])                                   # Αλλαγή κατεύθηνσης ανάλογα με την είσοδο
        # self.direction.normalize() if self.direction else self.direction                                # Αν είχα κίνηση σε 2D κρατάει σταθερή ταχήτητα
        self.rect.center += self.direction*self.speed*dt                                                  # Αλλαγή θέσης

class Ball(pygame.sprite.Sprite):                                                                         # Κλάση μπάλας
    def __init__(self, all_sprites):                                                                      # Το δεύτερο arg είναι το sprite group
        super().__init__(all_sprites)                                                                     # Αρχικοποίηση μητρικής κλάσης
        self.image = pygame.image.load('C:/Users/Admin/Desktop/pong/Ball/ball1.png').convert_alpha()      # Surface μπάλας
        self.rect = self.image.get_frect(center=(screen_width/2, screen_height/2))                        # Rectangle μπάλας
        self.direction = pygame.math.Vector2(1,-1)                                                        # Αρχικοποίηση κατεύθυνσης με [1,-1]
        self.speed = 250                                                                                  # Αρχικοποίηση ταχύτητας
        # cooldown
        self.collided = False                                                                             # Αρχικοποίηση για να μπει στο if
        self.collision_time = 0                                                                           # Αρχικοποίηση collision_time
        self.cooldown_duration = 1000                                                                     # Διάρκεια cooldown

    def collision_timer(self):                                                                            # Μέθοδος που δέχεται τον τωρινό χρόνο
        if self.collided:
            current_time = pygame.time.get_ticks()
            if current_time >= self.collision_time + self.cooldown_duration: self.collided = False        # Αν έχει περάσει το cooldown ορίζει ξανά το collided = False

    def update(self, dt):
        self.collision_timer()                                                                            # Καλεί τη μέθοδο collision_timer
        if bool(pygame.sprite.spritecollide(ball, all_players, False)) and not self.collided:             # Έλεγχος γιά σύγκρουση μπάλας με παίχτη
            self.direction.x *= -1                                                                        # Αλλαγή κατεύθυνσης σε περίπτωση σύγκρουσης
            self.collided = True                                                                          # Έγινε η σύγκρουση
            self.collision_time = pygame.time.get_ticks()                                                 # Δέχεται την χρονική στιγμή της σύγκρουσης
        if self.rect.left <= 0:                                                                           # Αν ακουμπάει στο αριστερό άκρο
            self.rect.left = 0                                                                            # Τοποθετεί την άκρη της μπάλας στην άκρη της οθόνης (για αποφυγή προβλημάτων)
            self.direction.x *= -1                                                                        # Αλλαγή κατεύθυνσης
        if self.rect.right >= screen_width:                                                               # Όμοια με τα παραπάνω
            self.rect.right = screen_width
            self.direction.x *= -1
        if self.rect.bottom <= 0:                                                                         # Όμοια με τα παραπάνω
            self.rect.bottom = 0
            self.direction.y *= -1
        if self.rect.top >= screen_height:                                                                # Όμοια με τα παραπάνω
            self.rect.top = screen_height
            self.direction.y *= -1
        self.rect.center += self.direction * self.speed * dt                                              # Αλλαγή θέσης

pygame.init()                                                                                           # Αρχικοποιούμε το Pygame
screen_width, screen_height = 960, 720                                                                  # Πλάτος και ύψος παραθύρου
display_surface = pygame.display.set_mode((screen_width, screen_height))                                # Μέγεθος παραθύρου
pygame.display.set_caption('Pong')                                                                      # Τίτλος παραθύρου
pygame.display.set_icon(pygame.image.load('C:\\Users\\Admin\\Desktop\\pong\\Image\\pong.png'))          # Εικονίδιο παραθύρου
background_image = pygame.image.load('C:/Users/Admin/Desktop/pong/Background/background.png').convert() # Background
clock = pygame.time.Clock()                                                                             # fps

all_sprites = pygame.sprite.Group()                # Δημιουργία sprite group για όλα τα sprites
all_players = pygame.sprite.Group()                # Δημιουργία sprite group για παίχτες
player1 = Player1(all_sprites,all_players)         # Instance της κλάσης του player1
player2 = Player2(all_sprites,all_players)         # Instance της κλάσης του player2
ball = Ball(all_sprites)                           # Instance της κλάσης της μπάλας

# n = random.randint(1, 2)    # Τυχαία επιλογή κατεύθυνσης της μπάλας
# not_hit = True              # Αρχικά η μπάλα δεν έχει χτυπήσει κάποιον παίκτη
counter = 0
running = True                           # Σημαία για τον κύκλο του παιχνιδιού
while running:                           # Κύκλος του παιχνιδιού
    counter += 1
    dt = clock.tick()/1000               # Delta Time
    for event in pygame.event.get():     # Γεγονότα
        if event.type == pygame.QUIT:    # Τερματισμός παραθύρου
            running = False
 
    all_sprites.update(dt)                                # update

    display_surface.blit(background_image, (0,0))         # Εμφάνιση background
    all_sprites.draw(display_surface)                     # Εμφάνιση των sprites
    pygame.display.update()                               # Επικαιροποίηση της οθόνης

pygame.quit()
print(f'{counter} επαναλήψεις συνολικά.')
'''
if not_hit:
    n = randint(1, 2)
    ball_x_pos += (-1) ** n
else:
    Ό,τι κώδικα χρειάζεται για να αλλάξει η κατεύθυνση της μπάλας όταν χτυπήσει τον παίκτη
'''
# !!! Να προσθεσω οταν μπει γκολ να οριζεται not_hit = True και το n=1 ή n=2 αναλογα με τον νικητη !!!
# Να δω αν μπορώ να χρησιμοποιήσω inheritance για players  με μια μητρικη κλαση "Player()"
# Να κάνω normalize() τη κατεύθυνση της μπάλας; - Μάλλον όχι...
# Να προσθέσω όριο για να μην βγαίνουν οι παίχτες έξω από την οθόνη.
# Μπορώ να κάνω troll pong που θα πρέπει να αποφύγεις την μπάλα, γιατί θα διαγράφεται η ρακέτα.
# Μπορώ να κάνω μενού με pong variants.