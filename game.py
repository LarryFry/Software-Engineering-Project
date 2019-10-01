import pygame, sys
from pygame.locals import *
import random
import time


class Game(object):
		"""
		Manages game states and other variables
		"""
		def __init__(self, screen, states, start_state):
				"""
				Initialize the Game object.

				screen: the pygame display surface
				states: a dict mapping state-names to GameState objects
				start_state: name of the first active game state
				"""
				self.done = False
				self.screen = screen
				self.clock = pygame.time.Clock()
				self.fps = 60
				self.states = states
				self.state_name = start_state
				self.state = self.states[self.state_name]


		def event_loop(self):
				"""Events are passed for handling to the current state."""
				for event in pygame.event.get():
						self.state.get_event(event)

		def flip_state(self):
				"""Switch to the next game state."""
				current_state = self.state_name
				next_state = self.state.next_state
				self.state.done = False
				self.state_name = next_state
				persistent = self.state.persist
				self.state = self.states[self.state_name]
				self.state.startup(persistent)

		def update(self, dt):
				"""
				Check for state flip and update active state.

				dt: milliseconds since last frame
				"""
				if self.state.quit:
						self.done = True
				elif self.state.done:
						self.flip_state()
				self.state.update(dt)

		def draw(self):
				"""Pass display surface to active state for drawing."""
				self.state.draw(self.screen)

		def run(self):
				"""
				Pretty much the entirety of the game's runtime will be
				spent inside this while loop.
				"""
				while not self.done:
						dt = self.clock.tick(self.fps)
						self.event_loop()
						self.update(dt)
						self.draw()
						pygame.display.update()



class GameState(object):
		"""
		Parent class for individual game states to inherit from.
		"""
		def __init__(self):
				self.done = False
				self.quit = False
				self.next_state = None
				self.screen_rect = pygame.display.get_surface().get_rect()
				self.persist = {}
				self.font = pygame.font.Font(None, 24)

		def startup(self, persistent):
				"""
				Called when a state resumes being active.
				Allows information to be passed between states.

				persistent: a dict passed from state to state
				"""
				self.persist = persistent

		def get_event(self, event):
				"""
				Handle a single event passed by the Game object.
				"""
				pass


		def update(self, dt):
				"""
				Update the state. Called by the Game object once
				per frame.

				dt: time since last frame
				"""
				pass

		def draw(self, surface):
				"""
				Draw everything to the screen.
				"""
				pass


class Option:
				hovered = False

				def __init__(self, text, pos):
								self.text = text
								self.pos = pos
								self.set_rect()
								self.draw()

				def draw(self):
								self.set_rend()
								screen.blit(self.rend, self.rect)

				def set_rend(self):
								self.rend = menu_font.render(self.text, True, self.get_color())

				def get_color(self):
								if self.hovered:
												return (255, 255, 255)
								else:
												return (100, 100, 100)

				def set_rect(self):
								self.set_rend()
								self.rect = self.rend.get_rect()
								self.rect.topleft = self.pos
	

class MenuScreen(GameState):
		def __init__(self):
				super(MenuScreen, self).__init__()
				self.persist["screen_color"] = "black"
				
		def get_event(self, event):
				# Set clicker, which is an area of 3
				click = pygame.mouse.get_pressed()

				# Exits with wxit button
				if event.type == pygame.QUIT:
						self.quit = True
				
				# Menu Options
				if options[0].rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
						self.persist["screen_color"] = "dodgerblue"
						self.done = True
						self.next_state = "GAMEPLAY"
				elif options[1].rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
						self.done = True
						self.next_state = "RULES"
				elif options[2].rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
						self.done = True
						self.next_state = "GAMEOP"
				elif options[3].rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
						self.quit = True

		def draw(self, surface):
				surface.fill(pygame.Color("black"))
				for option in options:
								if option.rect.collidepoint(pygame.mouse.get_pos()):
												option.hovered = True
								else:
												option.hovered = False
								option.draw()


class Gameplay(GameState):
		"""
		Gameplay screen that will run the man game content at some point
		"""
		def __init__(self):
				super(Gameplay, self).__init__()
				self.rect = pygame.Rect((128, 128), (256, 256))
				self.x_velocity = 0
				self.deck = Deck()

		def startup(self, persistent):
				self.persist = persistent
				color = self.persist["screen_color"]
				self.screen_color = pygame.Color(color)
				if color == "dodgerblue":
						#text = "You clicked the mouse to get here"

						text = self.deck.deal_card()
				elif color == "gold":
						text = "You pressed a key to get here"
				self.title = self.font.render(text, True, pygame.Color("gray10"))
				self.title_rect = self.title.get_rect(center=self.screen_rect.center)

		def get_event(self, event):
				if event.type == pygame.QUIT:
						self.quit = True
				elif event.type == pygame.MOUSEBUTTONUP:
						self.deck.shuffle()
						text = self.deck.deal_card()
						self.title = self.font.render(text, True, pygame.Color("gray10"))
						self.title_rect.center = event.pos

		def update(self, dt):
				self.rect.move_ip(self.x_velocity, 0)


		def draw(self, surface):
				surface.fill(self.screen_color)
				surface.blit(self.title, self.title_rect)
				pygame.draw.rect(surface, pygame.Color("darkgreen"), self.rect)

class Rules(GameState):
		# back = Option("BACK", (0, 0)) 

		def __init__(self):
				super(Rules, self).__init__()
				self.screen_color = pygame.Color("indianred")		

		def get_event(self, event):
				click = pygame.mouse.get_pressed()
				# back = Option("BACK", (0, 0)) 
				if event.type == pygame.QUIT:
						self.quit = True

				# Back button 	NEED TO MAKE SO IT CAN GO BACK TO PREV STEP 	
				if back.rect.collidepoint(pygame.mouse.get_pos()) and click[0]:
					self.done = True
					self.next_state = "MENU"

		def draw(self, surface):
				surface.fill(self.screen_color)

				# Make back button
				if back.rect.collidepoint(pygame.mouse.get_pos()):
					back.hovered = True
				else:
					back.hovered = False
				back.draw()

class GameOp(GameState):
		def __init__(self):
				super(GameOp, self).__init__()

		def startup(self, persistent):
				self.screen_color = pygame.Color("lightblue")

		def get_event(self, event):
				if event.type == pygame.QUIT:
						self.quit = True

		def draw(self, surface):
				surface.fill(self.screen_color)

class Card:
		def __init__(self, rank, suit):
				self.suit = suit
				self.rank = rank
				self.ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
				if self.suit == "Clubs" or self.suit == "Spades":
						self.color = "Black"
				else:
						self.color = "Red"
		def get_name(self):
				return self.ranks[self.rank-1] + ' of ' + self.suit


		def __repr__(self):
				return self.get_name()

class Deck:
		def __init__(self):
				self.remainingCards = []
				self.dealtCards = []
				for suit in ['Hearts', 'Spades', 'Diamonds', 'Clubs']:
						for rank in range(1,14):
								self.remainingCards.append(Card(rank,suit))

		def shuffle(self):
				#print(self.remainingCards[0].get_name())
				#random.shuffle(self.remainingCards)
				#print(self.remainingCards[0].get_name())
				return random.shuffle(self.remainingCards)

		def deal_card(self):
				self.dealtCards.append(self.remainingCards.pop())
				return self.dealtCards[-1].get_name()
		def get_size(self):
				return len[self.remainingCards]


if __name__ == "__main__":
		pygame.init()
		menu_font = pygame.font.Font(None, 40)
		screen = pygame.display.set_mode((1280, 720))
		pygame.display.set_caption('Hand and Foot')

		# Need to figure out how to put these into the classs that is being used
		options = [Option("PLAY", (250, 100)), Option("RULES", (250, 150)),
						 Option("OPTIONS", (250, 200)), Option("QUIT", (250, 250))]
		back = Option("BACK", (0, 0)) 

		states = {"MENU": MenuScreen(), "GAMEPLAY": Gameplay(), "RULES": Rules(), "GAMEOP": GameOp()}
		game = Game(screen, states, "MENU")
		game.run()
		pygame.quit()
		sys.exit()
