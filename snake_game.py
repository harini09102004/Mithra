import turtle
import time
import random

def snakegame():
    delay = 0.1

    score = 0  # Score should start from 0, not 0.1
    high_score = 0

    # Set up the screen
    wn = turtle.Screen()
    wn.title("Snake Game")
    wn.bgcolor("green")
    wn.setup(width=600, height=600)
    wn.tracer(0)  # Disable automatic updates

    # Snake head
    head = turtle.Turtle()
    head.speed(0)
    head.shape("square")
    head.penup()
    head.goto(0, 0)
    head.direction = "stop"

    # Snake food
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("red")
    food.penup()
    food.goto(0, 100)

    # Segments (initially empty)
    segments = []

    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write("Score: 0 High Score: 0", align="center", font=("Courier", 24, "normal"))

    # Functions for moving the snake
    def go_up():
        if head.direction != "down":  # Prevent the snake from moving in the opposite direction
            head.direction = "up"

    def go_down():
        if head.direction != "up":
            head.direction = "down"

    def go_left():
        if head.direction != "right":
            head.direction = "left"

    def go_right():
        if head.direction != "left":
            head.direction = "right"

    # Move the snake
    def move():
        if head.direction == "up":
            y = head.ycor()
            head.sety(y + 20)

        if head.direction == "down":
            y = head.ycor()
            head.sety(y - 20)

        if head.direction == "left":
            x = head.xcor()
            head.setx(x - 20)

        if head.direction == "right":
            x = head.xcor()
            head.setx(x + 20)

    # Keyboard bindings
    wn.listen()
    wn.onkeypress(go_up, "w")
    wn.onkeypress(go_down, "s")
    wn.onkeypress(go_left, "a")
    wn.onkeypress(go_right, "d")

    # Main game loop
    while True:
        wn.update()

        # Check for border collision
        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            # Hide segments and reset
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0  # Reset score
            pen.clear()  # Clear the score display
            pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Check for collision with the food
        if head.distance(food) < 20:
            # Move the food to a random spot
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            food.goto(x, y)

            # Add a new segment to the snake
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

            delay += 0.001

            score += 10

            if score > high_score:
                high_score = score

            pen.clear()  # Clear the previous score
            pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Move segments
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move()

        # Check for collision with the snake's body
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"

                # Hide the segments
                for segment in segments:
                    segment.goto(1000, 1000)

                segments.clear()

                score = 0
                # Reset the score
                delay = 0.1
                pen.clear()  # Clear the score display
                pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        time.sleep(delay)  # Adjust time delay



    # No need to call wn.mainloop() in a while loop, so it is removed from here






    # Keep the window open
    wn.mainloop()  # Keeps the window running and responsive
