import pygame
import math
import random

# Introduction print statements

print("*"*40)
print("WELCOME TO BIRD SWARM!")
print("*"*40)

print("-"*250)
print ("PROGRAM DESCRIPTION:")
print("\nThis program uses Pygame in order to show a visual of two arlgorithms, swarm algorithm and bird flocking algorithm."
      "\nA leader bird is created and then other birds are added onto the flock in a swarm manner along with a secondary leader bird."
      "\nThere is also palm tree obsticles that make the birds bounce back and slow down. "
      "\nThis algorithm could be used for plenty of things like showcasing how birds interact with their environment to being used with drones to keep them all together"
      "in a swarm.")
print("-"*250)

print("-"*250)
print("PROGRAM LEGEND:")
print("Birds: White circles"
      "\nPalm Trees: Green circles")
print("-"*250)
input("\n\nPress enter to start the bird flock simulation....")

# Initializing pygame which is what our algorithm is going to use as a visual
pygame.init()

# Image used for our background
bg = pygame.image.load("bg.png")

# Setting the width and height of the screen
WIDTH = 1200
HEIGHT = 600

# Sets the center of where the birds will stay around to which is the width and height divided by two
CENTREX = WIDTH / 2
CENTREY = HEIGHT / 2

# Setting the max number of birds
NUMBEROFBIRDS = 200

# Setting the maximum speed, speed of spreading and the positional spread distance of the birds
POSITIONSPREAD = 15000
SPEEDSPREAD = 1
MAXSPEED = 6

# Dimensions for the border
BORDER = 10
LEADERBORDER = 200
BORDERSPEEDCHANGE = 6

# Setting for minimum distance
MINDIST = 10.0
MATCHSPEEDWINDOW = 40.0

# Sets the speed of the leader bird
LEADERBIRDRANDOMSPEEDCHANGE = 6
LEADERMAXSPEED = 10.0

# Barrier dimensions which will act as obstacles for the birds
barriers = [[50, 100], [475, 500], [100, 250], [75, 150], [300, 515], [600, 200], [675, 900], [700, 400], [400, 900],
            [200, 520]]

# The radius of the barriers
BARRIERRADIUS = 20

# Size of the pygame screen
size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)

# Makes the mouse cursor invisible
pygame.mouse.set_visible(0)

# Array of birds
birdlist = []

# Creates a leader bird in a pre set x and y axys
leaderbirdx = 300.0
leaderbirdy = 300.0
leaderbirdvx = 5.0
leaderbirdvy = 0.0

# i will be the number of birds at the start and will increase
i = 0

# While loop for when number of birds is less than i which will increase the number of birds
while (i < NUMBEROFBIRDS):
    x = random.uniform(CENTREX - POSITIONSPREAD, CENTREX + POSITIONSPREAD)
    y = random.uniform(CENTREY - POSITIONSPREAD, CENTREY + POSITIONSPREAD)
    vx = random.uniform(-SPEEDSPREAD, SPEEDSPREAD)
    vy = random.uniform(-SPEEDSPREAD, SPEEDSPREAD)

    newbird = [x, y, vx, vy]

    birdlist.append(newbird)
    i += 1

# While loop for the starter bird which is a leader bird
while (1):
    screen.fill((0, 0, 0))
    screen.blit(bg, (0,0))

    # Changes the leader bird location and speed
    if (leaderbirdx < LEADERBORDER):
        leaderbirdvx += BORDERSPEEDCHANGE
    if (leaderbirdy < LEADERBORDER):
        leaderbirdvy += BORDERSPEEDCHANGE
    if (leaderbirdx > WIDTH - LEADERBORDER):
        leaderbirdvx -= BORDERSPEEDCHANGE
    if (leaderbirdy > HEIGHT - LEADERBORDER):
        leaderbirdvy -= BORDERSPEEDCHANGE

    # Creates the leader bird
    leaderbirdvx += random.uniform(-LEADERBIRDRANDOMSPEEDCHANGE, LEADERBIRDRANDOMSPEEDCHANGE)
    leaderbirdvy += random.uniform(-LEADERBIRDRANDOMSPEEDCHANGE, LEADERBIRDRANDOMSPEEDCHANGE)

    # Seeting the maximum speed
    speed = math.sqrt(leaderbirdvx * leaderbirdvx + leaderbirdvy * leaderbirdvy)
    if (speed > LEADERMAXSPEED):
        leaderbirdvx = leaderbirdvx * LEADERMAXSPEED / speed
        leaderbirdvy = leaderbirdvy * LEADERMAXSPEED / speed

    leaderbirdx += leaderbirdvx
    leaderbirdy += leaderbirdvy

    # Creates birds, gives them a position and speed
    i = 0
    while (i < NUMBEROFBIRDS):

        # Makes a list of birds
        x = birdlist[i][0]
        y = birdlist[i][1]
        vx = birdlist[i][2]
        vy = birdlist[i][3]



        # Draws circles using pygame
        pygame.draw.circle(screen, (245,245,245), (int(x), int(y)), 6, 0)

        # Defines what happens when birds collide with borders
        if (x < BORDER):
            vx += BORDERSPEEDCHANGE
        if (y < BORDER):
            vy += BORDERSPEEDCHANGE
        if (x > WIDTH - BORDER):
            vx -= BORDERSPEEDCHANGE
        if (y > HEIGHT - BORDER):
            vy -= BORDERSPEEDCHANGE

        # Birds will follow the leader bird
        leaderdiffx = leaderbirdx - x
        leaderdiffy = leaderbirdy - y
        vx += 0.007 * leaderdiffx
        vy += 0.007 * leaderdiffy

        # Used to move away from other birds to simulate flocking
        j = 0

        #  Used to calculate the speed of the other surrounding birds
        avxtotal = 0
        avytotal = 0
        avcount = 0
        while (j < NUMBEROFBIRDS):

            if (j != i):
                dx = birdlist[j][0] - x
                dy = birdlist[j][1] - y
                dist = math.sqrt(dx * dx + dy * dy)
                if (dist < MINDIST):
                    vx -= dx * 0.2
                    vy -= dy * 0.2
                if (dist < MATCHSPEEDWINDOW):
                    avxtotal += birdlist[j][2]
                    avytotal += birdlist[j][3]
                    avcount += 1
            j += 1

        # Lets birds copy the same speed of birds around them
        if (avcount != 0):
            avx = avxtotal / avcount
            avy = avytotal / avcount
            vx = 0.9 * vx + 0.1 * avx
            vy = 0.9 * vy + 0.1 * avy

        # If bird collides with barrier, slow down and move away
        for barrier in barriers:
            dx = barrier[0] - x
            dy = barrier[1] - y
            dist = math.sqrt(dx * dx + dy * dy)
            if (dist < BARRIERRADIUS + 15):
                vx -= dx * 0.1
                vx *= 0.6
                vy -= dy * 0.1
                vy *= 0.6

        # Setting max speed
        speed = math.sqrt(vx * vx + vy * vy)
        if (speed > MAXSPEED):
            vx = vx * MAXSPEED / speed
            vy = vy * MAXSPEED / speed

        # Sets the current positions according to the current speed
        birdlist[i][0] += vx
        birdlist[i][1] += vy
        birdlist[i][2] = vx
        birdlist[i][3] = vy
        i += 1

    # Uses  pygame to draw circles and create barriers
    for barrier in barriers:
        pygame.draw.circle(screen, (102,205,0),(int(barrier[0]), int(barrier[1])), BARRIERRADIUS, 0)

    # Updates the pygame screen when i is increased by 1
    pygame.display.flip()
    i += 1