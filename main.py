import pygame
from random import choice

pygame.mixer.pre_init(44100, -16, 1, 512)  # для отсутствия задержи
pygame.init()
size = width, height = 474, 800  # размеры окна
screen = pygame.display.set_mode(size)
damage_enemy = range(3, 10)

FPS = 15
clock = pygame.time.Clock()

# список с путями игровых костей
dice_list = ['data\image\dice 1.png', 'data\image\dice 2.png', 'data\image\dice 3.png',
             'data\image\dice 4.png', 'data\image\dice 5.png', 'data\image\dice 6.png']

# словарь для определения типа кости
type_dice_dict = {'data\image\dice 1.png': '1',
                  'data\image\dice 2.png': '2',
                  'data\image\dice 3.png': '3',
                  'data\image\dice 4.png': '4',
                  'data\image\dice 5.png': '5',
                  'data\image\dice 6.png': '6'}


# класс игровых костей
class Dice(pygame.sprite.Sprite):
    def __init__(self, coords, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.filename = filename

    def render(self):
        sprite_image = pygame.image.load(self.filename)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))

    def get_type_dice(self):
        return type_dice_dict[self.filename]


# класс поля игрока
class PlayersField(pygame.sprite.Sprite):
    def __init__(self, coords, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.filename = filename

    def render(self):
        sprite_image = pygame.image.load(self.filename)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))


# класс поля врага
class EnemysField(pygame.sprite.Sprite):
    def __init__(self, coords, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.filename = filename

    def render(self):
        sprite_image = pygame.image.load(self.filename)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))


# класс кнопки перемешивания игровых костей
class MixDiceButton(pygame.sprite.Sprite):
    def __init__(self, coords, filename_btn_on, filename_btn_off, sound_patn=None, number_throws=None):
        pygame.sprite.Sprite.__init__(self)
        self.image_btn_on = pygame.image.load(filename_btn_on)
        self.image_btn_off = pygame.image.load(filename_btn_off)
        self.rect = self.image_btn_on.get_rect()  # прямоугольник для обоих состояний кнопки
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.filename_btn_on = filename_btn_on
        self.filename_btn_off = filename_btn_off

        self.sound = None
        if sound_patn:
            self.sound = pygame.mixer.Sound(sound_patn)

        self.number_throws = number_throws

    def render(self):
        if self.number_throws is None or self.number_throws > 0:
            sprite_image = pygame.image.load(self.filename_btn_on)
        else:
            sprite_image = pygame.image.load(self.filename_btn_off)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered and \
                (self.number_throws is None or self.number_throws > 0):

            if self.number_throws:
                self.number_throws -= 1

            global dice1, dice2, dice3, dice4, dice5
            dice1 = Dice((12, size[1] - 164), choice(dice_list))
            dice2 = Dice((88, size[1] - 164), choice(dice_list))
            dice3 = Dice((164, size[1] - 164), choice(dice_list))
            dice4 = Dice((240, size[1] - 164), choice(dice_list))
            dice5 = Dice((316, size[1] - 164), choice(dice_list))

            if self.sound:
                self.sound.play()

            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def remove_number_throws(self):
        global fix_mix
        self.number_throws = fix_mix
        return self.number_throws


# класс кнопки конца хода
class EndTurnButton(pygame.sprite.Sprite):
    def __init__(self, coords, filename, sound_path=None, st=None, player=None, players_cards=None, enemy=None, mix_btn=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

        self.filename = filename
        self.player = player
        self.players_cards = players_cards
        self.enemy = enemy
        self.mix_btn = mix_btn

    def render(self):
        sprite_image = pygame.image.load(self.filename)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            global striker
            striker = 'enemy'

            if self.sound:
                self.sound.play()

            if choice([0, 1]) == 1:
                self.player.get_damage(choice(damage_enemy))
            else:
                self.enemy.get_healtn(choice(damage_enemy))
            for i in self.players_cards:
                i.remove_motion()

            global dice1, dice2, dice3, dice4, dice5
            dice1 = Dice((12, size[1] - 164), choice(dice_list))
            dice2 = Dice((88, size[1] - 164), choice(dice_list))
            dice3 = Dice((164, size[1] - 164), choice(dice_list))
            dice4 = Dice((240, size[1] - 164), choice(dice_list))
            dice5 = Dice((316, size[1] - 164), choice(dice_list))

            self.mix_btn.remove_number_throws()

            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


# класс обычных кнопок
class Button(pygame.sprite.Sprite):
    def __init__(self, coords, filename, sound_path=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

        self.filename = filename

    def render(self):
        sprite_image = pygame.image.load(self.filename)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:

            if self.sound:
                self.sound.play()

            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


# класс кнопки старта
class PlayButton(pygame.sprite.Sprite):
    def __init__(self, coords, filename, sound_path=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

        self.filename = filename

    def render(self):
        sprite_image = pygame.image.load(self.filename)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:

            if self.sound:
                self.sound.play()

            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

            global run
            run = False


# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, coords, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.filename = filename

        self.current_healtn = 10
        self.max_healtn = 10
        self.healtn_bar_length = 292
        self.healtn_ratio = self.max_healtn / self.healtn_bar_length

    def render(self):
        sprite_image = pygame.image.load(self.filename)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))

    def update_player(self):
        self.basic_healtn()

    def get_damage(self, amount):
        if self.current_healtn > 0:
            self.current_healtn -= amount
        if self.current_healtn <= 0:
            self.current_healtn = 0

    def get_healtn(self, amount):
        if self.current_healtn < self.max_healtn:
            self.current_healtn += amount
        if self.current_healtn >= self.max_healtn:
            self.current_healtn = self.max_healtn

    def basic_healtn(self):
        pygame.draw.rect(screen, (230, 103, 97), (88, size[1] - 76, self.current_healtn / self.healtn_ratio, 64))

    def get_hp(self):
        return self.current_healtn


# класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, coords, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.filename = filename

        self.current_healtn = 10
        self.max_healtn = 10
        self.healtn_bar_length = 216
        self.healtn_ratio = self.max_healtn / self.healtn_bar_length

    def render(self):
        sprite_image = pygame.image.load(self.filename)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))

    def update_enemy(self):
        self.basic_healtn()

    def get_damage(self, amount):
        if self.current_healtn > 0:
            self.current_healtn -= amount
        if self.current_healtn <= 0:
            self.current_healtn = 0

    def get_healtn(self, amount):
        if self.current_healtn < self.max_healtn:
            self.current_healtn += amount
        if self.current_healtn >= self.max_healtn:
            self.current_healtn = self.max_healtn

    def basic_healtn(self):
        pygame.draw.rect(screen, (230, 103, 97), (167, 28, self.current_healtn / self.healtn_ratio, 64))

    def get_hp(self):
        return self.current_healtn


class PlayerCard(pygame.sprite.Sprite):
    def __init__(self, coords, filename_card_on, filename_card_off, type_condition, action, condition=None):
        pygame.sprite.Sprite.__init__(self)
        self.image_card_on = pygame.image.load(filename_card_on)
        self.image_card_off = pygame.image.load(filename_card_off)
        self.rect = self.image_card_on.get_rect()  # прямоугольник для обоих состояний кнопки
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.filename_card_on = filename_card_on
        self.filename_card_off = filename_card_off

        self.type_condition = type_condition
        self.condition = condition

        self.on_or_off = False
        self.mouse_pos_True_or_False = False
        self.motion = True

        self.action = action

    def render(self):
        global dice1, dice2, dice3, dice4, dice5
        type_dice_player = ''.join([dice1.get_type_dice(), dice2.get_type_dice(), dice3.get_type_dice(),
                                    dice4.get_type_dice(), dice5.get_type_dice()])
        if self.type_condition == 'specific':
            type_dice_condition = {'1': 0,
                                   '2': 0,
                                   '3': 0,
                                   '4': 0,
                                   '5': 0,
                                   '6': 0}
            for i in self.condition:
                if type_dice_condition[i] != 0:
                    type_dice_condition[i] += 1
                else:
                    type_dice_condition[i] = 1
            k = 0
            for i in range(1, 7):
                if type_dice_condition[str(i)] <= type_dice_player.count(str(i)):
                    k += 1
            if self.motion:
                if k == 6:
                    sprite_image = pygame.image.load(self.filename_card_on)
                    self.on_or_off = True
                else:
                    sprite_image = pygame.image.load(self.filename_card_off)
                    self.on_or_off = False
                screen.blit(sprite_image, (self.rect.x, self.rect.y))

        if self.type_condition == 'similar':
            k = False
            for i in range(1, 7):
                if type_dice_player.count(str(i)) >= int(self.condition):
                    k = True
                    break
            if self.motion:
                if k:
                    sprite_image = pygame.image.load(self.filename_card_on)
                    self.on_or_off = True
                else:
                    sprite_image = pygame.image.load(self.filename_card_off)
                    self.on_or_off = False
                screen.blit(sprite_image, (self.rect.x, self.rect.y))

    def get_on_or_off(self):
        return self.on_or_off

    def get_mouse_pos_True_or_False(self):
        return self.mouse_pos_True_or_False

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered:
            self.mouse_pos_True_or_False = True
        else:
            self.mouse_pos_True_or_False = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:

            if self.motion and self.on_or_off:
                self.motion = False
                sound = pygame.mixer.Sound('data\sound\put the card down.mp3')
                sound.play()

            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def get_action(self):
        return self.action

    def get_motion(self):
        return self.motion

    def remove_motion(self):
        self.motion = True


class Game:
    def __init__(self, dice1, dice2, dice3, dice4, dice5,
                 playercard1, playercard2, playercard3, playercard4, playercard5, playercard6,
                 player, enemy,
                 mix_dice_btn, end_turn_btn,
                 striker):
        self.dice1 = dice1
        self.dice2 = dice2
        self.dice3 = dice3
        self.dice4 = dice4
        self.dice5 = dice5

        self.playercard1 = playercard1
        self.playercard2 = playercard2
        self.playercard3 = playercard3
        '''self.playercard4 = playercard4
        self.playercard5 = playercard5
        self.playercard6 = playercard6'''

        self.player = player
        self.enemy = enemy
        self.mix_dice_btn = mix_dice_btn
        self.end_turn_btn = end_turn_btn

        self.striker = striker

    def card_update(self, event):
        if self.striker:
            if self.playercard1:
                if self.playercard1.get_on_or_off() and self.playercard1.get_mouse_pos_True_or_False() and \
                        event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.playercard1.get_motion():
                    if self.playercard1.get_action()[0] == '-':
                        self.enemy.get_damage(int(self.playercard1.get_action()[1:]))
                    else:
                        self.player.get_healtn(int(self.playercard1.get_action()[1:]))

            if self.playercard2:
                if self.playercard2.get_on_or_off() and self.playercard2.get_mouse_pos_True_or_False() and \
                        event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.playercard2.get_motion():
                    if self.playercard2.get_action()[0] == '-':
                        self.enemy.get_damage(int(self.playercard2.get_action()[1:]))
                    else:
                        self.player.get_healtn(int(self.playercard2.get_action()[1:]))

            if self.playercard3:
                if self.playercard3.get_on_or_off() and self.playercard3.get_mouse_pos_True_or_False() and \
                        event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.playercard3.get_motion():
                    if self.playercard3.get_action()[0] == '-':
                        self.enemy.get_damage(int(self.playercard3.get_action()[1:]))
                    else:
                        self.player.get_healtn(int(self.playercard3.get_action()[1:]))


class MySprite(pygame.sprite.Sprite):
    def __init__(self, coords, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.filename = filename

    def render(self):
        sprite_image = pygame.image.load(self.filename)
        screen.blit(sprite_image, (self.rect.x, self.rect.y))


# функция для проигрывания звуков
def sound_play(sound_path, volume):
    music = pygame.mixer.Sound(sound_path)
    music.play()
    music.set_volume(volume)


# функция начального экрана
def start_screen():
    global run
    hi = MySprite((0, 0), 'data\image\hi.png')
    playbtn = PlayButton((158, 468), 'data\image\play btn.png',
                         'data\sound\pressing button sound 1.mp3')
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            playbtn.handle_event(event)
        hi.render()
        playbtn.render()
        playbtn.check_hover(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def show_go_screen():
    pygame.display.set_mode((800, 474))
    screen.fill((0, 0, 0))
    end_text = MySprite((0, 0), filename='data\image\end.png')
    end_text.render()
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)


start_screen()
striker = 'player'

# проигрывание фоновой музыки
sound_play('data\sound\music background 1.mp3', 0.2)

fix_mix = 2


def main():
    global fix_mix
    fon = MySprite((0, 0), 'data\image\_fon1.jpg')
    # игровые кости
    global dice1, dice2, dice3, dice4, dice5
    dice1 = Dice((12, size[1] - 164), choice(dice_list))
    dice2 = Dice((88, size[1] - 164), choice(dice_list))
    dice3 = Dice((164, size[1] - 164), choice(dice_list))
    dice4 = Dice((240, size[1] - 164), choice(dice_list))
    dice5 = Dice((316, size[1] - 164), choice(dice_list))

    # карты игрока
    playercard1 = PlayerCard((18, size[1] - 304), 'data\image\card 1 on.png', 'data\image\card 1 off.png',
                                 'specific', '-5', '12')
    playercard2 = PlayerCard((170, size[1] - 304), 'data\image\card 2 on.png', 'data\image\card 2 off.png',
                                 'specific', '+5', '5')
    playercard3 = PlayerCard((332, size[1] - 304), 'data\image\card 3 on.png', 'data\image\card 3 off.png',
                                 'similar', '-1', '2')
    playercard4 = PlayerCard((18, size[1] - 442), 'data\image\card 4 on.png', 'data\image\card 4 off.png',
                                 'similar', '3')
    playercard5 = PlayerCard((170, size[1] - 442), 'data\image\card 5 on.png', 'data\image\card 5 off.png',
                                 'specific', '666')
    playercard6 = PlayerCard((322, size[1] - 442), 'data\image\card 6 on.png', 'data\image\card 6 off.png',
                                 'specific', '33')

    # поле игрока
    players_field = PlayersField((0, size[1] - 176), 'data\image\players field.png')

    # поле врага
    enemys_field = EnemysField((79, 16), 'data\image\enemys field hp.png')

    # кнопка перемешивания костей
    mix_dice_btn = MixDiceButton((404, size[1] - 164), 'data\image\mix dice btn on.png',
                                     'data\image\mix dice btn off.png', 'data\sound\mix dice sound 1.mp3', fix_mix)

    # игрок
    player = Player((12, size[1] - 76), 'data\image\players avatar 1.png')

    # враг
    enemy = Enemy((91, 28), 'data\image\enemy 1.png')

    # кнопка конца хода
    end_turn_btn = EndTurnButton((404, size[1] - 76), 'data\image\end turn btn.png',
                                 'data\sound\pressing button sound 1.mp3', player=player, players_cards=(
            playercard1, playercard2, playercard3
        ), enemy=enemy, mix_btn=mix_dice_btn)

    '''game = Game(dice1, dice2, dice3, dice4, dice5,
                playercard1, playercard2, playercard3, playercard4, playercard5, playercard6,
                player, enemy,
                mix_dice_btn, end_turn_btn)'''

    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over:
                show_go_screen()

            if enemy.get_hp() <= 0 or player.get_hp() <= 0:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.get_healtn(1)
                if event.key == pygame.K_DOWN:
                    player.get_damage(1)

            game = Game(dice1, dice2, dice3, dice4, dice5,
                        playercard1, playercard2, playercard3, playercard4, playercard5, playercard6,
                        player, enemy,
                        mix_dice_btn, end_turn_btn,
                        striker)

            game.card_update(event)

            mix_dice_btn.handle_event(event)
            end_turn_btn.handle_event(event)

            playercard1.handle_event(event)
            playercard2.handle_event(event)
            playercard3.handle_event(event)
            '''playercard4.handle_event(event)
            playercard5.handle_event(event)
            playercard6.handle_event(event)'''

        screen.fill((0, 128, 0))
        fon.render()
        # рендер всех спрайтов (кроме костей и карт)
        players_field.render()
        enemys_field.render()

        mix_dice_btn.render()
        end_turn_btn.render()

        player.render()
        enemy.render()

        # рендер карт игрока
        playercard1.render()
        playercard2.render()
        playercard3.render()
        '''playercard4.render()
        playercard5.render()
        playercard6.render()'''

        # рендер костей игрока
        dice1.render()
        dice2.render()
        dice3.render()
        dice4.render()
        dice5.render()

        player.update_player()  # обновление игрока
        enemy.update_enemy()  # обновление врага

        # проверка кнопок
        mix_dice_btn.check_hover(pygame.mouse.get_pos())
        end_turn_btn.check_hover(pygame.mouse.get_pos())

        # потом убрать звук
        playercard1.check_hover(pygame.mouse.get_pos())
        playercard2.check_hover(pygame.mouse.get_pos())
        playercard3.check_hover(pygame.mouse.get_pos())
        '''playercard4.check_hover(pygame.mouse.get_pos())
        playercard5.check_hover(pygame.mouse.get_pos())
        playercard6.check_hover(pygame.mouse.get_pos())'''

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    while True:
        main()
