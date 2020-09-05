import unittest
from unittest.mock import Mock, patch, call

import anki_vector
from parameterized import parameterized
from slack import RTMClient, WebClient

from vectorslack import vector
from vectorslack.command_parser import CommandParser

events = [
    {
        "type": "message",
        "channel": "C2147483705",
        "user": "U2147483697",
        "text": "<@12345> say hi",
        "ts": "1355517523.000005"
    },
    {
        "type": "message",
        "subtype": "channel_join",
        "text": "<@U023BECGF|bobby> has joined the channel",
        "ts": "1403051575.000407",
        "user": "U023BECGF"
    },
    {
        "type": "message",
        "channel": "C2147483705",
        "user": "U2147483697",
        "text": "@Someone wasup",
        "ts": "1355517523.000005"
    },
    {
        "type": "message",
        "channel": "C2147483705",
        "user": "U2147483697",
        "text": "some message",
        "ts": "1355517523.000005"
    },
    {
        "type": "message",
        "channel": "A45234",
        "user": "U2147483697",
        "text": "<@12345> make heart eyes",
        "ts": "1355517523.000005"
    },
]


class TestVector(unittest.TestCase):

    @parameterized.expand([
        ["matches", "<@VectorBot> go go", "VectorBot", "go go"],
        ["does NOT matche", "<@vector> go go", None, None],
        ["does match case insensitive", "<@vectorbot> go go", "vectorbot", "go go"],
    ])
    def test_parses_direct_mention_when_botname(self, name, message, expected_user, expected_message):
        user, message = vector.parse_direct_mention(message, "VectorBot")
        self.assertEqual(user, expected_user)
        self.assertEqual(message, expected_message)


    @patch('vectorslack.vector.handle_command')
    @patch('vectorslack.vector.parse_direct_mention')
    def test_parse_command(self, mock_direct_mention, mock_handle_command):
        payload = {
            'text': '<@VectorBot> say hi',
            'channel': '1234',
            'ts': '999.999'
        }
        mock_web_client = Mock(spec=WebClient)
        mock_command_parser = Mock(spec=CommandParser)

        vector.bot_id = 'VectorBot'
        vector.bot_name = 'Vector'
        vector.web_client = mock_web_client
        vector.command_parser = mock_command_parser

        mock_direct_mention.return_value = ('VectorBot', 'say hi')
        vector.parse_bot_commands(data=payload)

        mock_direct_mention.assert_called_with('<@VectorBot> say hi', 'VectorBot')
        mock_handle_command.assert_called_with('say hi', '1234', '999.999', 'Vector', mock_web_client, mock_command_parser)

    @patch('vectorslack.vector.create_command_parser')
    def test_start(self, mock_create_command):
        mock_web_client = Mock(spec=WebClient)
        mock_rtm_client = Mock(spec=RTMClient)
        mock_web_client.auth_test.return_value = {"user_id": "12345", "user": "vectorbot"}

        mock_command_parser = Mock(spec=CommandParser)
        mock_create_command.return_value = mock_command_parser

        mock_vector = Mock(spec=anki_vector.Robot)

        vector.start(mock_rtm_client, mock_web_client, mock_vector)

        mock_create_command.assert_called_with(mock_vector, mock_web_client)
        mock_web_client.auth_test.assert_called()
        mock_rtm_client.start.assert_called()

    def test_handle_command_say(self):
        mock_command_parser = Mock(spec=CommandParser)
        mock_web_client = Mock(spec=WebClient)

        vector.handle_command("say hello there", "1234", "9999.000", "vectorbot", mock_web_client, mock_command_parser)

        mock_command_parser.say.assert_called_with(channel="1234", command="hello there")

        mock_web_client.chat_postMessage.assert_called_with(
            channel="1234",
            text="vectorbot is a go go",
            thread_ts="9999.000"
        )

    def test_handle_command_move(self):
        mock_command_parser = Mock(spec=CommandParser)
        mock_web_client = Mock(spec=WebClient)

        vector.handle_command("move forward", "1234", "9999.000", "vectorbot", mock_web_client, mock_command_parser)

        mock_command_parser.move.assert_called_with(channel="1234", command="forward")

    def test_handle_command_whats_going_on(self):
        mock_command_parser = Mock(spec=CommandParser)
        mock_web_client = Mock(spec=WebClient)

        vector.handle_command("whats going on", "1234", "9999.000", "vectorbot", mock_web_client, mock_command_parser)

        mock_command_parser.whats_going_on.assert_called_with(channel="1234", command="")

    def test_handle_command_whats_going_on_case_insensitive(self):
        mock_command_parser = Mock(spec=CommandParser)
        mock_web_client = Mock(spec=WebClient)

        vector.handle_command("Whats going on", "1234", "9999.000", "vectorbot", mock_web_client, mock_command_parser)

        mock_command_parser.whats_going_on.assert_called_with(channel="1234", command="")

    def test_handle_command_invalid_posts_to_slack(self):
        mock_command_parser = Mock(spec=CommandParser)
        mock_web_client = Mock(spec=WebClient)

        vector.handle_command("utter garbage", "1234", "9999.000", "vectorbot", mock_web_client, mock_command_parser)

        mock_web_client.chat_postMessage.assert_called_with(
            channel="1234",
            text="I'm not sure what you mean.",
            thread_ts="9999.000"
        )


if __name__ == '__main__':
    unittest.main()
