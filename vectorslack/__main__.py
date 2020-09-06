import os
from vectorslack import vector
import anki_vector
from slack import RTMClient, WebClient

webclient = WebClient(token=os.environ['SLACK_TOKEN'])
rtm_client = RTMClient(token=os.environ['SLACK_TOKEN'])

if __name__ == '__main__':
    with anki_vector.Robot(os.environ['VECTOR_SERIAL'], behavior_control_level=None) as robot:
        vector.start(rtm_client, webclient, robot)
