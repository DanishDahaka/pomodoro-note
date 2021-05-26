# Set up custom Pomodoro notes

This repository contains the Pomodoro-note-creator "pomodoro_to_bear.py".

## pomodoro_to_bear.py

### Requirements:

- [Bear](www.bear.app) for MacOS or iPhone/iPad
- [Pandas](https://pandas.pydata.org) 

### Description

Creates a variable length string in X-URL-Callback formatting which then creates a Bear note for Pomodoro method. Depending on when the script is executed and the user input for an ending time and duration, an amount of pomodoro slices is generated. Each slice has space for you to take notes.

Currently, flexible cycle lengths in the range of [5,300] minutes are supported.


### There are six steps in the original Pomodoro-Technique:

1. Decide on the task to be done.
2. Set the pomodoro timer (traditionally to 25 minutes).
3. Work on the task.
4. End work when the timer rings and put a checkmark on a piece of paper.
5. If you have fewer than four checkmarks, take a short break (3–5 minutes) and then
    return to step 2; otherwise continue to step 6.
6. After four pomodoros, take a longer break (15–30 minutes), reset your checkmark
    count to zero, then go to step 1.

Source: [Pomodoro-Technique Description at Wikipedia](https://en.wikipedia.org/wiki/Pomodoro_Technique#Description)
