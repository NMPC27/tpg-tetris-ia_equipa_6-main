#time code
import time
from collections import Counter
start=time.time()
positions=[[2, 29], [1, 28],[4, 28],[8, 28], [1, 29], [3, 29], [4, 29], [6, 29], [3, 27], [2, 28], [3, 28], [5, 28], [6, 28], [7, 28], [8, 29], [4, 27], [5, 27], [6, 27], [7, 27], [3, 26], [4, 26], [5, 26], [6, 26], [2, 25], [3, 25], [2, 26], [2, 27], [8, 24], [6, 25], [7, 25], [8, 25]]
#new=     [[2, 29], [1, 29], [3, 29], [4, 29], [6, 29], [3, 28], [8, 29], [4, 28], [5, 28], [6, 28], [7, 28], [3, 27], [4, 27], [5, 27], [6, 27], [2, 26], [3, 26], [2, 27], [2, 28], [8, 25], [6, 26], [7, 26], [8, 26]]
#select from list of lists elements wioth x=i

    #print(i, height)

def select_x(list_of_lists, i):
    return [x for x in list_of_lists if x[0]==i] 

def get_all_columns_height(positions):
    heights=[]
    for i in range(1,9):    
        heights.append(min(select_x(positions, i), key=lambda x: x[1], default=[0,30])[1])
    return heights

#get_bumpiness
def get_bumpiness(heights):
    bumpiness=0
    for i in range(1,8):
        bumpiness+=abs(heights[i]-heights[i-1])
    return bumpiness   
    
def get_holes(heights, newpositions):
		holes = 0
		for i in range(0,8):    
			height=heights[i]
			for j in range(height,30):
				if [(i+1),j] not in newpositions:
					holes+=1
		return holes  

def get_aggregate_height(heights):
    aggregate_height=0
    for i in range(0,8):
        aggregate_height+=(30-heights[i])
    return aggregate_height 

def clear_rows(positions):
    lines = 0

    for item, count in sorted(Counter(y for _, y in positions).most_common()):
        if count == 8:
            positions = [
                [x, y + 1] if y < item else [x, y]
                for [x, y] in positions
                if y != item
            ]  # remove row and drop lines
            lines += 1
            
    return  lines, positions




# height=0
# heights=[]
# for j in range(1, 9):
#     for i in range(min_y, 30):
#         if [j,i] in positions:
#             heights.append(30 - i)
#             break
# for value in heights:
#     height += value
#print(height)
#select_x(positions, 1)
stop=time.time()
#print(get_bumpiness(positions))
(height, newpositions)= clear_rows(positions)
#print(height)

heights=get_all_columns_height(newpositions)
print(heights)
print("lines",height)
print("bumpiness", get_bumpiness(heights))
print("holes", get_holes(heights, newpositions))
print("aggregate height", get_aggregate_height(heights))

#print(stop-start)