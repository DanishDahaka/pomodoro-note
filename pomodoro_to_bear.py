import webbrowser
import pandas as pd

### ASCII encodings for X-URL-Callback-String ###
space = "%20"
left_bracket_round = "%28"
right_bracket_round = "%29"
left_bracket_square = "%5B"
right_bracket_square = "%5D"
comma = "%2C"
colon = "%3A"
new_line = "%0A"
hashtag = "%23"
equal_sign = "%3D"
question_mark = "%3F"
slash = "%2F"
separator = "%20-%20"
horizontal_line = "---"
and_sign = "%26"
### ASCII encodings end ###

# different variations for opening note after completion or not
keep_note_closed = "&open_note=no&text="
open_note = "&open_note=yes&text="

# default title
begin = 'bear://x-callback-url/create?title=Pomodoro%20'


### break strings ###
pushup_break = 'Do'+space+'10'+space+'push-ups'
pull_up_break = pushup_break.replace('push','pull')
front_lever_break = 'Do'+space+'1min'+space+'front'+space+'lever'

# this longer break happens after a set of four pomodoros
longer_break = 'Take'+space+'a'+space+'rest'+space+'for'+space+'25mins'+\
    colon+space+'Get'+space+'some'+space+'fresh'+space+'air'

# collect all breaks
breaks = [pushup_break,pull_up_break,front_lever_break]


def create_pomodoro(end_time, cycle):

    """takes an end date and creates cycles from right now (normalized to the min) until the end date.

    Args:
        end_date    (string): time in format "hh:mm", e.g. "20:30"
        cycle       (string): pomodoro duration, e.g. "60min"

    Returns:
        string

    # Add a section detailing what errors might be raised
    Raises:
        ValueError: If `cycle` is not one of the defined strings.
    """

    # rounding to the nearest 5min, beware, this can also lead to earlier time
    begin_time = pd.Timestamp.now().round('5min')

    # getting date info from timestamp
    year = begin_time.year
    month = begin_time.month
    day = begin_time.day

    # create dd.mm.yyyy string from current date
    titledate = str(day)+'.'+str(month)+'.'+str(year)
    print('titledate:',titledate)

    # creating new timestamp based on end_time; format of end_time == '20:30'
    end_time = pd.Timestamp(
                            year = year, month= month, day = day, 
                            hour = int(end_time[:2]), minute = int(end_time[3:])
                            )

    print('this is end time: ', end_time)
    print('this is the beginning:',begin_time)

    timediff_mins = pd.Timedelta(end_time - begin_time).seconds / 60

    print('timediff mins: ',timediff_mins)

    title_continue = begin + titledate +'%20'

    standard_content = '%20cycle&open_note=yes&text=%23pom'+\
            'odoro%2F25mins%0A---%0AFlow%3A%5B%5BPomodoro%20-%20Technique%5D%5D'+\
                '%0A---%0A%23%23%20Summary'+'%0A'

    if cycle == '90min':

        content = title_continue + '90mins' + standard_content

        # 1 pomodoro == 90min, how many mins break?
        #amount_cycles = 
        pass

    elif cycle == '60min':

        content = title_continue + '60mins' + standard_content

        # 1 pomodoro == 60min, how many mins break?
        #amount_cycles =
        pass

    elif cycle == '25min':

        # 1 pomodoro == 25min, 5 min break, thus 30min cycle
        content = title_continue + '25mins' + standard_content

        amount_cycles = round(timediff_mins/30)
        print('amount_cycles: ',amount_cycles)

        cycle_end_time = begin_time + pd.Timedelta(minutes=25)

        j = 0

        for i in range(1,amount_cycles+1):

                if i%4 == 0:
                    
                    break_elem = longer_break

                    cycle_content = '%0A---%0A%23%23%20Cycle%20'+str(i)+'%2C%20'+begin_time.strftime('%H:%M')+'-'+\
                                cycle_end_time.strftime('%H:%M')+\
                                '%0A%0A%0A---%0A%3A%3ABreak%20'+str(i)+'%2C%20'+\
                                cycle_end_time.strftime('%H:%M')

                    # changing times with +60min because of longer break
                    begin_time = begin_time + pd.Timedelta(minutes=60)

                    # also, make this statement bold at the same time
                    cycle_content = cycle_content +'-'+begin_time.strftime('%H:%M')+'%20-%3E%20'+\
                        '*'+break_elem+'*'+'%3A%3A'

                    cycle_end_time = cycle_end_time + pd.Timedelta(minutes=60)

                    content = content + cycle_content


                else:
                    
                    break_elem = breaks[j]
                    # concatenate string with hh:mm from timestamp, +25min and +5 for break
                    cycle_content = '%0A---%0A%23%23%20Cycle%20'+str(i)+'%2C%20'+begin_time.strftime('%H:%M')+'-'+\
                                cycle_end_time.strftime('%H:%M')+\
                                '%0A%0A%0A---%0A%3A%3ABreak%20'+str(i)+'%2C%20'+\
                                cycle_end_time.strftime('%H:%M')

                    # setting times forward for next cycle
                    begin_time = begin_time + pd.Timedelta(minutes=30)

                    cycle_content = cycle_content +'-'+begin_time.strftime('%H:%M')+'%20-%3E%20'+\
                        break_elem+'%3A%3A'

                    cycle_end_time = cycle_end_time + pd.Timedelta(minutes=30)

                    content = content + cycle_content
                    # setting up j for next step
                    if j < 2:
                        j += 1
                    else:
                        j = 0


    else:
        raise ValueError('Insert fitting value for time')


    return content

    """There are six steps in the original technique:

    Decide on the task to be done.
    Set the pomodoro timer (traditionally to 25 minutes).[1]
    Work on the task.
    End work when the timer rings and put a checkmark on a piece of paper.[5]
    If you have fewer than four checkmarks, take a short break (3–5 minutes) and then return to step 2; otherwise continue to step 6.
    After four pomodoros, take a longer break (15–30 minutes), reset your checkmark count to zero, then go to step 1."""



#### creating the final note ####


print('Welcome to Pomodoro.py as a flexible note time. '+\
    '\nThe options for cycles are "25min" for now') #"60min" and "90min" for now.')

# opens browser and enters x-url-callback string
webbrowser.open(create_pomodoro('20:30','25min'))

#create_pomodoro('20:30','25min')