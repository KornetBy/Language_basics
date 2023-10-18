import turtle

# Set up screen
screen = turtle.Screen()
screen.title("Circle")
screen.setup(450, 450)
screen.bgcolor("cyan")

# Create a turtle
toby = turtle.Turtle()
toby.speed(0)
toby.width(5)
toby.hideturtle()
toby.color("red")

# Draw a circle starting at (x, y)
radius = 100
toby.circle(radius)

# Make it all work properly
turtle.done()