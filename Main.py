import pygame
import pygame_gui
import Mobs
import Hero
import Gui
import Bullet 


pygame.init()
size = width, height = 1420, 720
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))

main_group = pygame.sprite.Group()
back_group = pygame.sprite.Group()
monstr_group = pygame.sprite.Group()
clock = pygame.time.Clock()

mobs_control = Mobs.Mob_manager()

character = Hero.Main_character(width, height, screen, monstr_group, main_group)

troll = Mobs.Troll(width, height, screen, character, False, monstr_group)

background = Hero.Background(screen)
###############################

gui = Gui.Gui(screen)
menu = True
new_wave = False
ups = False


###############################
wave = 0
tick_die = 0

with open("Save.txt", "r") as file:
	sp = [int(i.strip()) for i in file.readlines()]
	character.balance = sp[0]
	wave = sp[1]
	character.max_hp = character.health = sp[2]
	Bullet.Bullet.damage = sp[3]
	character.up_costs[1] = sp[4]
	character.up_costs[2] = sp[5]



run = True
while run:
	time_delta = clock.tick(70) / 1000.0 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame_gui.UI_BUTTON_PRESSED:
			if event.ui_element == gui.start_game:
				menu = False
				new_wave = False
				ups = False
			elif event.ui_element == gui.quit:
				run = False
			elif event.ui_element == gui.no:
				menu = True
				new_wave = False
				ups = False

				flag = True
			elif event.ui_element == gui.yes:
				menu = False
				new_wave = False
				ups = False
			elif event.ui_element == gui.lvl_up:
				ups = True
				menu = False
				new_wave = False
			elif event.ui_element == gui.button_attack:
				if character.balance - character.up_costs[1] >= 0:
					Bullet.Bullet.damage *= 2
					character.balance -= character.up_costs[1]
					character.up_costs[1] *= 2

				ups = True
				menu = False
				new_wave = False
			elif event.ui_element == gui.button_health:
				if character.balance - character.up_costs[2] >= 0:
					character.max_hp *= 2
					character.balance -= character.up_costs[2]
					character.up_costs[2] *= 2
					character.health = character.max_hp

				ups = True
				menu = False
				new_wave = False

			elif event.ui_element == gui.button_return:
				ups = False
				new_wave = False
				menu = True
		

		gui.manager.process_events(event)
		gui.manager1.process_events(event)
		gui.manager2.process_events(event)


	if ups:
		f = pygame.font.SysFont("arial", 36)
		text = f.render("Что будем улучшать?", True, (0, 0, 0))

		gui.manager2.update(time_delta)
		background.update(character.die, 0)
		gui.manager2.draw_ui(screen)



		screen.blit(text, (540, 270))
		character.balanced()
		character.costs()

			
	elif new_wave:
		f = pygame.font.SysFont("arial", 36)
		text = f.render("Вы готовы продолжать?", True, (0, 0, 0))

		gui.manager1.update(time_delta)
		background.update(character.die, 0)
		gui.manager1.draw_ui(screen)
		screen.blit(text, (510, 460))

	elif menu:	
		gui.manager.update(time_delta)
		background.update(character.die, 0)
		gui.manager.draw_ui(screen)
	elif not character.die:
		mobs_control.manager(width, height, screen, character, 2, 4, monstr_group, wave)

		background.update(character.die, wave)
		main_group.draw(screen)
		monstr_group.draw(screen)
		character.bullet_group.draw(screen)


		monstr_group.update()
		main_group.update(pygame.key.get_pressed(), event)
		character.bullet_group.update()

		if len(monstr_group) == 0 and wave < 5:
			wave += 1
			new_wave = True

	else:
		background.update(character.die, 0)
		tick_die += 1
		if tick_die == 150:
			main_group = pygame.sprite.Group()
			back_group = pygame.sprite.Group()
			monstr_group = pygame.sprite.Group()
			mobs_control = Mobs.Mob_manager()
			character = Hero.Main_character(width, height, screen, monstr_group, main_group)
			troll = Mobs.Troll(width, height, screen, character, False, monstr_group)
			background = Hero.Background(screen)
			tick_die = 0

			wave = 1
			menu = True
			ups = False
			new_wave = False


	pygame.display.flip()
	screen.fill((0, 0, 0))

with open("Save.txt", "w") as file:
	file.write(str(character.balance) + "\n")
	file.write(str(wave) + "\n")
	file.write(str(character.max_hp) + "\n")
	file.write(str(Bullet.Bullet.damage) + "\n")
	file.write(str(character.up_costs[1]) + "\n")
	file.write(str(character.up_costs[2]) + "\n")

pygame.quit()
