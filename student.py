#pygame tetris AI agent
import asyncio
import getpass
import json
import os
from shape import *
import websockets
from move import *
from copy import deepcopy

peca = {
	"[[2, 2], [3, 2], [4, 2], [5, 2]]" :  I,
	"[[4, 2], [5, 2], [4, 3], [4, 4]]" :  J,
	"[[4, 2], [4, 3], [4, 4], [5, 4]]" :  L,
	"[[3, 3], [4, 3], [3, 4], [4, 4]]" :  O,
	"[[4, 2], [4, 3], [5, 3], [5, 4]]" :  S,
	"[[4, 2], [4, 3], [5, 3], [4, 4]]" :  T,
	"[[4, 2], [3, 3], [4, 3], [3, 4]]" :  Z	
}

rotacoes= {
	"[[2, 2], [3, 2], [4, 2], [5, 2]]" :  2,
	"[[4, 2], [5, 2], [4, 3], [4, 4]]" :  4,
	"[[4, 2], [4, 3], [4, 4], [5, 4]]" :  4,
	"[[3, 3], [4, 3], [3, 4], [4, 4]]" :  1,
	"[[4, 2], [4, 3], [5, 3], [5, 4]]" :  2,
	"[[4, 2], [4, 3], [5, 3], [4, 4]]" :  4,
	"[[4, 2], [3, 3], [4, 3], [3, 4]]" :  2	
}

def identify_piece(piece):
	current= peca.get(piece, None)
	rotation= rotacoes.get(piece, None)
	if current and rotation is not None:
		return Shape(current), rotation
	return None


def generateinputs(piece, position, game,inputs, new_inputs, width, height):
	new_piece=deepcopy(piece)
	new_inputs.extend(inputs)

	while isvalid(new_piece, game, width, height): #in last iteration, piece is inside wall
		new_piece.translate(-1, 0)
		new_inputs.append("a")
	new_piece.translate(1, 0)		#piece is at x=1? left most position
	
	if "a" in new_inputs: new_inputs.remove("a")

	for i in range(1,position):	#percorrer position (x) vezes este for para remover "a" extras e se necessário introduzir "d" na lista para a peça ficar na coluna certa
		if isvalid(new_piece, game, width, height):
			new_piece.translate(1, 0)
			if "a" in new_inputs : new_inputs.remove("a")
			else: new_inputs.append("d")
		else:
			new_piece.translate(-1, 0)
			if "d" in new_inputs : new_inputs.remove("d")
			else: new_inputs.append("a")
			break

	new_inputs.append("s")		# por ulitmo, mandar o input "s"

	while isvalid(new_piece, game,width,height):
			new_piece.translate(0, 1)      #put piece in the bottom most position
	new_piece.translate(0, -1)
	 
	return (new_inputs, new_piece)     #return input sequence and piece at the position led by the inputs                

def simulation(piece, rotations, game, width, height):
	keys = []
	inputs = []
	score = -10000
	for i in range(0, rotations):
		for j in range(1, width - 1):          #piece is between x=1 and x=width-1 (exclude right wall)
			new_inputs = []
			new_inputs, test_piece = generateinputs(piece, j, game,inputs, new_inputs, width, height)  #generate inputs and shape object 
																						#for piece at x = i
			#print("i ", j)
			for position in test_piece.positions:
				game.append([position[0], position[1]])       #add piece to game        
							  
			new_move = Move(game, height,width)  
			new_score = new_move.get_score()

			for position in test_piece.positions:
				game.remove([position[0], position[1]]) 

			if new_score > score:
				score=new_score
				keys = new_inputs

		piece.rotate()
		inputs.append("w")

	return keys

def isvalid(piece, game, width, height):
	for bit in piece.positions:
		if bit[0] < 1 or bit[0] >= width-1 or bit[1] >= height:
			return False
		if[bit[0], bit[1]] in game:
			return False
	return True


async def agent_loop(server_address="localhost:8000", agent_name="student"):
	async with websockets.connect(f"ws://{server_address}/player") as websocket:

		# Receive information about static game properties
		await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
		game_properties =json.loads(await websocket.recv())
		width = game_properties["dimensions"][0]
		height = game_properties["dimensions"][1]
		piece = None # Tuple will contain shape object and number of rotations 
		while True:
			keys = []
			
			try:
				state = json.loads(
					await websocket.recv()
				)  # receive game update, this must be called timely or your game will get out of sync with the server
				
				if "piece"  not in state.keys():
					continue
				
				piece = identify_piece(str(state['piece'])) 
				if piece is not None:           
					piece[0].set_pos(
					(width - piece[0].dimensions.x) / 2, 2
				)

				if piece is not None : 
					keys = simulation(piece[0], piece[1], state['game'], width, height)

					for key in keys:
						await websocket.send(json.dumps({"cmd": "key", "key": key}))  # send key command to server - you must implement this send in the AI agent
						json.loads(await websocket.recv())  # receive confirmation of key command
		
			except websockets.exceptions.ConnectionClosedOK:
				print("Server has cleanly disconnected us")
				return

			
# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
