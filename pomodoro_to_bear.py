import webbrowser
import pandas as pd

"""  possible extensions:
-   put ASCII and Bear stuff in separate file and import 
-   Make cycle duration (cd) variable and calculate break lengths based on cd (e.g. cd = 50, bl = 0.1*cd)
"""

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

def make_cycles(title_continue, standard_content, cycle, begin_time, end_time, short_time, long_time):

    """concatenates for each cycle a new string to the main X-URL-Callback string

    Args:
        title_continue      (String): beginning of the X-URL-Callback String + title
        standard_content    (String): custom header for Bear note
        cycle               (String): cycle duration as string, e.g. '25min'
        begin_time          (Timestamp): current time rounded to nearest 5mins
        end_time            (Timestamp): converted String from user input into timestamp
        short_time          (Integer): shortest duration for a cycle (three of these sequentially)
        long_time           (Integer): longest duration for a cycle (once per three short ones)

    Returns:
        content             (String): the content for the entire pomodoro note

    """

    # preparing the string with length of cycle as text in between
    content = title_continue + cycle + standard_content 
    
    # add duration of cycle time as timedelta from the first two chars of cycle, e.g. 25 from '25min'
    cycle_end_time = begin_time + pd.Timedelta(minutes=int(cycle[:2]))
    
    # initialize variables before while loop
    i,j = 1,0

    # end before or on time supplied by user
    while cycle_end_time < end_time:
        
        # every fourth cycle
        if i%4 == 0:
            
            break_elem = longer_break

            # 1 pomodoro == 25min, 5 min break, thus 30min normal cycle time
            cycle_content, begin_time, cycle_end_time = add_cycle_content(break_elem, begin_time, cycle_end_time, i, long_time)

            content = content + cycle_content

        # every other cycle
        else:
            
            break_elem = breaks[j]
            
            cycle_content, begin_time, cycle_end_time = add_cycle_content(break_elem, begin_time, cycle_end_time, i, short_time)

            content = content + cycle_content

            # circling through [0,1,2] for j to get text at breaks[j]
            if j < 2:

                j += 1

            else:

                j = 0
        
        i += 1
    
    print('amount_cycles: ', i)

    return content
    

def add_cycle_content(break_element, cycle_begin_time, cycle_end_time, cycle_number, minute_difference):

    """concatenates for each cycle a new string to the main X-URL-Callback string

    Args:
        break_element       (String):  message for break lines 
        cycle_begin_time    (Timestamp): when the cycle starts
        cycle_end_time      (Timestamp): end of current cycle
        cycle_number        (integer): current cycle number

    Returns:
        cycle_content (string): the X-URL-Callback string for one cycle

    """

    cycle_content = '%0A---%0A%23%23%20Cycle%20'+str(cycle_number)+'%2C%20'+\
                            cycle_begin_time.strftime('%H:%M')+'-'+\
                            cycle_end_time.strftime('%H:%M')+\
                            '%0A%0A%0A---%0A%3A%3ABreak%20'+str(cycle_number)+'%2C%20'+\
                            cycle_end_time.strftime('%H:%M')

    # change times with minute difference depending on which interval is wished
    cycle_begin_time = cycle_begin_time + pd.Timedelta(minutes=minute_difference)
    cycle_end_time = cycle_end_time + pd.Timedelta(minutes=minute_difference)

    # also, make this statement bold at the same time
    cycle_content = cycle_content +'-'+cycle_begin_time.strftime('%H:%M')+\
        '%20-%3E%20'+'*'+break_element+'*'+'%3A%3A'


    return cycle_content, cycle_begin_time, cycle_end_time


def create_pomodoro(end_time, cycle):

    """takes an end date and creates cycles from right now (normalized to
    a 5-minute time) until the end date.

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

    # prepare strings for adding tag "diary/yyyy/mm/dd"
    if day < 10:
        day_prefix_zero = '0'+str(day) 
    else:
        day_prefix_zero = str(day)

    if month < 10:
        month_prefix_zero = '0'+str(month) 
    else:
        month_prefix_zero = str(month)

    # create dd.mm.yyyy string from current date
    titledate = str(day)+'.'+str(month)+'.'+str(year)
    print('titledate:',titledate)

    # creating new timestamp based on end_time; format of end_time == '20:30'
    end_time = pd.Timestamp(year = year, month= month, day = day, 
                            hour = int(end_time[:2]), 
                            minute = int(end_time[3:])
                            )

    print('this is end time: ', end_time)
    print('this is the beginning:',begin_time)

    timediff_mins = pd.Timedelta(end_time - begin_time).seconds / 60

    print('timediff mins: ',timediff_mins)

    title_continue = begin + titledate + space

    # prepare the beginning of the X-URL-Callback String
    standard_content = '%20cycle&open_note=yes&text=%23pom'+\
        'odoro%2F' + cycle + space + hashtag + 'diary' + slash + str(year) + slash +\
            month_prefix_zero + slash + day_prefix_zero +\
            '%0A---%0AFlow%3A%5B%5BPomodoro%20-%20Technique%5D%5D'+\
            '%0A---%0A%23%23%20Summary%0A'

    # adapted from https://www.huffpost.com/entry/work-life-balance-the-90_b_578671
    if cycle == '90min':
        
        # no concrete duration for break given, so example uses 90+30 and 90+60
        content = make_cycles(title_continue, standard_content, cycle, begin_time, end_time, 120, 150)
        

    elif cycle == '60min':

        # 52+17 and 52 + 34 mins, from: https://medium.com/@timmetz/pomodoro-technique-and-other-work-rhythms-which-one-suits-you-34c2d05fe46e
        content = make_cycles(title_continue, standard_content, cycle, begin_time, end_time, 69, 86)

    elif cycle == '25min':

        # the classic approach with 25+5 and 25+25 mins
        content = make_cycles(title_continue, standard_content, cycle, begin_time, end_time, 30, 50)

    else:
        raise ValueError('Insert fitting value for time. Allowed values: "25min", "60min", "90min"')


    return content

    """There are six steps in the original technique:

    Decide on the task to be done.
    Set the pomodoro timer (traditionally to 25 minutes).[1]
    Work on the task.
    End work when the timer rings and put a checkmark on a piece of paper.[5]
    If you have fewer than four checkmarks, take a short break (3–5 minutes) and then 
    return to step 2; otherwise continue to step 6.
    After four pomodoros, take a longer break (15–30 minutes), reset your checkmark 
    count to zero, then go to step 1."""



#### creating the final note ####


print('Welcome to Pomodoro.py with a flexible note time. '+\
    '\nThe options for cycles are "25min" for now.') #"60min" and "90min" for now.')

user_input_end = input('Please enter a time (e.g. "20:30") when you want to be done.\n')

user_input_duration = input('Thanks. Please input duration of your pomodoro cycles.\n')

# opens browser and enters x-url-callback string
webbrowser.open(create_pomodoro(user_input_end,user_input_duration))

### function test ###
#create_pomodoro('20:30','25min')