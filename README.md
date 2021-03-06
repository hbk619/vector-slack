# WORK IN PROGRESS

Integrate Slack with Anki's Vector

## Possible commands

    say <message>
    show <image name>
    show <image name> for <number> seconds
    whats going on
    play <spritesheet name>
    fireworks
    giggle

## Requirements

Python 3.6 (for Vector)

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.6

### Slack token

You will need a [classic  slack app](https://api.slack.com/rtm#classic) with a single scope of 'bot'. Ignore the 
"there are new permissions!" warnings. Add a bot user via App Home on the left, then install to your workspace and take
the token beginning with xoxb

## Developing
    
    python3.6 -m venv .
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -e .
    
### Tests

    python -m unittest discover -s vectorslack/tests
    
## Docker

    docker build .
    docker run -v vector_config:/root/.anki_vector -ti <image id> /bin/bash
    python3.6 -m anki_vector.configure
    <enter all your details>
    exit
    docker run -v vector_config:/root/.anki_vector -e SLACK_TOKEN -e VECTOR_SERIAL <image id>
    
## Sprite sheets for animations

Create a PNG sprite sheet, each sprite is 184 in width, 96 in height. Two rows of five and place in

    vectorslack/images

## Images

Any images you want to use with the "show" command should go in vectorslack/images and be 184 pixels wide and 94 pixels
high