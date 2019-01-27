import os
from vectorslack import vector
from slackclient import SlackClient
import anki_vector
import argparse

parser = argparse.ArgumentParser(description='Connect Slack and Vector')
parser.add_argument('--botname', type=str, dest='botname', default='VectorBot',
                    help='Name of your bot')

args = parser.parse_args()

if __name__ == '__main__':
    sc = SlackClient(os.environ['SLACK_TOKEN'])

    with anki_vector.Robot(os.environ['VECTOR_SERIAL'], enable_camera_feed=True) as robot:
        vector.start(args.botname, sc, robot)
