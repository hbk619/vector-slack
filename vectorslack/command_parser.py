from PIL import Image
from anki_vector import screen

DEFAULT_IMAGE_TIME = 4.0  # seconds


class CommandParser:
    def __init__(self, robot):
        self.robot = robot

    def say(self, command):
        self.robot.say_text(command)

    def move(self, command):
        self.robot.motors.set_wheel_motors()

    def show(self, command):
        split_command = command.split(' ')
        image_file = Image.open('images/%s.png' % split_command[0])
        duration = None

        try:
            duration = float(split_command[2])
        except (IndexError, TypeError):
            print("No duration specified for image. Message: '%s', using default" % command)

        screen_data = screen.convert_image_to_screen_data(image_file)
        self.robot.screen.set_screen_with_image_data(screen_data, duration or DEFAULT_IMAGE_TIME)
