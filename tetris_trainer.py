from pygame.constants import K_LEFT
from pygame_trainer import PyGamePlayer, function_intercept
import games.tetris
import pygame


class TetrisPlayer(PyGamePlayer):
	def __init__(self):
		"""
		Example class for playing Tetris
		"""
		super(TetrisPlayer, self).__init__(force_game_fps=8)
		self._toggle_down_key = True
		self._new_reward = 0.0
		self._terminal = False

		def add_removed_lines_to_reward(lines_removed, *args, **kwargs):
			self._new_reward += lines_removed
			return lines_removed

		def check_for_game_over(ret, text):
			if text == 'Game Over':
				self._terminal = True

		# to get the reward we will intercept the removeCompleteLines method and store what it returns
		games.tetris.removeCompleteLines = function_intercept(games.tetris.removeCompleteLines,
															  add_removed_lines_to_reward)
		# find out if we have had a game over
		games.tetris.showTextScreen = function_intercept(games.tetris.showTextScreen,
														 check_for_game_over)

		def print_keys(event, *args, **kwargs):
			if not event is None:
				for e in event:
					try:
						print e.key
					except:
						None	
			return event	
			
		pygame.event.get = function_intercept(pygame.event.get,
														 print_keys)   

	def get_feedback(self):
		temp = self._new_reward
		self._new_reward = 0.0
		terminal = self._terminal
		self._terminal = False
		return temp, terminal

	def start(self):
		super(TetrisPlayer, self).start()

		#games.tetris.main()
		games.tetris.main(screenwidth=640, screenheight=480, frames_per_second=8)

if __name__ == '__main__':
	player = TetrisPlayer()
	player.start()
