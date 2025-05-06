import tkinter as tk
import random
import winsound
from PIL import Image, ImageTk, ImageEnhance
import os

# Create the main window
root = tk.Tk()
root.title("PRATHIU MAN GAME")

# Set the dimensions of the window
root.geometry("800x600")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Load and adjust the background image from the Documents directory
documents_path = os.path.join(os.path.expanduser("~"), "Documents")
image_path = os.path.join(documents_path, "rocky.jpg")  # Update this with your image file name
background_image = Image.open(image_path)

# Resize the image to fit the canvas
background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)

# Adjust the brightness of the image
enhancer = ImageEnhance.Brightness(background_image)
background_image = enhancer.enhance(0.5)  # Adjust the intensity (0.5 for less intensity)
background_photo = ImageTk.PhotoImage(background_image)

# Add the background image to the canvas
canvas.create_image(0, 0, image=background_photo, anchor=tk.NW)

# Create road and lane markings
road = canvas.create_rectangle(200, 0, 600, 600, fill="darkgrey")
lane_markings = []
for i in range(0, 600, 40):
    lane_marking = canvas.create_rectangle(395, i, 405, i+20, fill="white")
    lane_markings.append(lane_marking)

# Create trees on the sides of the road
trees = []
for i in range(0, 600, 100):
    # Tree on the left side
    trunk_left = canvas.create_rectangle(160, i, 170, i+30, fill="brown")
    leaves_left = canvas.create_oval(140, i-20, 190, i+20, fill="green")
    trees.append((trunk_left, leaves_left))
    
    # Tree on the right side
    trunk_right = canvas.create_rectangle(630, i, 640, i+30, fill="brown")
    leaves_right = canvas.create_oval(610, i-20, 660, i+20, fill="green")
    trees.append((trunk_right, leaves_right))

# Create a man using multiple shapes
head = canvas.create_oval(380, 470, 420, 510, fill="peachpuff")
body = canvas.create_rectangle(370, 510, 430, 570, fill="blue")
left_arm = canvas.create_rectangle(350, 510, 370, 550, fill="blue")
right_arm = canvas.create_rectangle(430, 510, 450, 550, fill="blue")
left_leg = canvas.create_rectangle(370, 570, 390, 610, fill="black")
right_leg = canvas.create_rectangle(410, 570, 430, 610, fill="black")

# Group the man parts together
man_parts = [head, body, left_arm, right_arm, left_leg, right_leg]

# Load car images
car_images = []
car_image_paths = ["car1.png", "car2.png", "car3.png"]  # Update these with your car image file names
for car_image_path in car_image_paths:
    car_image = Image.open(os.path.join(documents_path, car_image_path))
    car_image = car_image.resize((40, 40), Image.Resampling.LANCZOS)
    car_images.append(ImageTk.PhotoImage(car_image))

# Create obstacles (balls and cars) on the canvas
obstacles = []
for _ in range(5):
    x = random.randint(220, 580)
    y = random.randint(-400, -20)
    '''if random.choice([True, False]):
        # Create a colorful ball
        color = random.choice(["red", "blue", "green", "yellow", "purple"])
        obstacle = canvas.create_oval(x, y, x+20, y+20, fill=color)
    else:'''
        # Create a random car
    car_image = random.choice(car_images)
    obstacle = canvas.create_image(x, y, image=car_image)
    obstacles.append(obstacle)

# Initialize score and game over flag
score = 0
game_over_flag = False
score_text = canvas.create_text(700, 50, text=f"Score: {score}", font=("Arial", 16), fill="black")
game_over_text = None

# Function to move the man
def move_man(event):
    if not game_over_flag:
        if event.keysym == 'Left':
            for part in man_parts:
                canvas.move(part, -10, 0)
        elif event.keysym == 'Right':
            for part in man_parts:
                canvas.move(part, 10, 0)
        elif event.keysym == 'Down':
            for part in man_parts:
                canvas.move(part, 0, 10)
        elif event.keysym == 'Up':
            for part in man_parts:
                canvas.move(part, 0, -10)
        
        # Check if the man is off the road
        check_off_road()

# Function to move the obstacles, lane markings, and trees
def move_objects():
    global score
    if not game_over_flag:
        for obstacle in obstacles:
            canvas.move(obstacle, 0, 5)
            if canvas.coords(obstacle)[1] > 600:
                x = random.randint(220, 580)
                y = random.randint(-400, -20)
                if canvas.type(obstacle) == "oval":
                    canvas.coords(obstacle, x, y, x+20, y+20)
                else:
                    canvas.coords(obstacle, x, y)
                score += 1
                canvas.itemconfigure(score_text, text=f"Score: {score}")
        
        for lane_marking in lane_markings:
            canvas.move(lane_marking, 0, 5)
            if canvas.coords(lane_marking)[1] > 600:
                canvas.move(lane_marking, 0, -600)
        
        for trunk, leaves in trees:
            canvas.move(trunk, 0, 5)
            canvas.move(leaves, 0, 5)
            if canvas.coords(trunk)[1] > 600:
                canvas.move(trunk, 0, -600)
                canvas.move(leaves, 0, -600)
        
        # Check for collision between man and obstacles
        check_collision()
        
        # Schedule the function to be called again after 50 ms
        root.after(50, move_objects)

# Function to check for collision between man and obstacles
def check_collision():
    for part in man_parts:
        man_coords = canvas.bbox(part)
        for obstacle in obstacles:
            obstacle_coords = canvas.bbox(obstacle)
            if (man_coords[2] >= obstacle_coords[0] and man_coords[0] <= obstacle_coords[2] and
                man_coords[3] >= obstacle_coords[1] and man_coords[1] <= obstacle_coords[3]):
                game_over()

# Function to check if the man is off the road
def check_off_road():
    man_coords = canvas.bbox(body)
    if man_coords[0] < 200 or man_coords[2] > 600:
        game_over()

# Function to end the game
def game_over():
    global game_over_flag, game_over_text
    if not game_over_flag:
        game_over_flag = True
        game_over_text = canvas.create_text(400, 300, text="Game Over", font=("Arial", 24), fill="red")
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

# Function to start/restart the game
def start_game():
    global score, game_over_flag, game_over_text
    score = 0
    game_over_flag = False
    canvas.itemconfigure(score_text, text=f"Score: {score}")
    for obstacle in obstacles:
        x = random.randint(220, 580)
        y = random.randint(-400, -20)
        if canvas.type(obstacle) == "oval":
            canvas.coords(obstacle, x, y, x+20, y+20)
        else:
            canvas.coords(obstacle, x, y)
    canvas.coords(head, 380, 470, 420, 510)
    canvas.coords(body, 370, 510, 430, 570)
    canvas.coords(left_arm, 350, 510, 370, 550)
    canvas.coords(right_arm, 430, 510, 450, 550)
    canvas.coords(left_leg, 370, 570, 390, 610)
    canvas.coords(right_leg, 410, 570, 430, 610)
    if game_over_text:
        canvas.delete(game_over_text)
        game_over_text = None
    move_objects()

# Create a start/restart button
start_button = tk.Button(root, text="Start/Restart", command=start_game)
start_button.pack()

# Bind the arrow keys to the move_man function
root.bind('<Left>', move_man)
root.bind('<Right>', move_man)
root.bind('<Down>', move_man)
root.bind('<Up>', move_man)

# Run the main loop
root.mainloop()