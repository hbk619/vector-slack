# WORK IN PROGRESS

Integrate Slack with Anki's Vector

## Possible commands

    say <message>
    show <image name>
    show <image name> for <number> seconds
    whats going on
    fireworks
    giggle

## Requirements

Python 3.6 (for Vector)

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.6

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
