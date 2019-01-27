# WORK IN PROGRESS

Integrate Slack with Anki's Vector

## Possible commands

    say <message>
    show <image name>
    show <image name> for <number> seconds

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
