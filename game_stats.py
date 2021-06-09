class GameStats:
	"""Track statistics for Alien Invasion."""

	def __init__(self, ai_game):
		"""Initialize statistics."""
		self.settings = ai_game.settings
		self.reset_stats()
		# Start Alien Invasion in an active state.
		self.game_active = False

	def reset_stats(self):
		"""Initialize statistics that can chance during the game."""
		self.target_left = self.settings.target_limit