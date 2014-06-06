# STILL TO BE DONE
# 1. NETWORK ACCESS FOR QUESTIONS
# 2. TIMER - BASIC FUNCTIONALITY WORKING - POSSIBLY ADD HARD MODE OPTION
# 3. SCORING - WORKING
# 4. SCORE TABLE - BASIC DISPLAY + SCORE CHECK + ADDING TO TABLE + NAME ENTRY DONE.  NEEDS TABLE FOR EACH SECTION.
# 5. TITLE SCREEN/CHOICES - BASIC FUNCTIONALITY WORKING, CHOICE FUNCTIONALITY TO BE DONE
# 6. BUTTON INPUT - ARDUINO LEONARDO DONE
# 7. LIVES - WORKING

import pygame, sys, os.path, wave, time, random, csv
from pygame.locals import *

# Initialisation of variables
imagedir = os.path.abspath("C:\physquiz\images") #directory path for question images
questiondir = os.path.abspath("C:\physquiz\images\questions")
questionList = set() # Make a new set for previously selected questions
questionList.add(str(0))
questionLevel = 'IB' #Placeholder - difficulty select routine goes here
questionFile = 'none' #Placeholder - default error image goes here
score = 0
lives = 0
multiplier = 1
answerDict = {}
scoresList = []
timerRunning = False
tableSelect = 1

	
# Start pygame
pygame.init()
mainsurface = pygame.display.set_mode((1024,768),pygame.FULLSCREEN) # initialise main screen
titlesurf = pygame.image.load(os.path.join(imagedir, 'title.png'))
titlerect = titlesurf.get_rect(center = (500,50))
answerfont = pygame.font.Font('freesansbold.ttf',64) # set font and size
scorefont = pygame.font.Font('freesansbold.ttf',30)

# Main routine for game
def main():
	global timerRunning
	if timerRunning == False:
		pygame.time.set_timer(pygame.USEREVENT + 2, 10000)
		timerRunning = True
	titleScreen()
	pygame.event.clear()
	while lives > 0:
		global score
		global multiplier
		global timelimit
		pygame.time.set_timer(pygame.USEREVENT + 2, 0)
		timerRunning = False
		timelimit = 60
		fillScreen((255,255,255)) # Clear screen
		mainsurface.blit(titlesurf,titlerect) # Add title image to quiz
		userAnswer = 'none' # Default to no answer
		questionPicker()
		displayBasics()
		displayLives()
		pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
		pygame.display.update()
		while userAnswer == 'none': # Wait for user input
			userAnswer = eventCheck()
		if userAnswer == 'Out of Time':
			for i in range(1,5):
				fillScreen((255,237,133)) #orange background
				textsurface = answerfont.render('Out of Time', True, (0,0,0))
				textrect = textsurface.get_rect()
				textrect.center = mainsurface.get_rect().center
				mainsurface.blit(textsurface, textrect)
				pygame.display.update()
				time.sleep(0.5)
				mainsurface.fill((255,237,133))
				pygame.display.update()
				time.sleep(0.5)
				pygame.event.clear()
				
		elif checkAnswer(questionFile,userAnswer):
			fillScreen((140,250,125)) #green background
			for i in range(1,5):
				textsurface = answerfont.render('Correct', True, (0,0,0))
				textrect = textsurface.get_rect()
				textrect.center = mainsurface.get_rect().center
				mainsurface.blit(textsurface, textrect)
				pygame.display.update()
				time.sleep(0.5)
				mainsurface.fill((140,250,125))
				pygame.display.update()
				time.sleep(0.5)
			score = score + (timelimit*multiplier) # Variable score based on time remaining
			if multiplier < 10:
				multiplier += 1
			pygame.event.clear()
		else:
			fillScreen((255,133,133)) #red background
			for i in range(1,5):
				textsurface = answerfont.render('Incorrect', True, (0,0,0))
				textrect = textsurface.get_rect()
				textrect.center = mainsurface.get_rect().center
				mainsurface.blit(textsurface, textrect)
				pygame.display.update()
				time.sleep(0.5)
				mainsurface.fill((255,133,133))
				pygame.display.update()
				time.sleep(0.5)
			multiplier = 1
			if lives == 0:
				gameOver()
			pygame.event.clear()
		pygame.event.clear(USEREVENT + 1)
	
def gameOver():
	global lives
	global score
	pygame.time.set_timer(pygame.USEREVENT + 1, 0)
	pygame.event.clear()
	fillScreen((255,255,255)) #white background
	textsurface = answerfont.render('Game Over', True, (0,0,0))
	textrect = textsurface.get_rect(center = mainsurface.get_rect().center)
	textrect = textrect.move(0,-300)
	mainsurface.blit(textsurface, textrect)
	textsurface = answerfont.render('You Scored: ' +str(score), True, (0,0,0))
	textrect = textrect.move(-60,100)
	mainsurface.blit(textsurface, textrect)
	pygame.display.update()
	checkHighScore(score)
	score = 0
	global questionList
	questionList = set()
	questionList.add(str(0))
	time.sleep(2)

def nameEntry():
	userAnswer = ''
	n=49
	name = ''
	textsurface = answerfont.render('HIGH SCORE', True, (255,0,0))
	textrect = textsurface.get_rect(center = mainsurface.get_rect().center)
	textrect = textrect.move(0,-100)
	mainsurface.blit(textsurface,textrect)
	helpsurf = pygame.image.load(os.path.join(imagedir, 'namebuttons.png'))
	helprect = helpsurf.get_rect(center = mainsurface.get_rect().center)
	helprect = helprect.move(0,255)
	mainsurface.blit(helpsurf, helprect)
	while userAnswer != 'd':
		textsurface.fill((255,255,255))
		textrect = textsurface.get_rect(center = mainsurface.get_rect().center)
		textrect = textrect.move(0, 30)
		mainsurface.blit(textsurface,textrect)
		textsurface = scorefont.render('Enter Name', True, (0,0,0))
		textrect = textsurface.get_rect(center = mainsurface.get_rect().center)
		textrect = textrect.move(0, -30)
		mainsurface.blit(textsurface,textrect)
		textsurface = scorefont.render(name + chr(n), True, (0,0,0))
		textrect = textsurface.get_rect(center = mainsurface.get_rect().center)
		textrect = textrect.move(0, 30)
		mainsurface.blit(textsurface,textrect)
		pygame.display.update()
		userAnswer = eventCheck()
		if userAnswer == 'a':
			if n < 123:
				n += 1
			else:
				n = 32
		elif userAnswer == 'b':
			if n > 32:
				n -= 1
			else:
				n = 123
		elif userAnswer == 'c':
			name = name + chr(n)
			print name
		elif userAnswer == 'd':
			return name
	
# Select random question from appropriate folder - WORKING
def questionPicker():
	global questionFile
	global questionList
	questionNumber = str(0)
	while questionNumber in questionList:
		questionNumber = str(random.randint(1,112)) # pick a random question from those available
	questionList.add(questionNumber) # add to list of selected questions
	questionFile = questionLevel + questionNumber + '.png' # generate filename to get picture
	print questionFile
	questionSurface = pygame.image.load(os.path.join(questiondir, questionLevel + "/" +questionFile)) # load question image
	questionRect = questionSurface.get_rect()
	questionRect = questionRect.move(140,180)
	mainsurface.blit(questionSurface,questionRect) # Display question

# Display current score and question number
def displayBasics():
	questionNumberSurf = scorefont.render('Question ' + str(len(questionList)-1), True, (255,0,255)) # Display question number
	questionNumberRect = questionNumberSurf.get_rect()
	questionNumberRect.center = titlerect.center
	questionNumberRect = questionNumberRect.move(0,100)
	mainsurface.blit(questionNumberSurf,questionNumberRect)
	scoresurf = scorefont.render('Score: ' +str(score), True, (255,5,5)) # Write score on screen
	scorerect = scoresurf.get_rect()
	scorerect.center = titlerect.center
	scorerect = scorerect.move(-300, 100)
	mainsurface.blit(scoresurf,scorerect)
	multisurf = scorefont.render('Streak', True, (255,5,5)) # Write streak on screen
	multirect = scoresurf.get_rect(center = mainsurface.get_rect().center)
	multirect = multirect.move(-440, -180)
	mainsurface.blit(multisurf,multirect)
	multisurf = scorefont.render('x' +str(multiplier), True, (255,5,5)) # Write streak number on screen
	multirect = scoresurf.get_rect(center = mainsurface.get_rect().center)
	multirect = multirect.move(-410, -145)
	mainsurface.blit(multisurf,multirect)
	
# Lives Display
def displayLives():
	lifeSurf = pygame.image.load(os.path.join(imagedir, str(lives)+'hearts.png'))
	lifeRect = lifeSurf.get_rect(center = mainsurface.get_rect().center)
	lifeRect = lifeRect.move(450,-90)
	mainsurface.blit(lifeSurf,lifeRect)
		

# Check for quit or user input - WORKING
def eventCheck():
	userAnswer = 'none'
	for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				userAnswer = chr(event.key) # change unicode into letter
			elif event.type == pygame.USEREVENT + 1:
				userAnswer = timedown()
			elif event.type == pygame.USEREVENT + 2:
				scoreTable()
	return userAnswer

# Countdown timer and screen updater	
def timedown():
	global lives
	global timelimit
	if timelimit > 0:
		timelimit -= 1
		timesurf = scorefont.render('Time:' +str(timelimit), True, (255,0,0))
		timerect = timesurf.get_rect()
		timerect.center = titlerect.center
		timerect = timerect.move(300,100)
		mainsurface.blit(timesurf,timerect)
		pygame.display.update()
		timesurf.fill((255,255,255))
		mainsurface.blit(timesurf,timerect)
		print timelimit
		return 'none'
	else:
		lives -= 1
		return 'Out of Time'
		
# Compare user input with correct answer - WORKING
def checkAnswer(question,answer):
	global lives
	rightAnswer = answerDict[question]
	print rightAnswer
	if answer == rightAnswer:
		return True
	else: 
		lives -= 1
		return False
	
def titleScreen():
	global lives
	global questionLevel
	mainsurface.fill((255,255,255))# Clear screen
	mainsurface.blit(titlesurf,titlerect) # Add title image to quiz
	choiceSurf = scorefont.render('Select Level', True, (0,0,0))
	choiceRect = choiceSurf.get_rect(center = mainsurface.get_rect().center)
	choiceRect = choiceRect.move(0,-100)
	mainsurface.blit(choiceSurf, choiceRect)
	buttonSurf = pygame.image.load(os.path.join(imagedir,'newbuttons.png'))
	buttonRect = buttonSurf.get_rect(center = mainsurface.get_rect().center)
	buttonRect = buttonRect.move(0,100)
	mainsurface.blit(buttonSurf,buttonRect)
	pygame.display.update()
	userInput = eventCheck()
	if userInput == 'none':
		userInput = eventCheck()
	if userInput == 'a':
		fillScreen((255,255,255)) # Clear screen
		lives = 3
		questionLevel = 'IB'
		#Create answer dictionary
		with open('C:/physquiz/data/IBanswers.csv','rb') as answersFile:
			answerReader = csv.reader(answersFile)
			for row in answerReader:
				answerDict[row[0]] = row[1]
	if userInput == 'b':
		fillScreen((255,255,255)) # Clear screen
		lives = 3
		questionLevel = 'IGCSE'
		#Create answer dictionary
		with open('C:/physquiz/data/IGCSEanswers.csv','rb') as answersFile:
			answerReader = csv.reader(answersFile)
			for row in answerReader:
				answerDict[row[0]] = row[1]
		
def fillScreen(colour):
	for i in range(0,50):
		downsurf = pygame.Surface((1024,i*8))
		downrect = downsurf.get_rect()
		downsurf.fill((colour))
		mainsurface.blit(downsurf,downrect)
		upsurf = pygame.Surface((1024,i*8))
		uprect = upsurf.get_rect()
		uprect = uprect.move(0,768-i*8)
		upsurf.fill((colour))
		mainsurface.blit(upsurf,uprect)
		pygame.display.update()

#Check if player score should add to the table
def checkHighScore(playerscore):
	scorelist = sorted(scoresList, reverse = True)
	print min(scorelist)
	if playerscore > min(scorelist)[0]:
		name = nameEntry()
		addScore(playerscore, name)
		
#Ask for name and add to score table
def addScore(score,name):
	global scoresList
	scorelist = sorted(scoresList, reverse = True)
	scorelist.pop()
	print scorelist
	with open('C:/physquiz/data/highscores.csv','wb') as scoresFile:
		scoresWriter = csv.writer(scoresFile)
		for things in scorelist:
			scoresWriter.writerow([things[0]]+[things[1]])
		print 'adding score'
		scoresWriter.writerow([str(score)]+[name])
	scoresList = []
	with open('C:/physquiz/data/highscores.csv','rb') as highScoresFile:
		HSReader = csv.reader(highScoresFile)
		for row in HSReader:
			scoresList.append((int(row[0]),row[1]))
	
#Display high score table
def scoreTable():
	#Display Stuff Here
	global tableSelect
	global timerRunning
	currentTable = ''
	if tableSelect == 1:
		currentTable = 'IB'
		tableSelect = 2
	elif tableSelect == 2:
		currentTable = 'IGCSE'
		tableSelect = 1
	global scoresList
	scoresList = []
	#Import high score table
	with open('C:/physquiz/data/' +currentTable +'highscores.csv','rb') as highScoresFile:
		HSReader = csv.reader(highScoresFile)
		for row in HSReader:
			scoresList.append((int(row[0]),row[1]))
	timerRunning = False
	pygame.time.set_timer(pygame.USEREVENT + 2, 0)
	scorelist = sorted(scoresList, reverse = True)
	y = 2
	fillScreen((0,0,0))
	scoreSurf = answerfont.render(currentTable + ' HIGH SCORES', True, (255,0,0))
	scoreRect = scoreSurf.get_rect()
	if tableSelect == 1:
		scoreRect = scoreRect.move(200, 0)
	elif tableSelect == 2:
		scoreRect = scoreRect.move(250, 0)
	mainsurface.blit(scoreSurf,scoreRect)
	for things in scorelist:
		y += 1
		scoreSurf = scorefont.render(things[1], True, (255,0,0))
		scoreRect = scoreSurf.get_rect()
		scoreRect = scoreRect.move(200, 50*y)
		mainsurface.blit(scoreSurf,scoreRect)	
		scoreSurf = scorefont.render(str(things[0]), True, (255,0,0))
		scoreRect = scoreSurf.get_rect()
		scoreRect = scoreRect.move(700, 50*y)
		mainsurface.blit(scoreSurf,scoreRect)
	pygame.display.update()
	time.sleep(5)
	fillScreen((255,255,255))
	pygame.display.update()

while True:
	main()
