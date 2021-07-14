import matplotlib.pyplot as plt

EXTREME_REAR = -32768
EXTREME_FRONT = 32767

class Projector:

	def dissociate(self, frames):
		# TODO: format-specific
		for frame in frames:
			plt.scatter(frame['x'], frame['y'], s=3)
			plt.scatter(frame['x'], frame['y']-EXTREME_FRONT, s=3)
			plt.scatter(frame['x']-EXTREME_REAR, frame['y'], c='black', s=1)
			plt.scatter(frame['x']-9999, frame['y']-9999, c='orange', s=.5)
		plt.show()