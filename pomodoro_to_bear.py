import webbrowser
import pandas as pd

"""  possible extensions:
-   put ASCII and Bear stuff in separate file and import 
-   Make cycle_duration duration (cd) variable and calculate break lengths based on cd (e.g. cd = 50, bl = 0.1*cd)
"""

### ASCII encodings for X-URL-Callback-String ###
# see https://ascii.cl
space = "%20"
left_bracket_round = "%28"
right_bracket_round = "%29"
left_bracket_square = "%5B"
right_bracket_square = "%5D"
triangle_left_open = "%3E"
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

# default title for bear note
begin = 'bear://x-callback-url/create?title=Pomodoro' + space

current_time = pd.Timestamp.now()

### break strings ###
pushup_break = 'Do'+space+'10'+space+'push-ups'
pull_up_break = pushup_break.replace('push','pull')
front_lever_break = 'Do'+space+'1min'+space+'front'+space+'lever'

# this longer break happens after a set of four pomodoros
longer_break = 'Take'+space+'a'+space+'longer'+space+'rest'+\
    colon+space+'Get'+space+'some'+space+'fresh'+space+'air'

# collect all breaks
breaks = [pushup_break,pull_up_break,front_lever_break]

def create_greeting(moment):

    """Prints customized welcome string based on time

    Args: 
        moment      (timestamp):  current time

    Returns:
        greeting    (string):     the final welcome string

    """

    if moment.hour < 12:

        greeting = 'Good morning'

    elif moment.hour < 20:

        greeting = 'Good evening'

    else:

        greeting = 'Good night'

    return greeting

def make_cycles(title_continue, standard_content, cycle_duration, begin_time, end_time):

    """concatenates for each cycle_duration a new string to the main X-URL-Callback string

    Args:
        title_continue      (string): beginning of the X-URL-Callback String + title
        standard_content    (string): custom header for Bear note
        cycle_duration      (int): cycle duration in minutes, e.g. '25'
        begin_time          (timestamp): current time rounded to nearest 5mins
        end_time            (timestamp): converted String from user input into timestamp
        long_time           (int): longest duration for a cycle_duration (once per three cycles)

    Returns:
        content             (string): the content for the entire pomodoro note

    """
    # setting short cycle time to e.g. 25 if input was 20
    short_time = cycle_duration * 1.2
    long_time = cycle_duration * 2

    # preparing the string with length of cycle_duration as text in between
    content = title_continue + str(cycle_duration)+'min' + standard_content 
    
    # add duration to begin_time
    cycle_end_time = begin_time + pd.Timedelta(minutes=cycle_duration)

    
    # initialize variables before while loop
    i,j = 1,0

    # end before or on time supplied by user
    while cycle_end_time < end_time:
        
        # every fourth cycle
        if i%4 == 0:
            
            break_elem = longer_break

            # concatenate strings for cycle content
            cycle_content, begin_time, cycle_end_time = add_cycle_content(break_elem, 
                                                    begin_time, cycle_end_time, i, long_time)

            content = content + cycle_content

        # every other cycle
        else:
            
            break_elem = breaks[j]
            
            cycle_content, begin_time, cycle_end_time = add_cycle_content(break_elem, 
                                                    begin_time, cycle_end_time, i, short_time)

            content = content + cycle_content

            # circling through [0,1,2] for j to get text at breaks[j]
            if j < 2:

                j += 1

            else:

                j = 0
        
        i += 1
    
    print('amount_cycles: ', i-1)

    return content
    

def add_cycle_content(break_element, cycle_begin_time, 
                        cycle_end_time, cycle_number, minute_difference):

    """concatenates for each cycle a new string to the main X-URL-Callback string

    Args:
        break_element       (String):  message for break lines 
        cycle_begin_time    (Timestamp): when the cycle starts
        cycle_end_time      (Timestamp): end of current cycle
        cycle_number        (integer): current cycle number

    Returns:
        cycle_content (string): the X-URL-Callback string for one cycle

    """

    cycle_content = new_line + horizontal_line + new_line + hashtag + hashtag +space +\
                        'Cycle' + space +str(cycle_number)+ comma + space +\
                        cycle_begin_time.strftime('%H:%M')+'-'+\
                        cycle_end_time.strftime('%H:%M')+\
                        new_line + new_line + new_line + horizontal_line + \
                        new_line + colon + colon + 'Break' + space +str(cycle_number)+\
                        comma + space + cycle_end_time.strftime('%H:%M')

    # change times with minute difference depending on which interval is wished
    cycle_begin_time = cycle_begin_time + pd.Timedelta(minutes=minute_difference)
    cycle_end_time = cycle_end_time + pd.Timedelta(minutes=minute_difference)

    # also, make this statement bold at the same time
    cycle_content = cycle_content +'-'+cycle_begin_time.strftime('%H:%M')+\
        space + '-' + triangle_left_open +space +'*'+break_element+'*'+ colon + colon


    return cycle_content, cycle_begin_time, cycle_end_time


def create_pomodoro(end_time, cycle_duration):

    """takes an end date and creates cycles from right now (normalized to
    a 5-minute time) until the end date.

    Args:
        end_date        (string): time in format "hh:mm", e.g. "20:30"
        cycle_duration  (int): pomodoro duration in mins, e.g. 60

    Returns:
        string

    # Add a section detailing what errors might be raised
    Raises:
        ValueError: If `cycle_duration` is not one of the defined strings.
    """

    # rounding to the nearest 5min, beware, this can also lead to earlier time
    begin_time = pd.Timestamp.now().round('5min')

    # getting date info from timestamp
    year = begin_time.year
    month = begin_time.month
    day = begin_time.day

    # case next day
    if day_change == True:
        day = day + 1
    else:
        pass

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
    standard_content = space+'cycle&open_note=yes&text='+hashtag+'pom'+\
        'odoro' + slash + str(cycle_duration) + 'min' + space + hashtag + \
            'diary' + slash + str(year) + slash +\
            month_prefix_zero + slash + day_prefix_zero +\
            new_line + '---'+ new_line + 'Flow' + colon + left_bracket_square +\
            left_bracket_square + 'Pomodoro'+ space+ '-' + space + 'Technique'+\
            right_bracket_square + right_bracket_square +\
            new_line +'---' + new_line + hashtag + hashtag + space + 'Summary' + new_line


    # use a break which is 1.3 times as long as a normal cycle
    content = make_cycles(title_continue, standard_content, cycle_duration, 
                            begin_time, end_time)



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
if __name__ == '__main__':

    print(create_greeting(current_time)+' to Pomodoro.py with a flexible note time.')

    input_text = 'Please enter a time when you want to be done and the'+\
                ' preferred focus time per cycle in mins (e.g. "20:30,25").'+\
                    '\n Time per cycle should be (5,300) minutes and will be rounded to closest 5mins.'
    try: 
        user_input = input(input_text+'\n').split(',')
    except: 
        raise ValueError('Enter in the format "hh:mm",mm.')

    end_time, cycle_length = user_input[0], int(user_input[1])

    hours, minutes = int(end_time.split(':')[0]), int(end_time.split(':')[1])

    # round to nearest multiple of 5
    cycle_length = round(5 * (cycle_length / 5))

    # minimum length 4 mins
    try:
        assert cycle_length > 4
    except:
        raise ValueError('Enter cycle length larger than 4 minutes.')

    # max length capped at 301 mins
    try:
        assert cycle_length < 301
    except:
        raise ValueError('Enter cycle length up to 300 minutes.')

    same_day_ts = pd.Timestamp(year = current_time.year, month = current_time.month, 
                                day = current_time.day, hour = hours, minute=minutes) 

    next_day_ts = same_day_ts + pd.Timedelta(days=1)
    first_end_time = current_time + pd.Timedelta(minutes=cycle_length)

    # dummy for yes_no functionality for now
    day_change = False

    # catching too low inputs for time with option to extend to next day
    try: 
        assert same_day_ts > first_end_time
    except:
        yes_no = input('Do you want to use Pomodoro until the next day? y/n \n')

        if yes_no == "y":
            assert next_day_ts > first_end_time
            day_change = True
        else:
            raise ValueError('Enter an ending which allows for at least one cycle and ends today.')


    # opens browser and enters x-url-callback string
    webbrowser.open(create_pomodoro(end_time,cycle_length))
