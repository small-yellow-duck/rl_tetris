# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys
import numpy as np
from pygame.locals import *


FPS = 8

WINDOWWIDTH = 640
WINDOWHEIGHT = 480

BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = ''

scale = (1.0e11)
MOVESIDEWAYSFREQ = 0.1 #*30/FPS/scale #0.15
MOVEDOWNFREQ = 0.1 #*30/FPS/scale #0.1


XMARGIN = 0 #int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = 0 #WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#				R	 G	  B
WHITE		= (255, 255, 255)
GRAY		= (185, 185, 185)
BLACK		= (	 0,	  0,   0)
RED			= (155,	  0,   0)
LIGHTRED	= (175,	 20,  20)
GREEN		= (	 0, 155,   0)
LIGHTGREEN	= ( 20, 175,  20)
BLUE		= (	 0,	  51, 255)
LIGHTBLUE	= ( 51,	 51, 175)
YELLOW		= (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
ORANGE		= (255, 102,   0)
LIGHTORANGE		= (255, 102,   0)
PURPLE		= (153, 51, 255)
LIGHTPURPLE		 = (178, 102, 255)
CYAN = (0, 255, 255)
LIGHTCYAN = (102, 255, 255)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS		= (		BLUE,	   GREEN,	   RED,		 YELLOW, ORANGE, PURPLE, CYAN)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW, LIGHTORANGE, LIGHTPURPLE, LIGHTCYAN)

assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = np.array([[['','','','',''],
					 ['','','','',''],
					 ['','','O','O',''],
					 ['','O','O','',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','O','',''],
					 ['','','O','O',''],
					 ['','','','O',''],
					 ['','','','','']]])

Z_SHAPE_TEMPLATE = np.array([[['','','','',''],
					 ['','','','',''],
					 ['','O','O','',''],
					 ['','','O','O',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','O','',''],
					 ['','O','O','',''],
					 ['','O','','',''],
					 ['','','','','']]])

I_SHAPE_TEMPLATE = np.array([[['','','O','',''],
					 ['','','O','',''],
					 ['','','O','',''],
					 ['','','O','',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','','',''],
					 ['O','O','O','O',''],
					 ['','','','',''],
					 ['','','','','']]])

O_SHAPE_TEMPLATE = np.array([[['','','','',''],
					 ['','','','',''],
					 ['','O','O','',''],
					 ['','O','O','',''],
					 ['','','','','']]])

J_SHAPE_TEMPLATE = np.array([[['','','','',''],
					 ['','O','','',''],
					 ['','O','O','O',''],
					 ['','','','',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','O','O',''],
					 ['','','O','',''],
					 ['','','O','',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','','',''],
					 ['','O','O','O',''],
					 ['','','','O',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','O','',''],
					 ['','','O','',''],
					 ['','O','O','',''],
					 ['','','','','']]])

L_SHAPE_TEMPLATE = np.array([[['','','','',''],
					 ['','','','O',''],
					 ['','O','O','O',''],
					 ['','','','',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','O','',''],
					 ['','','O','',''],
					 ['','','O','O',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','','',''],
					 ['','O','O','O',''],
					 ['','O','','',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','O','O','',''],
					 ['','','O','',''],
					 ['','','O','',''],
					 ['','','','','']]])

T_SHAPE_TEMPLATE = np.array([[['','','','',''],
					 ['','','O','',''],
					 ['','O','O','O',''],
					 ['','','','',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','O','',''],
					 ['','','O','O',''],
					 ['','','O','',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','','',''],
					 ['','O','O','O',''],
					 ['','','O','',''],
					 ['','','','','']],
					[['','','','',''],
					 ['','','O','',''],
					 ['','O','O','',''],
					 ['','','O','',''],
					 ['','','','','']]])
					 


PIECES = {'S': S_SHAPE_TEMPLATE,
		  'Z': Z_SHAPE_TEMPLATE,
		  'J': J_SHAPE_TEMPLATE,
		  'L': L_SHAPE_TEMPLATE,
		  'I': I_SHAPE_TEMPLATE,
		  'O': O_SHAPE_TEMPLATE,
		  'T': T_SHAPE_TEMPLATE}

PIECES_COLORS = {'S': GREEN,
		  'Z': RED,
		  'J': BLUE,
		  'L': ORANGE,
		  'I': CYAN,
		  'O': YELLOW,
		  'T': PURPLE}


def main(screenwidth=640, screenheight=480, frames_per_second=2):
	global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
	global XMARGIN, TOPMARGIN, WINDOWWIDTH, WINDOWHEIGHT, FPS, MOVESIDEWAYSFREQ, MOVEDOWNFREQ
	FPS = frames_per_second
	WINDOWWIDTH = screenwidth
	WINDOWHEIGHT = screenheight
	
	MOVESIDEWAYSFREQ = 0.15 #*30/FPS/scale
	MOVEDOWNFREQ = 0.1 #*30/FPS/scale

	XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
	TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5
	
	score = 0
	
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', int(18))
	BIGFONT = pygame.font.Font('freesansbold.ttf', int(100))
	pygame.display.set_caption('Tetromino')

	showTextScreen('Tetromino')
	while True: # game loop
		#if random.randint(0, 1) == 0:
		#	 pygame.mixer.music.load('tetrisb.mid')
		#else:
		#	 pygame.mixer.music.load('tetrisc.mid')
		#pygame.mixer.music.play(-1, 0.0)
		run()
		#pygame.mixer.music.stop()
		showTextScreen('Game Over')


def run():
	# setup variables for the start of the game
	board = getBlankBoard()
	lastMoveDownTime = time.time()
	lastMoveSidewaysTime = time.time()
	lastFallTime = time.time()
	movingDown = False # note: there is no movingUp variable
	movingLeft = False
	movingRight = False
	score = 0
	level, fallFreq = calculateLevelAndFallFreq(score)

	fallingPiece = getNewPiece()
	nextPiece = getNewPiece()

	while True: # game loop
		if fallingPiece == None:
			# No falling piece in play, so start a new piece at the top
			fallingPiece = nextPiece
			nextPiece = getNewPiece()
			lastFallTime = time.time() # reset lastFallTime

			if not isValidPosition(board, fallingPiece):
				return # can't fit a new piece on the board, so game over

		checkForQuit()
		for event in pygame.event.get(): # event handling loop
			if event.type == KEYUP:
				if (event.key == K_p):
					# Pausing the game
					DISPLAYSURF.fill(BGCOLOR)
					pygame.mixer.music.stop()
					showTextScreen('Paused') # pause until a key press
					pygame.mixer.music.play(-1, 0.0)
					lastFallTime = time.time()
					lastMoveDownTime = time.time()
					lastMoveSidewaysTime = time.time()
				elif (event.key == K_LEFT or event.key == K_a):
					movingLeft = False
				elif (event.key == K_RIGHT or event.key == K_d):
					movingRight = False
				elif (event.key == K_DOWN or event.key == K_s):
					movingDown = False

			elif event.type == KEYDOWN:
				# moving the piece sideways
				if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
					fallingPiece['x'] -= 1
					movingLeft = True
					movingRight = False
					lastMoveSidewaysTime = time.time()

				elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
					fallingPiece['x'] += 1
					movingRight = True
					movingLeft = False
					lastMoveSidewaysTime = time.time()

				# rotating the piece (if there is room to rotate)
				elif (event.key == K_UP or event.key == K_w):
					fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % PIECES[fallingPiece['shape']].shape[0]
					if not isValidPosition(board, fallingPiece):
						fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % PIECES[fallingPiece['shape']].shape[0]
				elif (event.key == K_q): # rotate the other direction
					fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % PIECES[fallingPiece['shape']].shape[0]
					if not isValidPosition(board, fallingPiece):
						fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % PIECES[fallingPiece['shape']].shape[0]

				# making the piece fall faster with the down key
				elif (event.key == K_DOWN or event.key == K_s):
					movingDown = True
					if isValidPosition(board, fallingPiece, adjY=1):
						fallingPiece['y'] += 1
					lastMoveDownTime = time.time()

				# move the current piece all the way down
				elif event.key == K_SPACE:
					movingDown = False
					movingLeft = False
					movingRight = False
					for i in range(1, BOARDHEIGHT):
						if not isValidPosition(board, fallingPiece, adjY=i):
							break
					fallingPiece['y'] += i - 1

		# handle moving the piece because of user input
		if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
			if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
				fallingPiece['x'] -= 1
			elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
				fallingPiece['x'] += 1
			lastMoveSidewaysTime = time.time()

		if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
			fallingPiece['y'] += 1
			lastMoveDownTime = time.time()

		# let the piece fall if it is time to fall
		if time.time() - lastFallTime > fallFreq:
			# see if the piece has landed
			if not isValidPosition(board, fallingPiece, adjY=1):
				# falling piece has landed, set it on the board
				addToBoard(board, fallingPiece)
				score += removeCompleteLines(board)
				level, fallFreq = calculateLevelAndFallFreq(score)
				fallingPiece = None
			else:
				# piece did not land, just move the piece down
				fallingPiece['y'] += 1
				lastFallTime = time.time()

		# drawing everything on the screen
		DISPLAYSURF.fill(BGCOLOR)
		drawBoard(board)
		drawStatus(score, level)
		drawNextPiece(nextPiece)#Here
		if fallingPiece != None:
			drawPiece(fallingPiece)

		pygame.display.update()

		FPSCLOCK.tick(FPS)



def makeTextObjs(text, font, color):
	surf = font.render(text, True, color)
	return surf, surf.get_rect()


def terminate():
	pygame.quit()
	sys.exit()


def checkForKeyPress():
	# Go through event queue looking for a KEYUP event.
	# Grab KEYDOWN events to remove them from the event queue.
	checkForQuit()

	for event in pygame.event.get([KEYDOWN, KEYUP]):
		if event.type == KEYDOWN:
			continue
		return event.key
	return None


def showTextScreen(text):
	# This function displays large text in the
	# center of the screen until a key is pressed.
	# Draw the text drop shadow
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
	DISPLAYSURF.blit(titleSurf, titleRect)

	# Draw the text
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
	DISPLAYSURF.blit(titleSurf, titleRect)

	# Draw the additional "Press a key to play." text.
	pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play or ESC to quit.', BASICFONT, TEXTCOLOR)
	pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

	while checkForKeyPress() == None:
		pygame.display.update()
		FPSCLOCK.tick()


def checkForQuit():
	for event in pygame.event.get(QUIT): # get all the QUIT events
		terminate() # terminate if any QUIT events are present
	for event in pygame.event.get(KEYUP): # get all the KEYUP events
		if event.key == K_ESCAPE:
			terminate() # terminate if the KEYUP event was for the Esc key
		pygame.event.post(event) # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
	# Based on the score, return the level the player is on and
	# how many seconds pass until a falling piece falls one space.
	level = int(score / 10) + 1
	fallFreq = 0.27 #/FPS/scale #- (level * 0.02)
	
	return level, fallFreq

def getNewPiece():
	# return a random new piece in a random rotation and color
	shape = random.choice(list(PIECES.keys()))
	newPiece = {'shape': shape,
				'rotation': random.randint(0, PIECES[shape].shape[0] - 1),
				'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
				'y': -2, # start it above the board (i.e. less than 0)
				'color': COLORS.index(PIECES_COLORS[shape])} #random.randint(0, len(COLORS)-1)}
	return newPiece



def addToBoard(board, piece):
	# fill in the board based on piece's location, shape, and rotation
	
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if PIECES[piece['shape']][piece['rotation']][x,y] != '':
				try:
					board[x + piece['x'], y + piece['y']] = piece['color']
				except:
					print('outside board', y + piece['y'])	
	
	
	
	'''
	left = np.where(np.sum(PIECES[piece['shape']][piece['rotation']] != '', axis=1) > 0)[0][0] 
	right = np.where(np.sum(PIECES[piece['shape']][piece['rotation']] != '', axis=1) > 0)[0][-1] + 1
	top = np.where(np.sum(PIECES[piece['shape']][piece['rotation']] != '', axis=0) > 0)[0][0] 
	bottom = np.where(np.sum(PIECES[piece['shape']][piece['rotation']] != '', axis=0) > 0)[0][-1] +1
	
	try:
		miny = piece['y']+top#np.max([0, piece['y']+top])
		top2 = -piece['y'] +miny
		p = PIECES[piece['shape']][piece['rotation']][left:right, top2:bottom]
		np.place(p, p != '' , piece['color'])
		print p
		board[piece['x']+left:piece['x']+right, miny:piece['y']+bottom] = np.core.defchararray.add(board[piece['x']+left:piece['x']+right, miny:piece['y']+bottom], p)				
		print board[piece['x']+left:piece['x']+right, miny:piece['y']+bottom]
		print ''

	except:
		print 'outside board'
	'''	
			

def getBlankBoard():
	# create and return a new blank board data structure
	board = np.array(BOARDWIDTH*BOARDHEIGHT*['']).reshape((BOARDWIDTH, BOARDHEIGHT))
	return board
	



def isValidPosition(board, piece, adjX=0, adjY=0):
	# Return True if the piece is within the board and not colliding
	
	left = np.where(np.sum(PIECES[piece['shape']][piece['rotation']] != '', axis=1) > 0)[0][0] 
	right = np.where(np.sum(PIECES[piece['shape']][piece['rotation']] != '', axis=1) > 0)[0][-1] + 1
	top = np.where(np.sum(PIECES[piece['shape']][piece['rotation']] != '', axis=0) > 0)[0][0] 
	bottom = np.where(np.sum(PIECES[piece['shape']][piece['rotation']] != '', axis=0) > 0)[0][-1] +1
	
	if (piece['x']+ adjX + left) >= 0 and (piece['x'] + adjX + right) <= BOARDWIDTH and (piece['y']+ adjY + bottom) <= BOARDHEIGHT: #adjY+top >= 0 and
		miny = np.max([piece['y']+ adjY +top, 0])
		miny2 = -piece['y'] - adjY + miny
		t = (board[piece['x']+ adjX +left:piece['x']+ adjX +right, miny:piece['y']+ adjY +bottom] != '') * ( PIECES[piece['shape']][piece['rotation']][left:right, miny2:bottom] != '')
		if np.sum(t) == 0:
			return True
		else:
			return False
	else:
		return False




def removeCompleteLines(board):
	# Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
	cleared_lines = np.sum(board == '', axis=0) == 0
	print cleared_lines
	numLinesRemoved = np.sum(cleared_lines)
	
	
	board[:, numLinesRemoved:] =  board[:, cleared_lines!=True]
	board[:, 0:numLinesRemoved] = np.array((BOARDWIDTH*numLinesRemoved*[''])).reshape((BOARDWIDTH, numLinesRemoved))
	
	return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
	# Convert the given xy coordinates of the board to xy
	# coordinates of the location on the screen.
	return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
	# draw a single box (each tetromino piece has four boxes)
	# at xy coordinates on the board. Or, if pixelx & pixely
	# are specified, draw to the pixel coordinates stored in
	# pixelx & pixely (this is used for the "Next" piece).
	if color == BLANK:
		return
		
	if pixelx == None and pixely == None:
		pixelx, pixely = convertToPixelCoords(boxx, boxy)
	color = int(color)
	pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
	pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
	# draw the border around the board
	pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

	# fill the background of the board
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
	# draw the individual boxes on the board
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			drawBox(x, y, board[x, y])


def drawStatus(score, level):
	# draw the score text
	scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - int(150.0), int(20.0))
	DISPLAYSURF.blit(scoreSurf, scoreRect)

	# draw the level text
	levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.topleft = (WINDOWWIDTH - int(150.0), int(50.0))
	DISPLAYSURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
	shapeToDraw = PIECES[piece['shape']][piece['rotation']]
	if pixelx == None and pixely == None:
		# if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
		pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

	# draw each of the boxes that make up the piece
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if shapeToDraw[x, y] != BLANK:
				drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
	# draw the "next" text
	nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
	nextRect = nextSurf.get_rect()
	nextRect.topleft = (WINDOWWIDTH - int(120.0), int(80.0))
	DISPLAYSURF.blit(nextSurf, nextRect)
	# draw the "next" piece
	drawPiece(piece, pixelx=WINDOWWIDTH-int(120.0), pixely=int(100.0))


if __name__ == '__main__':
	main(screenwidth=640, screenheight=480, frames_per_second=8)
