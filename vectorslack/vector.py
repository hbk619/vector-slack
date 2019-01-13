import time
import re
from vectorslack.command_parser import CommandParser

RTM_READ_DELAY = 1


def start(botname, slack_client, robot):
    command_parser = create_command_parser(robot)
    if slack_client.rtm_connect():
        while slack_connected(slack_client) is True:
            parse_events(botname, slack_client, command_parser)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection Failed")


def create_command_parser(robot):
    return CommandParser(robot)


def slack_connected(slack_client):
    return slack_client.server.connected


def parse_events(botname, slack_client, command_parser):
    events = parse_bot_commands(slack_client.rtm_read(), botname)
    for event in events:
        handle_command(event[1], event[0], botname, slack_client, command_parser)


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

    command = message.split(' ')[0]

    try:
        getattr(command_parser, command)(message.replace(command, '', 1).strip())
        response = "%s is a go go" % botname
    except AttributeError as e:
        print("Failed to parse command " + message)

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
