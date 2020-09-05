import os
from vectorslack import vector
import anki_vector
from slack import RTMClient, WebClient
import sys

webclient = WebClient(token=os.environ['SLACK_TOKEN'])
rtm_client = RTMClient(token=os.environ['SLACK_TOKEN'])


if __name__ == '__main__':
    print(sys.path)
    print(os.environ['PYTHONPATH'])
    with anki_vector.Robot(os.environ['VECTOR_SERIAL']) as robot:
        vector.start(rtm_client, webclient, robot)
