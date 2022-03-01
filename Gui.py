import pygame
import pygame_gui


class Gui():
	def __init__(self, screen):

		self.manager = pygame_gui.UIManager((1420, 720))
		self.manager1 = pygame_gui.UIManager((1420, 720))
		self.manager2 = pygame_gui.UIManager((1420, 720))

		self.screen = screen

		self.start_game = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((610, 140), (200, 75)),
			text="Начать игру",
			manager=self.manager
		)

		self.lvl_up = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((610, 290), (200, 75)),
			text="Навыки",
			manager=self.manager
		)

		self.quit = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((610, 440), (200, 75)),
			text="Выход",
			manager=self.manager
		)

		self.yes = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((410, 550), (200, 75)),
			text="Да",
			manager=self.manager1
		)

		self.no = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((815, 550), (200, 75)),
			text="Нет",
			manager=self.manager1
		)

		self.button_attack = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((410, 360), (200, 75)),
			text="Атака",
			manager=self.manager2
		)

		self.button_health = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((810, 360), (200, 75)),
			text="Здоровье",
			manager=self.manager2
		)

		self.button_return = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((1222, 0), (200, 75)),
			text="Назад",
			manager=self.manager2
		)