import unittest
from vectorslack.command_parser import CommandParser
from unittest.mock import Mock, patch
import anki_vector
from anki_vector import screen
from PIL import Image


class TestSay(unittest.TestCase):

    def setUp(self):
        self.mock_robot = Mock(spec=anki_vector.Robot)
        self.mock_robot.screen = Mock(spec=screen.ScreenComponent)
        self.parser = CommandParser(self.mock_robot)

    def test_say(self):
        self.parser.say("hey mario!")

        self.mock_robot.say_text.assert_called_with("hey mario!")

    @patch('vectorslack.command_parser.screen.convert_image_to_screen_data')
    @patch('PIL.Image.open')
    def test_show(self, mock_open, mock_convert_image):
        mock_image = Mock(spec=Image.Image)
        mock_open.return_value = mock_image
        image_bytes = bytes()
        mock_convert_image.return_value = image_bytes

        self.parser.show("heart")

        mock_open.assert_called_with("images/heart.png")
        mock_convert_image.assert_called_with(mock_image)

        self.mock_robot.screen.set_screen_with_image_data.assert_called_with(image_bytes, 4.0)

    @patch('vectorslack.command_parser.screen.convert_image_to_screen_data')
    @patch('PIL.Image.open')
    def test_show_with_duration(self, mock_open, mock_convert_image):
        mock_image = Mock(spec=Image.Image)
        mock_open.return_value = mock_image
        image_bytes = bytes()
        mock_convert_image.return_value = image_bytes

        self.parser.show("heart for 7 seconds")

        mock_open.assert_called_with("images/heart.png")
        mock_convert_image.assert_called_with(mock_image)

        self.mock_robot.screen.set_screen_with_image_data.assert_called_with(image_bytes, 7.0)
