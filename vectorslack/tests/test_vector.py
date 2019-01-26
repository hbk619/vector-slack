import unittest
from vectorslack import vector
from vectorslack.command_parser import CommandParser
from parameterized import parameterized
from unittest.mock import Mock, patch
import anki_vector
from slackclient import SlackClient

events = [
    {
        "type": "message",
        "channel": "C2147483705",
        "user": "U2147483697",
        "text": "@VectorBot say hi",
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
        "text": "@VectorBot make heart eyes",
        "ts": "1355517523.000005"
    },
]


class TestVector(unittest.TestCase):

    @parameterized.expand([
        ["matches", "@VectorBot go go", "VectorBot", "go go"],
        ["does NOT matche", "@vector go go", None, None],
        ["does match case insensitive", "@vectorbot go go", "vectorbot", "go go"],
    ])
    def test_parses_direct_mention_when_botname(self, name, message, expected_user, expected_message):
        user, message = vector.parse_direct_mention(message, "VectorBot")
        self.assertEqual(user, expected_user)
        self.assertEqual(message, expected_message)

    def test_parse_command(self):
        expected_events = [
            (
                "say hi",
                "C2147483705"
            ),
            (
                "make heart eyes",
                "A45234"
            )
        ]

        actual_events = vector.parse_bot_commands(events, "VectorBot")

        self.assertListEqual(actual_events, expected_events)

    @patch('time.sleep')
    @patch('vectorslack.vector.slack_connected')
    @patch('vectorslack.vector.create_command_parser')
    @patch('vectorslack.vector.handle_command')
    def test_start(self, mock_handle_command, mock_create_command, mock_slack_connected, mock_time):
        mock_slack = Mock(spec=SlackClient)
        mock_slack_connected.side_effect = [True, False]
        mock_slack.rtm_read.return_value = events

        mock_command_parser = Mock(spec=CommandParser)
        mock_create_command.return_value = mock_command_parser

        mock_vector = Mock(spec=anki_vector.Robot)

        vector.start("VectorBot", mock_slack, mock_vector)

        self.assertEqual(mock_handle_command.call_count, 2)
        mock_create_command.assert_called_with(mock_vector, mock_slack)

    def test_handle_command_say(self):
        mock_command_parser = Mock(spec=CommandParser)
        mock_slack = Mock(spec=SlackClient)

        vector.handle_command("say hello there", "1234", "vectorbot", mock_slack, mock_command_parser)

        mock_command_parser.say.assert_called_with(channel="1234", command="hello there")

        mock_slack.api_call.assert_called_with(
            "chat.postMessage",
            channel="1234",
            text="vectorbot is a go go"
        )

    def test_handle_command_move(self):
        mock_command_parser = Mock(spec=CommandParser)
        mock_slack = Mock(spec=SlackClient)

        vector.handle_command("move forward", "1234", "vectorbot", mock_slack, mock_command_parser)

        mock_command_parser.move.assert_called_with(channel="1234", command="forward")

    def test_handle_command_whats_going_on(self):
        mock_command_parser = Mock(spec=CommandParser)
        mock_slack = Mock(spec=SlackClient)

        vector.handle_command("whatsgoingon", "1234", "vectorbot", mock_slack, mock_command_parser)

        mock_command_parser.whatsgoingon.assert_called_with(channel="1234", command="")

    def test_handle_command_invalid_posts_to_slack(self):
        mock_command_parser = Mock(spec=CommandParser)
        mock_slack = Mock(spec=SlackClient)

        vector.handle_command("utter garbage", "1234", "vectorbot", mock_slack, mock_command_parser)

        mock_slack.api_call.assert_called_with(
            "chat.postMessage",
            channel="1234",
            text="I'm not sure what you mean."
        )


if __name__ == '__main__':
    unittest.main()
