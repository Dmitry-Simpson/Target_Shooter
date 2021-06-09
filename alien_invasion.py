import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Target Practice")

		# Createan instance to store game statistics.
		self.stats = GameStats(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		# Start Alien Invasion in an active state.
		self.game_active = True

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()
			

	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
				
	def _check_keydown_events(self, event):
		"""Respond to keypresses."""
		if event.key == pygame.K_UP:
			self.ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		"""Respond to key releases."""
		if event.key == pygame.K_UP:
			self.ship.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = False

	def _create_fleet(self):
		"""Create the fleet of aliens."""
		# Create an alien and find the number of aliens in a column.
		# Spacing between each alien is equal to one alien width.
		alien = Alien(self)
		self.aliens.add(alien)


	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction."""
		for alien in self.aliens.sprites():
			alien.rect.x -= self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _check_bullet_alien_collisions(self):
		"""Respond to bullet-alien collisions."""
		# Remove any bullets and aliens that have collided.
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)

		if not self.aliens:
			# Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()

	def _ship_hit(self):
		"""Respond to the ship being hit by an alien."""
		if self.stats.ships_left > 0:
			# Decrement ships_left.
			self.stats.ships_left -= 1

			# Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

			# Pause.
			sleep(0.5)
			print(self.stats.ships_left)
		else:
			self.stats.game_active = False

	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen."""
		for alien in self.aliens.sprites():
			if alien.rect.left <= 0:
				# Treat this the same as if the ship got hit.
				self._ship_hit()
				break

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets."""
		# Update bullet positions.
		self.bullets.update()
		
		# Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.left >= self.settings.screen_width:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	
		
	def _update_aliens(self):
		"""
		Check if the fleet is at an edge,
			then update the positions of all aliens in the fleet.
		"""
		self._check_fleet_edges()
		self.aliens.update()

		# Look for alien-ship collisions.
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Look for aliens hitting the bottom of the screen.
		self._check_aliens_bottom()

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		
		pygame.display.flip()

if __name__ == '__main__':
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()