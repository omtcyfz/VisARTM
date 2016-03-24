#!/usr/bin/env python3

from manage import *

clear()
create()

generate_sample('data')

add_dataset('Sample Dataset', 'data')
add_topicmodel('Sample Topicmodel', 'data', 1)
add_topicmodel('Sample Topicmodel', 'data', 1)
add_topicmodel('Sample Topicmodel', 'data', 1)

add_dataset('Second Dataset', 'data')
add_topicmodel('Sample Topicmodel', 'data', 2)
