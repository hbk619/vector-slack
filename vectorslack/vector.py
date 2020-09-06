import re

from slack import RTMClient
from vectorslack.command_parser import CommandParser, SUPPORTED_COMMANDS

RTM_READ_DELAY = 1

command_parser = None
bot_id = ''
bot_name = ''
web_client = None


def start(rtm_client, webclient, robot):
    global command_parser
    command_parser = create_command_parser(robot, webclient)
    global web_client
    web_client = webclient
    bot_details = web_client.auth_test()
    global bot_id
    bot_id = bot_details["user_id"]
    global bot_name
    bot_name = bot_details["user"]
    rtm_client.start()


def create_command_parser(robot, slack_client):
    return CommandParser(robot, slack_client)


@RTMClient.run_on(event='message')
def parse_bot_commands(**payload):
    data = payload['data']
    user_id, message = parse_direct_mention(data["text"], bot_id)
    if user_id == bot_id:
        handle_command(message, data["channel"], data['ts'], bot_name, web_client, command_parser)


def parse_direct_mention(message_text, bot_name):
    regex = get_mention_regex(bot_name)
    matches = re.search(regex, message_text, re.RegexFlag.IGNORECASE)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def get_mention_regex(bot_name):
    return "^<@(%s)>(.*)" % bot_name


def handle_command(message, channel, ts, bot_name, slack_client, command_parser):
    default_response = "I'm not sure what you mean."

    response = None
    lower_case_message = message.lower()
    try:
        command_parser.robot.conn.request_control().result()
        command, attribute_name = next(
            (key, value) for key, value in SUPPORTED_COMMANDS if lower_case_message.startswith(key))

        message_contents = lower_case_message.replace(command, '', 1).strip()

        getattr(command_parser, attribute_name)(command=message_contents, channel=channel)
        response = "%s is a go go" % bot_name
        command_parser.robot.conn.release_control().result()
    except StopIteration as e:
        print("Failed to parse command " + message)
        command_parser.robot.conn.release_control().result()

    except Exception as e:
        print("Failed to trigger vector " + message)
        print(e)
        command_parser.robot.conn.release_control().result()

    slack_client.chat_postMessage(
        channel=channel,
        text=response or default_response,
        thread_ts=ts
    )
