from collections import Counter

class Move:
	def __init__(self, game, game_height, game_width) -> None:
		self.game = game
		self.game_height = game_height
		self.game_width = game_width

	def select_x(self,list_of_lists, i):
		return [x for x in list_of_lists if x[0]==i] 

	def get_all_columns_height(self):
		heights=[]
		for i in range(1,self.game_width-1):    
			heights.append(min(self.select_x(self.game, i), key=lambda x: x[1], default=[0,30])[1])
		return heights

	def get_bumpiness(self,heights):
		bumpiness=0
		for i in range(1,self.game_width-2):
			bumpiness+=abs(heights[i]-heights[i-1])
		return bumpiness   
		
	def get_holes(self, heights):
			holes = 0
			for i in range(0,8):    
				height=heights[i]
				for j in range(height,self.game_height):
					if [(i+1),j] not in self.game:
						holes+=1
			return holes  

	def get_aggregate_height(self,heights):
		aggregate_height=0
		for i in range(0,self.game_width-2):
			aggregate_height+=(self.game_height-heights[i])
		return aggregate_height 

	def clear_rows(self):
		lines = 0

		for item, count in sorted(Counter(y for _, y in self.game).most_common()):
			if count == self.game_width-2:
				self.game = [
					[x, y + 1] if y < item else [x, y]
					for [x, y] in self.game
					if y != item
				]  # remove row and drop lines
				lines += 1
				
		return  lines
	def get_score(self):
		
		lines = self.clear_rows()
		heights=self.get_all_columns_height()

		a=-0.51
		b=0.76
		c=-0.35
		d=-0.18

		score =( (a *self.get_aggregate_height(heights))+ (b*lines) + (c * self.get_holes(heights))+ (d * self.get_bumpiness(heights)))

		return score