import os
from vectorslack import vector
from slackclient import SlackClient
import anki_vector

if __name__ == '__main__':
    sc = SlackClient(os.environ['SLACK_TOKEN'])

    with anki_vector.Robot(os.environ['VECTOR_SERIAL'], enable_camera_feed=True) as robot:
        vector.start('VectorBot', sc, robot)
