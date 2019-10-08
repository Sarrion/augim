default_transitory = [
    'take original pick all apply all name_it firsts',
    'take firsts pick 0 apply all_except crop name_it seconds',
    'take firsts pick 3 apply all_except crop,rotation,homography,noise name_it thirds',
    'take firsts pick 10 apply flip_lr,flip_ud,hue,brightness,saturation,contrast name_it lasts'
]


default_stable = 'rotation,homography,hue,brightness,saturation,contrast'