import unittest
from unittest.mock import Mock, patch, call
from parameterized import parameterized

import anki_vector
from PIL import Image
from anki_vector import screen, camera, behavior, animation
from slack import WebClient

from vectorslack.command_parser import CommandParser


class TestSay(unittest.TestCase):

    def setUp(self):
        self.mock_robot = Mock(spec=anki_vector.Robot)
        self.mock_robot.screen = Mock(spec=screen.ScreenComponent)
        self.mock_robot.camera = Mock(spec=camera.CameraComponent)
        self.mock_robot.behavior = Mock(spec=behavior.BehaviorComponent)
        self.mock_robot.anim = Mock(spec=animation.AnimationComponent)
        self.mock_slack_client = Mock(spec=WebClient)
        self.parser = CommandParser(self.mock_robot, self.mock_slack_client)

    def test_say(self):
        self.parser.say(command="hey mario!")

        self.mock_robot.behavior.say_text.assert_called_with("hey mario!")

    @patch('vectorslack.command_parser.screen.convert_image_to_screen_data')
    @patch('PIL.Image.open')
    @patch('os.path.realpath', return_value="test/dir/file.png")
    @patch('os.path.dirname', return_value="test/dir/file.png")
    def test_play(self, mocked_dirname, mock_realpath, mock_open, mock_convert_image):
        mock_image = Mock(spec=Image.Image)
        mock_images = []
        expected_calls = []
        for _ in range(30):
            image = Mock(spec=Image.Image)
            mock_images.append(image)
            expected_calls.append(call(image))

        mock_image.crop.side_effect = mock_images
        mock_open.return_value = mock_image
        image_bytes = bytes()
        mock_convert_image.return_value = image_bytes

        self.parser.play(command="parrot")

        self.assertEqual(mock_image.crop.call_count, 30)

        mock_convert_image.assert_has_calls(expected_calls)

        self.mock_robot.screen.set_screen_with_image_data.assert_called_with(image_bytes, 4.0)
        self.assertEqual(self.mock_robot.screen.set_screen_with_image_data.call_count, 30)

    @patch('vectorslack.command_parser.screen.convert_image_to_screen_data')
    @patch('PIL.Image.open')
    @patch('os.path.realpath', return_value="test/dir/file.png")
    def test_show(self, mock_realpath, mock_open, mock_convert_image):
        mock_image = Mock(spec=Image.Image)
        mock_open.return_value = mock_image
        image_bytes = bytes()
        mock_convert_image.return_value = image_bytes

        self.parser.show(command="heart")

        mock_open.assert_called_with("test/dir/images/heart.png")
        mock_convert_image.assert_called_with(mock_image)

        self.mock_robot.screen.set_screen_with_image_data.assert_called_with(image_bytes, 4.0)

    @patch('vectorslack.command_parser.screen.convert_image_to_screen_data')
    @patch('PIL.Image.open')
    @patch('os.path.realpath', return_value="test/dir/file.png")
    def test_show_with_duration(self, mock_realpath, mock_open, mock_convert_image):
        mock_image = Mock(spec=Image.Image)
        mock_open.return_value = mock_image
        image_bytes = bytes()
        mock_convert_image.return_value = image_bytes

        self.parser.show(command="heart for 7 seconds")

        mock_open.assert_called_with("test/dir/images/heart.png")
        mock_convert_image.assert_called_with(mock_image)

        self.mock_robot.screen.set_screen_with_image_data.assert_called_with(image_bytes, 7.0)

    @patch('io.BytesIO')
    @patch('time.sleep')
    def test_whats_going_on(self, mock_time, mock_bytes_io):
        mock_bytes_io().getvalue.side_effect = ["This is a fun picture of the world 1",
                                                "This is a fun picture of the world 2",
                                                "This is a fun picture of the world 3",
                                                "This is a fun picture of the world 4"]
        mock_image = Mock(spec=Image.Image)
        self.mock_robot.camera.latest_image = mock_image

        self.parser.whats_going_on(channel="1234")

        self.mock_robot.behavior.drive_off_charger.assert_called_once()

        mock_image.save.assert_called_with(mock_bytes_io(), "PNG")

        calls = [call("files.upload",
                      channels="1234",
                      file="This is a fun picture of the world 1",
                      filename="this-is-whats-happening.png",
                      as_user=True),
                 call("files.upload",
                      channels="1234",
                      file="This is a fun picture of the world 2",
                      filename="this-is-whats-happening.png",
                      as_user=True),
                 call("files.upload",
                      channels="1234",
                      file="This is a fun picture of the world 3",
                      filename="this-is-whats-happening.png",
                      as_user=True),
                 call("files.upload",
                      channels="1234",
                      file="This is a fun picture of the world 4",
                      filename="this-is-whats-happening.png",
                      as_user=True)]

        self.mock_slack_client.api_call.assert_has_calls(calls)
        self.assertEqual(self.mock_slack_client.api_call.call_count, 4)

        mock_time.assert_has_calls([call(0.5), call(0.5), call(0.5), call(0.5)])

    def test_giggle(self):

        self.parser.giggle()

        self.mock_robot.anim.play_animation.assert_called_with('anim_eyecontact_giggle_01_head_angle_20')

    def test_fireworks(self):

        self.parser.fireworks()

        self.mock_robot.anim.play_animation.assert_called_with('anim_holiday_hny_fireworks_01')

    @parameterized.expand([
        ["zeros", 0, 0, 96, 0, 184, 0],
        ["ones", 1, 1, 192, 184, 368, 96],
        ["twos", 2, 2, 288, 368, 552, 192],
    ])
    def test_get_crop_coordinates(self, name, x, y, expected_bottom, expected_left, expected_right, expected_top):

        bottom, left, right, top = self.parser.get_crop_coordinates(x, y)

        self.assertEqual(bottom, expected_bottom)
        self.assertEqual(top, expected_top)
        self.assertEqual(left, expected_left)
        self.assertEqual(right, expected_right)