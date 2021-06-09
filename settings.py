class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's settings."""

		# Screen settings
		self.screen_width = 1200
		self.screen_height = 650
		self.bg_color = (230, 230, 230)
		self.ship_speed = 1.5
		self.target_limit = 2

		# Bullet settings
		self.bullet_speed = 1.5
		self.bullet_width = 15
		self.bullet_height = 3
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3

		# Alien settings
		self.alien_speed = 0.75
		self.fleet_drop_speed = 0
		# fleet_direction of 1 represents down; -1 represents up.
		self.fleet_direction = 1