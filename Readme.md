# Oracle

## Mainframe Usage

You need to install **Python version 3.9**

Create virtual environment with:

```sh
python3 -m venv oracle-env
```

Activate virtual environment with:

```sh
. ./oracle-env/bin/activate
```
Install required dependencies with:

```sh
pip install -r requirements.txt
```

Run:

```sh
python3 mainframe.py
```

## Features

#### Radio

- joke(), e.g.: *'tell a joke'*
- datetime_now(), e.g.: *'what|tell time'*
- aphorism(), e.g.: *'tell aphorism|quote'*
- weather(), e.g.: *'tell weather'*
- poem(), e.g.: *'tell a poem'*
- read_dial(), e.g.: *'dialectica'*

#### Searcher

- topic_news('SCIENCE'), e.g.: *'tell news about science'*
- local_news(), e.g.: *'tell news'*
- wiki('Ukraine'), e.g.: *'wiki|find about'*

#### Writer

- mustdo(), e.g.: *'fix that I must go walking'*

#### Conductor

- launch('sublime'), e.g.: *'open|launch|start application'*
- lock(), e.g.: *'lock data'*
- unlock(), e.g.: *'unlock data'*

#### Utils

- sys.exit(), e.g.: *'stop|finish|shutdown'*

### Future imporvements from dev point of view

- Neuro transformator from text 2 command by dict.
- Screen recording and manipulation with [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) (Screener feature)
- Read movements and signals from built-in camera
- Register life events (Logger feature)
- Features builder GUI
- Microservices arch with kafka segmentation
- Localize configs and dockerize 4 user per user
- OS-like notifications with log

### Wouldlikes from philosophical point of view

- Interrupt any current command
- Astrological feature (ex. weather)
- Collect voice emotion !!!!!!!!!!
- Private communication system
- Save Milestones/Tasks for day/week/month (calendar int)


