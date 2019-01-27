import re
import time

from vectorslack.command_parser import CommandParser, SUPPORTED_COMMANDS

RTM_READ_DELAY = 1


def start(botname, slack_client, robot):
    command_parser = create_command_parser(robot, slack_client)
    if slack_client.rtm_connect():
        while slack_connected(slack_client) is True:
            parse_events(botname, slack_client, command_parser)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection Failed")


def create_command_parser(robot, slack_client):
    return CommandParser(robot, slack_client)


def slack_connected(slack_client):
    return slack_client.server.connected


def parse_events(botname, slack_client, command_parser):
    events = parse_bot_commands(slack_client.rtm_read(), botname)
    for event in events:
        handle_command(event[0], event[1], botname, slack_client, command_parser)


def parse_bot_commands(slack_events, botname):
    events = []
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"], botname)
            if user_id == botname:
                events.append((message, event["channel"]))

    return events


def parse_direct_mention(message_text, botname):
    regex = get_mention_regex(botname)
    matches = re.search(regex, message_text, re.RegexFlag.IGNORECASE)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def get_mention_regex(botname):
    return "^@(%s)(.*)" % botname


def handle_command(message, channel, botname, slack_client, command_parser):
    default_response = "I'm not sure what you mean."

    response = None
    lower_case_message = message.lower()
    try:
        command, attribute_name = next(
            (key, value) for key, value in SUPPORTED_COMMANDS if lower_case_message.startswith(key))

        message_contents = lower_case_message.replace(command, '', 1).strip()

        getattr(command_parser, attribute_name)(command=message_contents, channel=channel)
        response = "%s is a go go" % botname
    except StopIteration as e:
        print("Failed to parse command " + message)

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
