# search1.py           5/20/08
#
# last modified 8/08/08
#
# John's first attempt to implement feature vs. conjunction search

import pygame, os, sys, math, datetime
# from text import *      # these are text-presentation routines Eric wrote
from pygame.locals import *
import random
from random import shuffle, choice
from operator import mod
from time import time  # for getting RTs
# from display import * # this is Eric's display code

# Define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,50)
ORANGE = (255,100,0)
BLUE = (50,150,255)
LIGHTBLUE = (100, 175, 255)
GRAY = (150,150,150)
DARKGRAY = (50, 50, 50)
DARKBLUE = (0,0,150) #(0, 0, 255)


random.seed(os.urandom(99))  # seed the random number generator

text_height = 30
# screen_height = 1000 # 768
# screen_width = 1500 # 1024

pygame.init()
screen = pygame.display.set_mode((0, 0), HWSURFACE)

screen_width, screen_height = screen.get_size()

pygame.mouse.set_visible(0)
pygame.font.init()
font = pygame.font.SysFont('times', text_height)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))


##subject_count_file = file('subject count.txt', 'r')
##subject_count = int(subject_count_file.read())
##subject_count_file.close()
##
##subject_number = subject_count + 1



# The display function (written by Eric)
# Displays multiple images at specified locations ('positions') on the screen

def display(images, positions, screen, background):
    """This function takes four arguments: images, positions, screen,\n
    and background.  Images is a vector with names of images to be displayed.\n
    Positions defines the placement each image receives on the rectangle.\n
    Screen and background define the screen size and other display features."""

    background = background.convert()
    background.fill((255, 255, 255, 255))

    try:
        rects = {}
        for f in range(len(images)):
            rects['rect' + str(f+1)] = images[f].get_rect()
            rects['rect' + str(f+1)].center = positions[f]

        screen.blit(background, (0, 0))

        for f in range(len(images)):
            screen.blit(images[f], rects['rect' + str(f+1)])

        pygame.display.flip()

    except:
        TypeError
        rect = images.get_rect()
        rect.center = background.get_rect().center
        screen.blit(background, (0, 0))
        screen.blit(images, rect)
        pygame.display.flip()


# some useful functions (written by JEH)

def get_keypress(trigger=None):
    all_done = False
    while not all_done:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                the_key = pygame.key.name(event.key) # <-- will return the key's name: a...z, 0...9, etc. Note: All letters lower-case
                if the_key == trigger or the_key.swapcase() == trigger:
                    return True # just quit, but return the "All good!" just to be nice
                else:
                    return the_key # quit, returning the name of the key they pressed (bearing in mind the lower-case thing)


##def key_to_letter(key_val, key_mod=1):# mod=1 means upper-case; mod = 0 means lower-case
##    # takes a key value as recorded by the event listner and returns the corresponding letter
##    # a (and A) is key value 97; z (and Z) is key value 122
##    #
##    # first, conver the key value to the ASCII value: A = 65; Z is 90,
##    #   so ASCII = key value minus 32
##    if key_mod == 0: # lower case
##        ascii = key_val
##    elif key_mod == 1: # upper case
##        ascii = key_val - 32
##    else:
##        print 'error in key_to_letter: key_mod = ',key_mod
##        # sys.exit()
##    if ascii < 256:
##        return chr(ascii)
##    else:
##        return '' # return space is not a valid ascii value
##
##def get_keypress(trigger=None):
##    # this is my version
##    # it waits for the user to enter a key in order to move on
##    all_done = False
##    while not all_done:
##        event_list = pygame.event.get()
##        for event in event_list:
##            # process the_event according to what type of event it is
##            if event.type == QUIT:
##                sys.exit()
##            elif event.type == KEYDOWN:
##                if event.key == K_ESCAPE:
##                    sys.exit(0)
##                elif key_to_letter(event.key, event.mod) == trigger:
##                    all_done = True
##                elif trigger == None:
##                    # if there's no trigger, then assume that the program
##                    # wants to know what the user entered
##                    all_done = True
##                    return key_to_letter(event.key, event.mod)

def blit_text(message, line):
    # formats, renders and blits a message to screen on the designated line
    #   but does NOT update the screen.
    # it is for use in cases where it is necessary to put several lines of
    #   text on the screen
    # 1) render the message
    the_text  = font.render(message, True, BLUE, (250,250,250))
    # 2) set it's location
    text_rect = [1,line * text_height + 1,screen_width,text_height]
    # 3) blit it to the screen
    screen.blit(the_text, text_rect)

def get_response():
    # gets a stimulus present (P) or absent (A) response from the subject 
    # and returns the response and the RT
    #
    # the following is for getting RT
    start_time = time()
    
    all_done = False
    valid_trial = True  # set to false if subject's first response is not A or P
    # Get user input while un-paused
    while not all_done:
        event_list = pygame.event.get()
        for event in event_list:
            # process the_event according to what type of event it is
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                all_done = True # end the trial on the first response
                if event.key == K_ESCAPE:
                    sys.exit(0)
                else:
                    response = pygame.key.name(event.key) # key_to_letter(event.key)
                if response in ('a','p','A','P'):
                    # Get RT
                    end_time = time()
                    RT = end_time - start_time
                    # print 'RT=',RT
                    screen.fill((250,250,250)) # blank the screen
                    pygame.display.update()
                    pygame.time.wait(1500) # wait 1500 ms before next trial
                    pygame.event.clear() # clear all events from the queue
                    return [response, RT, valid_trial]
                else:
                    # invald response: Inform subject of error
                    all_done = True
                    valid_trial = False
                    # clear the screen...
                    screen.fill((250,250,250))
                    error_message = response + ' is not a valid response.  Please respond only A or P.'
                    blit_text(error_message, 10)
                    blit_text('Press P or A to continue the experiment.',12)
                    pygame.display.update()
                    get_keypress()
                    pygame.event.clear() # clear all events from the queue
                    return [response, 0, valid_trial]

def mean_and_sd(data_vector):
    # takes one data vector and computes the mean and SD of the data therein
    mean = float(0.0)
    sd = float(0.0)
    n = len(data_vector)
    for datum in data_vector:
        mean += float(datum)
    if n > 0:
        mean = float(mean/n)
    for datum in data_vector:
        sd += float(pow(float(mean - datum), 2))
    if n > 0:
        sd = float(sd/n) # this is the Population (not sample) variance!
    sd = float(pow(sd, 0.5))
    return [mean, sd]

def print_data_string(mean, sd):
    # makes a printable string out of a mean and a sd
    string = '%.3f' % mean
    string = string + ' (%.3f)' % sd
    print string+'\t\t',



def designate_stimuli(target_index = None):
    # randomly designate images 0..3 to target, distractor 1 and distractor2
    # for the purposes of making stmulus construction easy
    #
    # first, if no target was specified,
    # randomly choose the target to be image 0, 1, 2 or 3
    # do this by randomly choosing a 0, 1, 2 or 3 and using it as the index, into image,
    #   of the target
    if target_index == None:
        target_index = -1
        while target_index < 0 or target_index > 3:
            target_index = int(round(random.random() * 3))
    # now, set the value of target to image[targer_index]
    target = images[target_index]

    # depending on which image is the target, the distractors will have to be chosen
    # differently:
    #   0 = redT, 1 = redL, 2 = greenT, 3 = greenL
    # e.g., if the target is redT (0), then the distractors must be redL (1) and greenT (2)
    if target_index == 0:   # target = redT
        dist1 = images[1]    # dist1 = redL
        dist2 = images[2]    # dist2 = greenT
        target_text = 'red T'
        dist1_text  = 'red L'
        dist2_text  = 'blue T'
    elif target_index == 1: # target = redL
        dist1 = images[0]    # dist1 = redT
        dist2 = images[3]    # dist2 = greenL
        target_text = 'red L'
        dist1_text  = 'red T'
        dist2_text  = 'blue L'
    elif target_index == 2: # target = greenT
        dist1 = images[0]    # dist1 = redT
        dist2 = images[3]    # dist2 = greenL
        target_text = 'blue T'
        dist1_text  = 'red T'
        dist2_text  = 'blue L'
    elif target_index == 3: # target = greenL
        dist1 = images[1]    # dist1 = redL
        dist2 = images[2]    # dist2 = greenT
        target_text = 'blue L'
        dist1_text  = 'red L'
        dist2_text  = 'blue T'
    else:
        print 'Error: Got an illegal target index in designate_stimuli()!'
        sys.exit()

    return [target, dist1, dist2, target_text, dist1_text, dist2_text]


def distance(loc1, loc2):
    # takes two two-dimensional vectors (locations) and computes the euclidean
    # distance between them
    distance = 0
    for i in xrange(len(loc1)):
        distance += pow((loc1[i] - loc2[i]),2)
    return pow(distance, 0.5)

def make_random_locations(n):
    # makes a list of n randomly chosen locations subject to the following constraints:
    #   each x coordinate is between minx and maxx
    #   each y coordinate is between miny and maxy
    #   no two locations are less than mindist from one another
    # these are the locaitons where the search target and distractors will be dislayed

    display_radius = 200
    mindist = 40
    mid_x = int(round(screen_width/2))
    mid_y = int(round(screen_height/2))

    minx = mid_x - display_radius
    maxx = mid_x + display_radius
    miny = mid_y - display_radius
    maxy = mid_y + display_radius
    
    locations = []
    for i in xrange(n): # make n locations
        # randomly choose x and y subject to the constraints above
        location_ok = False
        while not location_ok:
            location_ok = True # falsify when too-short distance found
            x = int(round(minx + random.random() * (maxx - minx)))
            y = int(round(miny + random.random() * (maxy - miny)))
            loc = (x, y)
            for other_loc in locations:
                if distance(loc, other_loc) < mindist:
                    location_ok = False
                    break # quit for other_loc loop
            if location_ok: locations.append(loc) # if it's ok, append to the list

    return locations
                

def make_display(num_target, num_dist_1, num_dist_2):
    # makes and returns a display: a list of stimuli (1 or 0 target, N distractor1, M dist. 2)
    #   and a corresponding list of randomly-chosen locations for those images
    stimuli = []
    # if there is a target, then append target (a global) to the list of stimuli
    if num_target > 0: stimuli.append(target)
    # append the requisite number of distractor-1s and -2s (dist1 and dist2, globals)
    for i in xrange(num_dist_1):
        stimuli.append(dist1)
    for i in xrange(num_dist_2):
        stimuli.append(dist2)
    # finally, make the locations of all these stimuli
    locations = make_random_locations(len(stimuli))
    # and return them both
    return [stimuli, locations]

def fixation_cross():
    # displays a fixation cross in center of screen for 750 ms
    screen.fill((250,250,250))# GRAY)  # fill it with a middle gray...
    mid_x = int(round(screen_width/2))
    mid_y = int(round(screen_height/2))
    vertical_rect = [mid_x - 2, mid_y - 20, 4, 40]
    horizontal_rect = [mid_x - 20, mid_y - 2, 40, 4]
    screen.fill(BLACK, vertical_rect)   # the vertical leg of the cross
    screen.fill(BLACK, horizontal_rect) # the horizontal leg
    pygame.display.update()
    pygame.time.wait(750)
    

class Block(object):
    # contains the info necessary to specify the nature of a block
    #   of trials
    def __init__(self, condition, dist1, dist2):
        self.condition = condition # 'feature' or 'conjunction'
        self.dist1     = dist1     # True or False: present distractor1
        self.dist2     = dist2     # True or False: present distractor2
        self.order     = 0  # order presented (1st, 2nd, etc.): compute at runtime
        self.trials    = [] # a record of which trials run in which order, plus data for each

class Trial(object):
    # contains the info about one trial:
    # which block target present/absent, how many distractors of each type,
    #   accuracy, validity (i.e.,valid response or not), and RT
    def __init__(self, block, target, dist1, dist2, num_dist_index):
        self.block  = block   # a pointer to the block that owns this trial
        self.order  = 0       # order presented (1st, 2nd, etc.): compute at runtime
        self.target = target  # 1 if present, 0 if absent
        self.dist1  = dist1   # 0...16
        self.dist2  = dist2   # 0...16
        self.num_dist_index = num_dist_index # the index into the array of num distractors
        valid       = False   # set to true if True
        correct     = False   # correct response or not: set to True if True
        rt          = -100    # -100 indicates no response; set to RT at runtime
        
def introduce_block(target_name, dist1_name, dist2_name):
    # tells the subject about the up-coming blocl of trials
    # also gives the subject the chance to rest between blocks
    
    screen.fill((250,250,250))# GRAY)  # fill it with a middle gray...
    message = 'On the next block of trials you will search for a '+target_name+' among '
    if dist1_name != '':
        message = message + dist1_name + 's'
    if dist1_name != '' and dist2_name != '':
        message = message + ' and '
    if dist2_name != '':
        message = message + dist2_name + 's'
    blit_text(message,5)
    blit_text('At this point you can take a moment to rest.',8)
    blit_text("Press P or A when you're ready to begin the next block",11)
    pygame.display.update()
    get_keypress()

def correlation(vector1, vector2, mean1, mean2):
    # computes the correlation coefficient between vectors 1 and 2
    # recall that the correlation is just the cosine of the angle of vectors
    # of difference scores
    #
    # before you even begin, make sure vectors 1 and 2 have te same dimensionality
    if len(vector1) == len(vector2):
        # all good: proceed to calculate correlation
        # first, make the vectors of difference scores
        dot_product = 0 # dot product of diff vector1 with diff vector2
        len_vect1   = 0
        len_vect2   = 0
        for i in xrange(len(vector1)):
            diff1 = vector1[i] - mean1
            diff2 = vector2[i] - mean2
            dot_product += diff1 * diff2 # update dot product
            len_vect1 += pow(diff1, 2)   # update vector1 length
            len_vect2 += pow(diff2, 2)   # update vector1 length
        # now take sqrt of current length values
        len_vect1 = pow(len_vect1, 0.5)
        len_vect2 = pow(len_vect2, 0.5)
        # now coompute correlation as dot product divided by product of lengths
        if (len_vect1 * len_vect2) > 0:
            correlation = dot_product/(len_vect1 * len_vect2)
        else: correlation = 0
        return correlation
    else:
        print 'ERROR: You tried to calculate the correlation of two vectors of different lengths'
        print 'Length of vector 1 =',str(len(vector1))
        print 'Length of vector 2 =',str(len(vector2))
        return 0

def write_summary_data(data_file, rt_data, acc_data):
    # computes summary data for one condition of feature or conjunction
    #  (over all conditions of num distractors) and saves it to file
    distractor_numbers=[2, 4, 6, 8, 12, 16] # YO! be sure this is consistent w/ the code!
    
    # response time data
    data_file.write('Response Times:\n')
    data_file.write('Num        \tTarget Absent\t\tTarget Present\n')
    data_file.write('Distractors\tMean\tSD\tMean\tSD\n')
    # iterate through all num distractors...
    for num_dist in xrange(len(rt_data)):
        text_line = str(distractor_numbers[num_dist])+'\t'
        # iterate through target absent/present
        for target in xrange(len(rt_data[num_dist])):
            [mean, sd] = mean_and_sd(rt_data[num_dist][target])
##            # * * * * This code modified 8/8/08
##            mean = float(0.0)
##            sd   = float(0.0)
##            n    = len(rt_data[num_dist][target])
##            if n > 0:
##                # compute the mean
##                for datum in rt_data[num_dist][target]:
##                    mean += datum
##                mean /= n
##                # compute the sd
##                for datum in rt_data[num_dist][target]:
##                    sd += pow((mean - datum),2)
##                sd = pow(sd, 0.5)
            # now add the mean and sd to the text line
            text_line = text_line + '%.4f\t' % mean
            if target == 0:
                text_line = text_line + '%.4f\t' % sd  # if target absent, end with a tab
            else:
                text_line = text_line + '%.4f\n' % sd  # if target present, end with new line
        # and finally, write the line to the file
        data_file.write(text_line)

    # accuracy data
    data_file.write('\n')
    data_file.write('Accuracy:\n')
    data_file.write('Num        \tTarget Absent\tTarget Present\n')
    data_file.write('Distractors\tNum Correct  \tNum Correct\n')
    # iterate through all num distractors...
    for num_dist in xrange(len(acc_data)):
        text_line = str(distractor_numbers[num_dist])+'\t'
        # iterate through target absent/present
        for target in xrange(len(acc_data[num_dist])):
            num_correct = 0
            # compute the mean
            for datum in acc_data[num_dist][target]:
                if datum == 1: num_correct += 1
            # now add the num correct and the total num to the text line
            text_line = text_line + str(num_correct)+' of '+str(len(acc_data[num_dist][target]))
            if target == 0:
                text_line = text_line + '\t'# if target absent, end with a tab
            else:
                text_line = text_line + '\n' # if target present, end with new line
        # and finally, write the line to the file
        data_file.write(text_line)

    #---------------------------------------------------
    #
    # save the data necessary to do the main analysis:
    #   you're going to compute each subject's search slope in each condition
    #   then just do a t-test on the slopes to see whether they are different
    #
    #   the slope is calculated as the rise over the run:
    #      the mean rise over the mean run
    #
    #   OR on the more general case, the slope = r * (std. dev. of y)/(std. of x)
    #   in this case:
    #      r = correlation between rt & num distractors
    #      std. of y is std of RT
    #      std. of x is std of # distractors
    #
    #   Intercept = mean_y - mean_x * slope
    #      ( recall: y = mx + b
    #        for y and x substitute mean_y and mean_x, then do the algebra:
    #        mean_y = m * mean_x + b
    #        mean_y - m * mean_x = b )
    #
    #--------------------------------------------------

    # prepare the data structures for the above analysis
    #
    # make vectors for rts and num distractors so you can easily compute correlations etc.
    # only enter rts and num distractors into vectors for trials with correct responses
    target_present_rts = []  # rts on correct target present trials
    target_absent_rts  = []  # rts on correct target absent trials
    target_present_num_dist = [] # num distractors on correct target present trials
    target_absent_num_dist  = [] # num distractors on correct target absent trials
    # iterate through all num distractors...
    for num_dist in xrange(len(acc_data)):
        # do target absent (acc_data[num_dist][0])
        for i in xrange(len(acc_data[num_dist][0])):
            # if response was accurate on this trial, then add the rt to the rt vector and the
            #   num dist to num_distractors vector
            if acc_data[num_dist][0][i] == 1:
                # add to the target absent rt vector... 
                target_absent_rts.append(rt_data[num_dist][0][i])
                # ... and add num distractors to target absent num distractors vector
                target_absent_num_dist.append(distractor_numbers[num_dist])
        # do target present (acc_data[num_dist][1])
        for i in xrange(len(acc_data[num_dist][1])):
            # of response was accurate on this trial, then add the rt to the rt vector and the
            #   num dist to num_distractors vector
            if acc_data[num_dist][1][i] == 1:
                # add to the target present rt vector... HERE 7/29/08
                target_present_rts.append(rt_data[num_dist][1][i])
                # ... and add num distractors to target present num distractors vector
                target_present_num_dist.append(distractor_numbers[num_dist])

    # now that you've got the vectors you need, calculate the stats you need
    [present_rt_mean, present_rt_sd] = mean_and_sd(target_present_rts)
    [absent_rt_mean, absent_rt_sd] = mean_and_sd(target_absent_rts)
    [present_num_dist_mean, present_num_dist_sd] = mean_and_sd(target_present_num_dist)
    [absent_num_dist_mean, absent_num_dist_sd] = mean_and_sd(target_absent_num_dist)

    # compute the correlations
    present_correlation = correlation(target_present_rts, target_present_num_dist, present_rt_mean, present_num_dist_mean)
    absent_correlation = correlation(target_absent_rts, target_absent_num_dist, absent_rt_mean, absent_num_dist_mean)

    # compute the slopes: slope = r * sd(y)/sd(x)
    if present_num_dist_sd > 0:
        target_present_slope = present_correlation * (present_rt_sd/present_num_dist_sd)
    else: target_present_slope = 0
    if absent_num_dist_sd > 0:
        target_absent_slope = absent_correlation * (absent_rt_sd/absent_num_dist_sd)
    else: target_absent_slope = 0

    # compute the intercepts
    target_present_intercept = present_rt_mean - target_present_slope * present_num_dist_mean
    target_absent_intercept  = absent_rt_mean  - target_absent_slope  * absent_num_dist_mean
    
    # and write the slopes and intercepts to file
    text_line = 'Target Present Slope = %.5f sec/distractor; ' % target_present_slope
    text_line = text_line + 'Intercept = %.5f\n' % target_present_intercept
    data_file.write(text_line)
    text_line = 'Target Absent Slope = %.5f sec/distractor; ' % target_absent_slope
    text_line = text_line + 'Intercept = %.5f\n' % target_absent_intercept
    data_file.write(text_line)
       
    data_file.write('\n')
            

def end_experiment():
    # saves the data to file, etc.

##    # update the subject count file
##    subject_count_file = file('subject count.txt', 'w')
##    subject_count_file.write(str(subject_number))
##    subject_count_file.close()
    
    # open the data file
    #data_file_name = 'data/data_'+str(subject_number)+'.txt'  # define the data file name
    # new 9/2/08: Usae time as filename to give each subject a unique file name
    end_time = time()
    data_file_name = 'data/'+str(end_time)+'.txt'
    data_file = open(data_file_name,'w')                 # open the data file for reading
    #
    # write file key, etc
    data_file.write('Data File: Feature vs. Conjunction Search Experiment.\n\n')
    data_file.write('Subject # '+data_file_name+'\n\n')
    data_file.write('Raw Data:  (Target = '+target_text+')\n\n')
    data_file.write('Cond.\tBlock\tTrial\tTarget\t'+dist1_text+'\t'+dist2_text+'\tCorrect\tRT\n\n')
    #
    #
    # save the raw data to file by blocks & trials
    for block in blocks:
        for trial in block.trials:
            if block.condition == 'conjunction': text_line = 'conj\t'
            else: text_line = 'feat\t'
            text_line = text_line + str(block.order)+'\t'
            text_line = text_line + str(trial.order)+'\t'
            text_line = text_line + str(trial.target) + '\t'
            text_line = text_line + str(trial.dist1) + '\t'
            text_line = text_line + str(trial.dist2) + '\t'
            if trial.correct:
                text_line = text_line + '1\t%.4f\n' % trial.rt # 1 for correct, plus save rt
            else:
                text_line = text_line + '0\n'  # 0 for incorrect
            data_file.write(text_line)
    #
    # save summary data
    #
    # prepare the data file
    data_file.write('\n\n')
    data_file.write('* * * * * Summary by Condition * * * * *\n\n')
    data_file.write('Feature Search Condition\n\n')
    data_file.write('Average over both distractors (target = '+target_text+'):\n')
    write_summary_data(data_file, rt_data['feature'], accuracy_data['feature'])

    data_file.write('Distractor '+dist1_text+' only (target = '+target_text+'):\n')
    write_summary_data(data_file, rt_data['dist1'], accuracy_data['dist1'])

    data_file.write('Distractor '+dist2_text+' only (target = '+target_text+'):\n')
    write_summary_data(data_file, rt_data['dist2'], accuracy_data['dist2'])

    data_file.write('Conjunction Search Condition (target = '+target_text+'):\n\n')
    write_summary_data(data_file, rt_data['conjunction'], accuracy_data['conjunction'])

    # close the data file
    data_file.close()
    #
    # inform the subject of end of experiment
    # first blank the screen and print the end-of-experiment message
    screen.fill((250,250,250))# GRAY)  # fill it with a middle gray...
    #
    blit_text('End of experiment.  Enter ctrl-F6 in the python shell to close this window.',10)
    # and update the screen
    pygame.display.update()



# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                               MAIN BODY
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# --------------------------------------------------------------------------------
# Read the stimulus images from file and store those images for later presentation
# --------------------------------------------------------------------------------
images_folder = 'images/'
file_names = ['redT','redL','greenT','greenL']
# read the files in letters/ and makes images for them
# these images (redL, redT, greenL, and greenT) will be printed
#   as many times as needed by the display() function
# file_names is a vector of file names of the files to read
#
# this function contans a bunch of very clever Python-specific Voodoo.
#   so when you get confused, refer back to these comments to
#   understand how it works.

for file_name in file_names:
    image = pygame.image.load(images_folder+file_name+'.png').convert() # read the image from the file & convert it (?)
    exec file_name+' = image'
    # Voodoo 1: this 'exec' makes the file name the key to the (surface of the) image in
    # python's "symbol table"

# vodoo 2: the 'images =...' below used the file names as keys to get at the
#   images in python's own private dictionary, aided by the 'vars()' voodoo,
#   which gives humble little you access to python's most private parts
images = [vars()['redT'],vars()['redL'],vars()['greenT'],vars()['greenL']]
# Now, executing this voodoo places those images into the vector 'images'
   
#-----------------------------------------------
# Introduction
#-----------------------------------------------
# blank the screen
screen.fill((250,250,250))# GRAY)  # fill it with a middle gray...
blit_text('This experiment investigates how people search for simple figures among',1)
blit_text('  arrays of distractors.',2)
blit_text('On each trial of the experiment, you will see an array of letters at',4)
blit_text('  random locations on the computer screen.',5)
blit_text('Your task is to indicate whether a target letter (e.g., a green T) is',7)
blit_text('  present in the array.',8)
blit_text('If the target is present, press the P key; if it is not present in the',10)
blit_text('  array, press the A key (for "absent").',11)
blit_text('Please respond to each array as quickly and accurately as you can.',13)
blit_text('Press any letter key (A...Z) to continue.',15) # John: Line 20 is the last line
# finally, update the screen
pygame.display.update()

get_keypress()

#-----------------------------------------------
# Get the condition (i.e., target)
#-----------------------------------------------
# query the subject for his/her condition code: a...d
# the condition code simply determines which letter serves as the target for this subject
# blank the screen
screen.fill((250,250,250))
blit_text('Please enter your condition letter (a, b, c or d):',10)
pygame.display.update()
# get the condition code
response = ''
while not (response in ['a','b','c','d']):
    response = get_keypress()

# set the condition based on the condition code (response)
if   response == 'a':
    target_index = 0
elif response == 'b':
    target_index = 1
elif response == 'c':
    target_index = 2
elif response == 'd':
    target_index = 3

# designate which stimuli will serve as target, distractor1 and distractor2
#   if a target index is provided as an argument, make that stim the target
#   otherwise, choose at random
[target, dist1, dist2, target_text, dist1_text, dist2_text] = designate_stimuli(target_index)

#-----------------------------------------------
# Display the target
#-----------------------------------------------
# next, show the subject what their target is
# clear the screen...
screen.fill((250,250,250))# GRAY)  # fill it with a middle gray...
# prepare the stimuli & locations "arrays" to pass to display()
#   in this case "stimuli" is simply the target and "locations" is the center of the screen
stimulus = [target]
location = [(int(round(screen_width/2)),2*text_height)]
# show the target
display(stimulus, location, screen, background)
message = 'Your target stimulus is a '+target_text+', as shown above.'
blit_text(message,4)
message = 'On each trial, if the array of letters contains a '+target_text+' then press the P ("present") key.'
blit_text(message,6)
message = 'If the array does not contain a '+target_text+' then press the A ("absent") key.'
blit_text(message,8)
blit_text('During the experiment, keep your fingers above the A and P keys.',10)
blit_text('Each trial will begin by showing a fixation cross in the center',12)
blit_text('  of the screen.',13)
blit_text('Please look at the fixation cross until the search display appears.',15)
blit_text('Please respond to each display as Quickly as you can Without Making Mistakes.',17)
blit_text('Press P or A to start a few practice trials.',20)
pygame.display.update()
get_keypress()

# -----------------------------------
# Practice trials
# -----------------------------------
#
# target present: conjunction
[stimuli, locations] = make_display(1, 2, 2) # 1 target, 2 distrator1, 2 distractor2
fixation_cross()
display(stimuli, locations, screen, background)
[response, RT, valid_trial] = get_response()
# target present: conjunction
[stimuli, locations] = make_display(1, 5, 5) # 1 target, 5 distrator1, 5 distractor2
fixation_cross()
display(stimuli, locations, screen, background)
[response, RT, valid_trial] = get_response()
# target absent: conjunction
[stimuli, locations] = make_display(0, 3, 3) # 1 target, 3 distrator1, 3 distractor2
fixation_cross()
display(stimuli, locations, screen, background)
[response, RT, valid_trial] = get_response()
# target absent: single feature
[stimuli, locations] = make_display(0, 0, 3) # 1 target, 3 distrator1, 3 distractor2
fixation_cross()
display(stimuli, locations, screen, background)
[response, RT, valid_trial] = get_response()
# target present: single feature
[stimuli, locations] = make_display(1, 0, 5) # 1 target, 3 distrator1, 3 distractor2
fixation_cross()
display(stimuli, locations, screen, background)
[response, RT, valid_trial] = get_response()
# target present: single feature
[stimuli, locations] = make_display(1, 4, 0) # 1 target, 3 distrator1, 3 distractor2
fixation_cross()
display(stimuli, locations, screen, background)
[response, RT, valid_trial] = get_response()
# target absent: single feature
[stimuli, locations] = make_display(0, 5, 0) # 1 target, 3 distrator1, 3 distractor2
fixation_cross()
display(stimuli, locations, screen, background)
[response, RT, valid_trial] = get_response()

# ---------------------------------------------------------------------
# Set up the data collection dictionaries: one for rts one for accuracy
# ---------------------------------------------------------------------
# dictionary references by 'conjunction', 'feature', dist1_text or dist2_text
#   feature is simply the union of dist1 data and dist2 data
#   we store both to make it easy to either lump the two single distractor
#   conditions (dist1 and dist2) together into simply the single feature condition
#   or to look for differences between the two kinds of distractors
# within each of these, there are 6 conditions corresponding to num distractors
#   and within each of These, there are two conditions: target present and target absent
# thus, each dictionary entry is a vector of 6 (num distractors) vectors of two (present/ansent)
#   vectors of rts (rt_data) or 1s and 0s (accuracy data)
# The following commented out code is evil: The "*6" operation makes six pointers to The SAME
#   Fucking Thing and Really fucks up data collection!
##rt_data = {'conjunction':[[[],[]]]*6,  # 6 numbers of distractors per condition X present/absent
##           'feature':[[[],[]]]*6,
##           'dist1':[[[],[]]]*6,
##           'dist2':[[[],[]]]*6}
##accuracy_data = {'conjunction':[[[],[]]]*6,  # 6 numbers of distractors per condition X present/absent
##                 'feature':[[[],[]]]*6,
##                 'dist1':[[[],[]]]*6,
##                 'dist2':[[[],[]]]*6}

rt_data = {'conjunction':[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]],
           'feature':[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]],
           'dist1':[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]],
           'dist2':[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]}
accuracy_data = {'conjunction':[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]],
                 'feature':[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]],
                 'dist1':[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]],
                 'dist2':[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]}

# -----------------------------------
# Start the experiment
# -----------------------------------
#
# ready screen
screen.fill((250,250,250))# GRAY)  # fill it with a very light gray...
blit_text("I hope you enjoyed that ('cause there's lots more coming).",5)
blit_text('Now get ready for the real experiment.',7)
blit_text('Remember to respond as quickly as you can Without Making Mistakes.',9)
blit_text('Place your fingers above the A and P keys...',11)
blit_text('... and press P or A to begin the experiment.',12)
pygame.display.update()
get_keypress()


# set up the blocks/conditions
# four blocks each of single feature (two blocks of dist1, two of dist2) and conjunction
# within each block, num distractors = 2, 4, 6, 8, 12 or 16
blocks = []

# below are two blocks for code development
##for i in xrange(2):
##    blocks.append(Block('conjunction',True,True)) # conj. condition, use dist1, use dist2

# Below are the real blocks
# create the conjunction blocks
for i in xrange(4): # 4
    blocks.append(Block('conjunction',True,True)) # conj. condition, use dist1, use dist2
# create the feature search blocks
# 1) with dist1
for i in xrange(2): # 2
    blocks.append(Block('feature',True,False)) # feat. condition, use dist1, do not use dist2
# 2) with dist2
for i in xrange(2): # 2
    blocks.append(Block('feature',False,True)) # feat. condition, do not use dist1, use dist2
# randomize the blocks' order
shuffle(blocks)

# -----------------------------------
# now run the blocks!
# -----------------------------------
block_number = 0
for block in blocks:
    block_number += 1
    block.order = block_number
    # set up the trials for this block
    if block.condition == 'conjunction':
        # conjunction search condition
        num_distractors = [1, 2, 3, 4, 6, 8] # this many of Both dist1 and dist2 (total num = [2, 4, 6, 8, 12, 16])
        # make all the trials for each num distractors
        for i in xrange(len(num_distractors)):
            # two target present trials and two target absent trials
            # arguments of Trial.__init__: block, target [1 or 0], num of dist1, num of dist2
            block.trials.append(Trial(block, 1, num_distractors[i], num_distractors[i], i)) # target present
            block.trials.append(Trial(block, 1, num_distractors[i], num_distractors[i], i)) # target present
            block.trials.append(Trial(block, 0, num_distractors[i], num_distractors[i], i)) # target absent
            block.trials.append(Trial(block, 0, num_distractors[i], num_distractors[i], i)) # target absent
    else:
        # feature search condition
        num_distractors = [2, 4, 6, 8, 12, 16] # this many of Either dist1 or dist2
        # make all the trials for each num distractors
        # only use one distractor or the other
        if block.dist1:
            for i in xrange(len(num_distractors)):
                # two target present trials and two target absent trials
                # arguments of Trial.__init__: block, target [1 or 0], num of dist1, num of dist2
                block.trials.append(Trial(block, 1, num_distractors[i], 0, i)) # target present
                block.trials.append(Trial(block, 1, num_distractors[i], 0, i)) # target present
                block.trials.append(Trial(block, 0, num_distractors[i], 0, i)) # target absent
                block.trials.append(Trial(block, 0, num_distractors[i], 0, i)) # target absent
        elif block.dist2:
            for i in xrange(len(num_distractors)):
                # two target present trials and two target absent trials
                # arguments of Trial.__init__: block, target [1 or 0], num of dist1, num of dist2
                block.trials.append(Trial(block, 1, 0, num_distractors[i], i)) # target present
                block.trials.append(Trial(block, 1, 0, num_distractors[i], i)) # target present
                block.trials.append(Trial(block, 0, 0, num_distractors[i], i)) # target absent
                block.trials.append(Trial(block, 0, 0, num_distractors[i], i)) # target absent
        else:
            print 'ERROR: Block',block.order,'has no specified distractors!'
    # randomize the order of the trials in the block
    shuffle(block.trials)
        
    # introduce the block
    if block.dist1:
        d1_text = dist1_text
    else:
        d1_text = ''
    if block.dist2:
        d2_text = dist2_text
    else:
        d2_text = ''
    introduce_block(target_text, d1_text, d2_text)

    # -----------------------------------
    # run the trials!
    # -----------------------------------
    trial_num = 0
    for trial in block.trials:
        trial_num += 1
        trial.order = trial_num
        [stimuli, locations] = make_display(trial.target, trial.dist1, trial.dist2)
        fixation_cross()
        display(stimuli, locations, screen, background)
        [response, trial.rt, trial.valid] = get_response()
        # figure out whether response was correct
        if trial.target == 1: # if target was present...
            if response in ('p', 'P'):
                trial.correct = True
            elif response in ('a','A'):
                trial.correct = False
            else:
                trial.correct = False
                trial.valid   = False
        elif trial.target == 0: # target was absent...
            if response in ('a','A'):
                trial.correct = True
            elif response in ('p', 'P'):
                trial.correct = False
            else:
                trial.correct = False
                trial.valid   = False
        # at this point, the data are stored in the trial object
        # store them also in the data dictionaries
        rt_data_matrix = rt_data[block.condition] # block.condition is either "conjunction" or "feature"
        acc_data_matrix = accuracy_data[block.condition]
        # now that you've got the right matrix, you need to access the correct cell:
        # [num_distractors][0] for target absent
        # [num_distractors][1] for target present
        # but be careful w/ num_distractors: it's not how many (2, 4, 6, etc.) but which
        #   num distractors Condition (0...5).  This is stroed in trial.num_dist_index
        if trial.correct:
            # if response correct, store the rt and store a 1 in the accuracy matrix
            rt_vector = rt_data_matrix[trial.num_dist_index][trial.target]
            rt_vector.append(trial.rt)
            acc_vector = acc_data_matrix[trial.num_dist_index][trial.target]
            acc_vector.append(1)
        else:
            # if error, store a 0 in the accuracy matrix and store the rt
            rt_vector = rt_data_matrix[trial.num_dist_index][trial.target]
            rt_vector.append(trial.rt)
            acc_vector = acc_data_matrix[trial.num_dist_index][trial.target]
            acc_vector.append(0)
        #------------------------
        # record the data!
        #------------------------
        # at this point, you have stored the data in either the 'conjunction' matrix
        #   or in the 'feature' matrix.  If you stored it in the 'feature' matrix,
        #   then also store it in the appropriate matrix of specific distractor data
        #   (i.e., either in dist1 or in dist2)
        if block.condition == 'feature':
            if trial.dist1 > 0:
                # store the data in the dist1 dictionaries
                rt_data_matrix = rt_data['dist1']
                acc_data_matrix = accuracy_data['dist1']
                if trial.correct:
                    # if response correct, store the rt and store a 1 in the accuracy matrix
                    rt_vector = rt_data_matrix[trial.num_dist_index][trial.target]
                    rt_vector.append(trial.rt)
                    acc_vector = acc_data_matrix[trial.num_dist_index][trial.target]
                    acc_vector.append(1)
                else:
                    # if error, store a 0 in the accuracy matrix and store the rt
                    rt_vector = rt_data_matrix[trial.num_dist_index][trial.target]
                    rt_vector.append(trial.rt)
                    acc_vector = acc_data_matrix[trial.num_dist_index][trial.target]
                    acc_vector.append(0)
            elif trial.dist2 > 0:
                # store the data in the dist2 dictionaries
                rt_data_matrix = rt_data['dist2']
                acc_data_matrix = accuracy_data['dist2']
                if trial.correct:
                    # if response correct, store the rt and store a 1 in the accuracy matrix
                    rt_vector = rt_data_matrix[trial.num_dist_index][trial.target]
                    rt_vector.append(trial.rt)
                    acc_vector = acc_data_matrix[trial.num_dist_index][trial.target]
                    acc_vector.append(1)
                else:
                    # if error, store a 0 in the accuracy matrix and store the rt
                    rt_vector = rt_data_matrix[trial.num_dist_index][trial.target]
                    rt_vector.append(trial.rt)
                    acc_vector = acc_data_matrix[trial.num_dist_index][trial.target]
                    acc_vector.append(0)

           
# finally, end the experiment: save data, close files, etc.        
end_experiment()

# goodbye message
screen.fill((250,250,250))# GRAY)  # fill it with a middle gray...
blit_text('All done.',5)
blit_text('Press any key to quit the experiment.',7)
pygame.display.update()
get_keypress()
# close the screen
pygame.display.quit()


