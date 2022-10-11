import re
import time

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
        handle_command(message, data["channel"], data['ts'], web_client, command_parser)


def parse_direct_mention(message_text, bot_name):
    regex = get_mention_regex(bot_name)
    matches = re.search(regex, message_text, re.RegexFlag.IGNORECASE)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def get_mention_regex(bot_name):
    return "^<@(%s)>(.*)" % bot_name


def gain_control(robot):
    robot.conn.request_control().result()
    time.sleep(0.5)


def release_control(robot):
    robot.conn.release_control(timeout=5).result()


def handle_command(message, channel, ts, slack_client, command_parser):
    default_response = "I'm not sure what you mean."

    response = None
    lower_case_message = message.lower()
    try:
        gain_control(command_parser.robot)
        command, attribute_name = next(
            (key, value) for key, value in SUPPORTED_COMMANDS if lower_case_message.startswith(key))

        message_contents = lower_case_message.replace(command, '', 1).strip()

        getattr(command_parser, attribute_name)(command=message_contents, channel=channel)
        response = "I did as you asked"
    except StopIteration:
        print("Failed to parse command: " + message)
    except Exception as e:
        print("Failed to trigger vector for command: " + message)
        print(e)

    try:
        release_control(command_parser.robot)
    except Exception as e:
        print("Failed to release vector for command: " + message)
        print(e)

    slack_client.chat_postMessage(
        channel=channel,
        text=response or default_response,
        thread_ts=ts
    )
