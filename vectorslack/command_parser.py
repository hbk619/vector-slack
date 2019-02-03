import io
import os

import time
from PIL import Image
from anki_vector import screen
from anki_vector.util import degrees

DEFAULT_IMAGE_TIME = 4.0  # seconds


class CommandParser:
    def __init__(self, robot, slack_client):
        self.robot = robot
        self.slack_client = slack_client

    def say(self, **kwargs):
        self.robot.say_text(kwargs['command'])

    def move(self):
        self.robot.motors.set_wheel_motors()

    def show(self, **kwargs):
        command = kwargs['command']
        split_command = command.split(' ')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image = Image.open('%s/images/%s.png' % (dir_path, split_command[0]))
        duration = None

        try:
            duration = float(split_command[2])
        except (IndexError, TypeError):
            print("No duration specified for image. Message: '%s', using default" % command)

        screen_data = screen.convert_image_to_screen_data(image)
        self.robot.screen.set_screen_with_image_data(screen_data, duration or DEFAULT_IMAGE_TIME)

    def play(self, **kwargs):
        command = kwargs['command']
        split_command = command.split(' ')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        sheet = Image.open('%s/images/%s.png' % (dir_path, split_command[0]))
        duration = None

        try:
            duration = float(split_command[2])
        except (IndexError, TypeError):
            print("No duration specified for image. Message: '%s', using default" % command)

        for _ in range(3):
            for y in range(2):
                for x in range(5):
                    left = x * 184
                    right = (x+1) * 184
                    top = y * 96
                    bottom = (y+1) * 96
                    image = sheet.crop((left, top, right, bottom))
                    screen_data = screen.convert_image_to_screen_data(image)
                    self.robot.screen.set_screen_with_image_data(screen_data, duration or DEFAULT_IMAGE_TIME)

    def whats_going_on(self, **kwargs):
        self.robot.behavior.drive_off_charger()

        for _ in range(4):
            time.sleep(0.5)

            content = io.BytesIO()
            image = self.robot.camera.latest_image
            image.save(content, "PNG")

            self.slack_client.api_call("files.upload",
                                       channels=kwargs['channel'],
                                       file=content.getvalue(),
                                       filename="this-is-whats-happening.png",
                                       as_user=True)

            self.robot.behavior.turn_in_place(degrees(90))


SUPPORTED_COMMANDS = {item.replace('_', ' '): item for item in dir(CommandParser) if not item.startswith('__')}.items()
