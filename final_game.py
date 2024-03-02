#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

class Rectangle:
    def __init__(self, faceX, faceY, faceZ): #defines the first 3 planes of faces
        self.z = faceZ
        self.y = faceY
        self.x = faceX
        
    def bounds(self, x, y, z, xbool, ybool, zbool): 
        if xbool:
            xbounds = np.array([self.x - x, self.x])
        else:
            xbounds = x
            
        if ybool:
            ybounds = np.array([self.y - y, self.y])
        else: 
            ybounds = y
            
        if zbool:
            zbounds = np.array([self.z - z, self.z])
        else:
            zbounds = z
            
        return [xbounds, ybounds, zbounds]
    
    def color(self, ambient, diffuse, specular, shine, reflection):
        if type(ambient) != np.ndarray or type(diffuse) != np.ndarray or type(specular) != np.ndarray:
            print('make sure to use correct type of stuff')
            return None
        else:
            return ambient, diffuse, specular, shine, reflection
    

def normalize(vector):
    return vector / np.linalg.norm(vector)

def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

def intersect(ray_origin, direction_vector, check_coord, axis_number, x_range, y_range, z_range):
    axis_number -= 1    
    ranges = [x_range, y_range, z_range]
    t = np.linspace(0, 5, 100)
    accuracy = (max(t)-min(t))/len(t)
    tvals = []
    tval = None
    for i in range(len(t)):
        v = ray_origin + direction_vector * t[i]
        if abs(v[axis_number] - check_coord) <= accuracy:
            for j in range(len(ranges)):
                if type(ranges[j]) == np.ndarray:
                    if v[j] <= max(ranges[j]) and v[j] >= min(ranges[j]):
                        tval = t[i]
                    else:
                        tval = None
                        break
        if tval != None:
            tvals.append(tval)

    l = np.mean(tvals)
    if np.isnan(l):
        return None
    else:
        return l

def nearest_intersected_object(objects, ray_origin, direction_vector, check_coord, axis_number):
    distances = []
    intersection = intersect(ray_origin, direction_vector, check_coord, axis_number, objects[0], objects[1], objects[2])
    if intersection != None:
        distances.append(intersection)
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects 
    return nearest_object, min_distance

def ray_trace(objects, colors):
    print("Rendering your object. Can take up to a minute. (It used to take an hour so don't complain!!!)")
    image = np.zeros((height, width, 3))
    for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
            pixel = np.array([x, y, 0])
            origin = camera
            direction = normalize(pixel - origin)
            color = np.zeros((3))
            reflection = 1
            for part in range(len(objects)):
                for k in range(max_depth):
    
                    ## Checks for ray intersection at nearest object
                    nearest_object, min_distance = nearest_intersected_object(objects[part], origin, direction, -1, 3) 
        
                    if nearest_object is None:
                        break
                    intersection = np.array(origin + min_distance * direction)
                    
                    ## prepares new ray origin close to intersection in direction of 
                    for h in range(len(nearest_object)):
                        if type(nearest_object[h]) != np.ndarray:
                            diff = np.copy(intersection) 
                            diff[h] = intersection[h]-1
                            break
                        
                    normal_to_surface = normalize(intersection - diff)
    
                    shifted_point = intersection + 1e-5 * normal_to_surface
                    intersection_to_light = normalize(light['position'] - shifted_point) ## direction to light
                
                    ## Color gets calculated after this point
                    illumination = np.zeros((3))
        
                    # ambient
                    if objects[part] == nearest_object:
                        illumination += colors[part][0] * light['ambient']
                        # diffuse
                        illumination += colors[part][1] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface)
                        # specular
                        intersection_to_camera = normalize(camera - intersection)
                        H = normalize(intersection_to_light + intersection_to_camera)
                        illumination += colors[part][2] * light['specular'] * np.dot(normal_to_surface, H) ** (colors[part][3] / 4)
                        # reflection
                        color += reflection * illumination
                        reflection *= colors[part][4]
                        
                        origin = shifted_point
                        direction = reflected(direction, normal_to_surface)
    
            image[i, j] = np.clip(color, 0, 1)
    
    plt.imsave('image.pdf', image)
    print('All done! You can find this image in the same directory in which you are running this game.')

width = 100
height = width

max_depth = 3

camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio) # left top right bottom

light = { 'position': np.array([1, 1, 1]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }

############################ KEY KEY KEY KEY KEY #############################
#                 key handle               key stem(spine)         tooth                       tooth                       lil square
key_parts = [Rectangle(7/6, 1/3, -1), Rectangle(1/2, 1/6, -1), Rectangle(-5/6, -1/6, -1), Rectangle(-1/2, -1/6, -1), Rectangle(-2/3, -1/6, -1)]
key = [key_parts[0].bounds(2*(1/3), 2*(1/3), -1, True, True, False), key_parts[1].bounds(5/3, 1/3, -1, True, True, False), key_parts[2].bounds(1/6, 1/3, -1, True, True, False),  key_parts[3].bounds(1/6, 1/3, -1, True, True, False), key_parts[4].bounds(1/6, 1/6, -1, True, True, False)]

key_color = []
for part in range(len(key_parts)):  
    key_color.append(key_parts[part].color(np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([1, 1, 1]), 100, 0.5))

########################### SWORD SWORD SWORD ###############################
#                 grip                       vertical thingy           blade
sword_parts = [Rectangle(7/6, 1/12, -1), Rectangle(5/6, 1/2, -1), Rectangle(2/3, 1/6, -1)]
sword = [sword_parts[0].bounds(1/3, 1/6, -1, True, True, False), sword_parts[1].bounds(1/6, 1, -1, True, True, False), sword_parts[2].bounds(7/6, 1/3, -1, True, True, False)]

# tip
maxim = 1/6
yinc = 1/42
l = 2
for j in reversed(np.linspace(-7/6, -1/2, 7)):
    maxim -= yinc
    minim = 2* maxim
    l += 1
    sword_parts.append(Rectangle(j, maxim, -1))
    sword.append(sword_parts[l].bounds(2/21, minim, -1, True, True, False))

sword_color = [sword_parts[0].color(np.array([0.3961, 0.2627, 0.1294]), np.array([0.3961, 0.2627, 0.1294]), np.array([0, 0, 0]), 0, 0.25), sword_parts[1].color(np.array([0.1, 0.1, 0.1]), np.array([0.1, 0.1, 0.1]), np.array([1, 1, 1]), 100, 0.5),  sword_parts[2].color(np.array([1-0.8275, 1-0.8275, 1-0.8275]), np.array([1-0.8275, 1-0.8275, 1-0.8275]), np.array([1, 1, 1]), 100, 0.5)]

l = 3
for i in range(7):  
    sword_color.append(sword_parts[l].color(np.array([1-0.8275, 1-0.8275, 1-0.8275]), np.array([1-0.8275, 1-0.8275, 1-0.8275]), np.array([1, 1, 1]), 100, 0.5))
    l+=1
################### STORY BEGINS BELOW #########################################


keys = False
blood_room = False
prisoner_records = False
dark_letter = False
spider = False
greatsword = False


def intro_hall():      
    print("""
    The room exits into a long dark hallway. On your left there is a lit 
    torch that you grab so you can see your surroundings. There is no 
    doubt in your mind that you are inside a dungeon, along the walls of 
    the hallways you see all the tools of imprisionment that you can 
    think of. Chains, handcuffs, whips, pliers, everything. However, it 
    is clear to you that none of these tools have been used in a very long 
    time, the chains are broken and rusted, the leather used to make the 
    whip is dried out, and the pliers can't even be opened due to the rust. 
    As you make your way down the hallway, you feel uneasy and vulnerable, 
    almost as if you are being watched. Nonetheless, you must find a way 
    out of here.
          """) 
    input("Press <enter> to continue\n")    
    print("""
    Once you reach the end of the hallway you see three exits. The room 
    to the left is too dark to see what is inside of it, and a dry pool 
    of blood seemed to emerge from a room where a fight had taken place 
    and leads to a room in which you hear something shuffling around.
          """)
    options = ['follow shuffling sounds', 'bloody room', 'dark room']
    print('options',options)
    userInput = input('Where would you like to go?:\n')
    while userInput not in options:
        print('I do not recognize that command. Try again.')
        print('options', options)
        userInput = input('Where would you like to go?:\n')
    if userInput == options[0]:
        spider_room()
    if userInput == options[2]:
        darkroom() 
    if userInput == options[1]:
        bloody_room()

def bloody_room():
    print("""
    You follow the trail of blood into the room to find what seems to 
    have been the location of a fight. Smears of blood sourround you and 
    the smell of rotted flesh overwhelms your sense of smell. However, it 
    is not the human blood that disturbs you, it is the glowing green 
    fluid that is mixed in with it...
          """)
    global blood_room
    if blood_room:
        if key:
            print("""
    There are two ways to exit the room. Return to the key room, or go 
    into the hallway you first stepped out of.
            """)
            options = ['key room', 'back to hallway', 'bbkjbkhbkh']
            userInput = input('what would you like to do? [options: key room/back to hallway]\n')
        else: 
            print("""
    There are two ways to exit the room. Explore the room with the shiny 
    object inside of it, or go into the hallway you first stepped out of.      
                  """)
            options = ['shiny object room', 'back to hallway', 'kbhbkjbb']
            userInput = input('what would you like to do? [options: shiny object room/back to hallway]\n')
    else: 
        print("""
    You notice a small bag on the floor, there seems to be something 
    inside of it. There is also a exit that has been slightly opened just 
    enough to notice a shiny object inside that room. The blood 
    leads out of the room into the hallway you first stepped out of.
          """)
        blood_room = True
        options = ['shiny object room', 'back to hallway', 'inspect bag']
        print('options', options)
        userInput = input('what would you like to do?')
    check_bag = True
    while True:
        while userInput not in options:
            print('I do not recognize that command. Try again.')
            print('options:', options)
            userInput = input('what would you like to do?\n')
        if userInput == options[0]:
            key_room()
        elif userInput == options[1]:
            intro_hall()
        elif userInput == options[2]:
            if check_bag == True:
                check_bag = False
                print("""
    You pick up the bag to notice that it was ripped off of its owner. 
    It likely belonged to whomever was in the fight that happened in 
    the room. Inside the bag is a vial containing leeches which can 
    help replenish your vitality. You drop the bag on the floor and 
    go on.
                      """)
                print('options:', options)
                userInput = input('what would you like to do?\n')
            elif check_bag == False:
                print('You already did that!')
                userInput = input('what would you like to do?\n')

def darkroom():
    print("""
    You enter the dark room. Even with your lit torch, you can't see very
    far ahead of you. You slowly make you way around the room to find 
    that it is not very large. There are a few bookshelves that seem to 
    keep prisoner records and a table at the center of the room with a 
    letter on it. Through one of the doorways you see an entrance to an 
    armory You are able to exit into the hallway from which you first 
    emerged from or you can enter the armory.
          """)
    global dark_letter 
    global prisoner_records
    global name
    if dark_letter:
        options = ['go to hallway', 'enter armory', 'examine prisoner records']
        if prisoner_records:
            options = ['go to hallway', 'enter armory']
    else:
        options = ['go to hallway', 'enter armory', 'examine prisoner records', 'examine letter']
    while True:  
        print('options', options)
        userInput = input("What would you like to do?")
        while userInput not in options:
            print('options', options)
            print('I do not recgonize that command.')
            userInput = input("What would you like to do?")
        if userInput == options[0]:
            intro_hall()
        elif userInput == options[1]:    
            armory()
        try:
            if userInput == options[2]:
                if prisoner_records == False:
                    prisoner_records = True
                    print("""
    You begin reading one of the record books. It contains the 
    various names, crimes, and punishments of all the previous prisoners 
    that have been in these dungeons. However you notice, as you flip 
    through the pages everything starts repeating. The same names 
    reappear again and again, but as you reach the last page... 
    its blank. There is nothing on it but a single name """+ name+ """" 
    
    "That's odd", You think to yourself as you place the book back
                      """)
                elif prisoner_records == True:
                    print('You already did that!')
            elif userInput == options[3]:
                if dark_letter == False:
                    dark_letter = True
                    print("""
    You examine the letter. It isnt very long.
    
    "Why do they keep thinking they can escape. I have seen these 
    men die too many times and for too long. I do not know when I 
    got here, just that my duty is to keep records of all those who 
    find themselves in this godforsaken dungeon. However, I have 
    aged considerably compared to when I first awoke and my time 
    here is limited. I fear this will be the last thing that I 
    will write. If you are reading this, may God follow you in 
    your journey." """)
                    print('options:', options)
                    userInput = input('what would you like to do?\n')
                elif dark_letter == True:
                    print('You already did that!')
                    print('options', options)
                    userInput = input('what would you like to do?\n')
        except:
            pass

def spider_room():    
    global spider
    global keys
    if spider:
        if keys:
            print("""
    You walk into the room in which you slayed the spyder, where its
    corpse twitches every so often. The smell of its rotting flesh
    disgusts you. You can return to the key room, or you can return 
    to the hall from which you first emerged.
    """)
            options = ['go to key room', 'return to hallway']
        else:
            print("""
    You walk into the room in which you slayed the spyder, where its
    corpse twitches every so often. The smell of its rotting flesh
    disgusts you. There is a room where you can see a shiny object through
    acracked open door, or you can return to the hall from which you 
    first emerged.""")
            options = ['go to shiny object', 'return to hallway']
        triumphed = True
    else:
        triumphed = False
        print("""
    You follow the trail of blood into the room in front of you. As you 
    continue to follow the trail slowly, you notice spider webs surround 
    you in all directions. As you wave your torch around to see your 
    surroundings you see spiders of different sizes scurry away from you,
    dissapearing into the many webs. You continue to follow the trail until
    you realize that it ends at the center of the room. All the evidence
    that is left of the person that perished is scraps of their armor that
    is scattered around the end of the trail. 
              """)
        input('press <Enter> to continue\n')
        print("""
    You begin to hear a light continuous tapping on your helmet as you stand there. 
    When taking it off to look at it you realize that your helmet is covered
    in the green fluid that you saw in the previous room. 
    
    "It's... above me..." You realize with horror.
    
    You slowly look up as the green liquid keeps dripping on you, making 
    sure to not make any sudden movements. As the creature gets into your 
    field of view, you begin to notice its long, thin legs, that are as 
    sharp as spears, there is eight of them. Its large bulbous abdomen 
    is as large as the rest of the creature. And what is hanging about 
    two feet above your head are the fangs of a 10 foot tall arachnid that 
    seems to have found it next meal. 
              """)
        input('press <Enter> to continue\n')
        print("""
    Before you're able to run, the creature picks you up with its fangs.
    You drop your torch as you struggle to get free from it. As it tries
    to wrap you up in its thick webbing you reach for your sword and strike 
    at one its many legs. The arachnid squirms in pain and drops you. 
    After you pick up your sword, you nervously check where the fangs 
    punctured, expecting to see blood spilling out of you. However, the 
    chainmail you had on was able to stop the fangs from ripping into your 
    flesh. After you pick up your weapon and torch you see the arahcnid 
    lower itself from the ceiling onto the floor. You notice that the leg 
    that you struck is dragging behind it, almost fully severed off. With 
    its fangs, the creature rips off the hurt leg and faces you. You notice
    that the spider has a spear that was stabbed onto the bottom of its 
    abdomen and the green fluid that is dripping off of it has been its 
    blood all along. Your torch seems to keep it at bay, so it seems that
    it does not like the light.
              """)
        options = ['charge it with your sword', 'throw torch at it', 'run away']
    if triumphed:
        print('options:', options)
        userInput = input('what would you like to do?\n')
        while userInput not in options:
            print('I do not recognize that command. Try again.')
            print('options:', options)
            userInput = input('what would you like to do?\n')
        if userInput == options[0]:
            key_room()
        elif userInput == options[1]:
            intro_hall()
    else:
        while True:
            print('options:', options)
            userInput = input('what would you like to do?\n')
            while userInput not in options:
                print('I do not recognize that command. Try again.')
                print('options:', options)
                userInput = input('what would you like to do?\n')
            if userInput == options[0] or userInput==options[1]:
                if userInput == options[0]:
                    print("""
    With your sword raised, you charge at the arachnid. You 
    swing at its head, and you slash through its face, cutting 
    off one of its fangs. As it screaches in pain ot swipes at 
    your legs, knocking you over. You drop both your torch 
    and sword. The creature raises its front legs to pounce on 
    you. As its sharp legs close in on you, you roll beneath it.
                          """)
                elif userInput == options[1]:
                    print("""
    You throw your torch direcly at the creature, hitting it on
    its face. The arachnid screaches as the flames burn its 
    eyes. As its scurries to put the flame out you unsheath 
    your sword, recognizing that theres nothing holding the 
    creature away from you any longer. The creature charges at 
    you after it the flames have gone away, tackling you and 
    knocking your sword off your hand. You fall on your back 
    and see the arachnid raise its front legs to pounce on you. 
    As its sharp legs close on you you roll underneath it. 
                          """)
                print("""
    You try to crawl behind the spider as its strikes at 
    you with its legs. It stabs its leg into your bicep and 
    tries to drag you out from underneath it, but it struggles 
    due to its missing leg.You look around desperately trying 
    to find something to defend yourself with until you see 
    the spear that is stuck in its abdomen. With all your 
    force you kick the spear deeper into its abdomen. The creature 
    lets out a final screach of pain, before falling over your 
    legs. You pull your legs out from underneath and stand up. 
    You see that your kick full drove the spear through its 
    abdomenn onto the other side. You pick up your sword 
    and torch.
                          """) 
                spider = True
                input('press <enter> to continue')
                spider_room()
            elif userInput == options[2]:
                print("""
    You decide to not risk you life so you run towards the exit.
    As you run, you hear the arachnid run towards you at full speed.
    You near the door, but the sounds of its footsteps grow louder 
    too. Just as you run across the door the spider strikes at your 
    back with one of its legs, breaking though your armor and 
    cutting into your skin. The creature is too large to fit through 
    door. It desperately tries to reach at you but you are too far
    away for it to get to you. After a few moments of it trying 
    to reach you, it return into the darkness from which you found 
    it.
                      """) 
                input('press <enter> to continue')
                spider_room()

def key_room(): 
    global keys
    if keys:
        print("""
    You walk into the key room. Various keys of different shapes, sizes, and 
    complexity hang from the walls. These keys are old. They are rusted, and 
    some even broken. Other than that there is three doorways to take. The one 
    that leads into a bloody room, one that leads to another cell, and the one 
    that leads to the room in which you heard scurrying. """)
        options = ['bloody room', 'cell room', 'scurrying room']
    else: 
        print("""
    You walk through the half opened door to find what seems to be a key 
    room. Various keys of different shapes, sizes, and complexity hang 
    from the walls. These keys are old. They are rusted, and some even 
    broken. It's pretty clear that most of them haven't been used in a 
    long time, except for one. In the middle of the room is a table with 
    the skeletal remains of someone who passed so long ago. On the table 
    is a single silver key. Other than that there is three 
    doorways to take. The one that leads into a bloody room, one that 
    leads to another cell, and the one that leads to the room in which you 
    heard scurrying. """)
        options = ['bloody room', 'cell', 'scurrying room', 'inspect key']
        
    print('options', options)
    check_key = True
    userInput = input('what would you like to do?\n')
    while True:
        while userInput not in options:
            print('I do not recognize that command. Try again.')
            print('options', options)
            userInput = input('what would you like to do?\n')
        if userInput == options[2]:
            spider_room()
        elif userInput == options[0]:
            bloody_room()
        elif userInput == options[1]:
            cell_room() 
        try:
            if userInput == options[3]:
                if check_key == True:
                    check_key = False
                    keys = True
                    print("""
    This key seems much newer than any of the rest, like if 
    it has never been used. It's heavier than you would expect, 
    but other than that, it's just a key. You place it in your 
    pocket in case it is useful later on.
                          """)
                    ray_trace(key, key_color)      
                    userInput = input('what would you like to do? [options: scurrying room/bloody room/cell]\n')
                elif check_key == False:
                    print('You already did that!')
                    userInput = input('what would you like to do? [options: scurrying room/bloody room/cell]\n')
        except:
            pass
        
def cell_room(): 
    print("""
    You walk into the cell room to find that it is much larger than you 
    anticipated. There a large hole in one of the walls, which looks like
    it was caused by something large breaking out. Scattered across the 
    cell are long reinforced chains, however, whatever they were meant to 
    hold down was still able to break out of them. It becomes clear to you 
    that this cell was only meant to hold only one creature, larger than 
    anything you have ever seen. You see that there is an exit onto a long 
    hallway.
          """)
    input("Press <enter> to continue\n")
    print("""
    Just as you were about to approach the broken wall, you hear the monster
    that was supposed to be held inside this cell. Its roar is so loud that
    you can feel the sound in your chest. Your surroundings shake at every
    step that it takes like if they too were afraid of what lie beyond. 
          """)
    while True:  
        options = ['go to key room', 'go into long hallway', 'exit through broken wall']
        print('options', options)
        userInput = input("What would you like to do?\n")
        while userInput not in options:
            print('I do not recognize that command.')
            userInput = input("What would you like to do?\n")
        if userInput == options[0]:
            key_room()
        elif userInput == options[1]:    
            armory()  
        elif userInput == options[2]:
            options = ['continue', 'go back']
            userInput = input('You are now entering the room. Once you enter this room, you can no longer go back to continue exploring. If you would like to continue onwards type "continue." If you changed your mind type "go back."\n')
            while userInput not in options:
                print('I do not recgonize that command.')
                userInput = input('You are now entering the final room. Once you enter this room, you can no longer go back to continue exploring. If you would like to continue onwards type "continue." If you changed your mind type "go back."\n')
            if userInput == options[0]:
                final_room()
            elif userInput == options[1]:
                print("""
                      You decide to continue exploring through the dungeons 
                      before facing the monster that lies ahead.
                      """)
                     
def armory():
    print("""
    You enter the armory. As you look around you realize that there is 
    not a single weapon in the room!
    
    "What's the point of an armory if youre not going to have any weapons
    to store!?" You exclaim to yourself. 
    
    You also realize that the armory isn't just a single room either, it 
    continues deeper through a doorway. Aside from that, there nothing 
    really special inside the armory. You can also exit the armory into a 
    dark room, a long hallway, and a torture room.
          """)
    while True:  
        options = ['further explore armory', 'explore long hallway', 'explore dark room', 'explore torture room']
        print('options:', options)
        userInput = input("What would you like to do?\n")
        while userInput not in options:
            print('I do not recgonize that command.')
            print('options:', options)
            userInput = input("What would you like to do?\n")
        if userInput == options[0]:
            armory2() 
        elif userInput == options[1]:    
            cell_room()  
        elif userInput == options[2]:
            darkroom()
        elif userInput == options[3]:
            torture_room()

def torture_room():
    print("""
    You enter the torture room. The walls are adorned with the many tools 
    of torment that the mind can think of. Scattered acrooss the room are 
    tables, all painted with the dried blood of those who suffered in this 
    place. Only God will know the horrors that ocurred in this room. Your 
    train of though is interrupted by the loud thumps of something trudging 
    nearby. It is immediately clear that whatever is causing those tremors 
    is something much larger than what any person can do. With each step 
    that it takes, all the tables and hanging tools shake as if an earthquake 
    had suddenly struck. You look towards the source of the sound. It lies 
    beyond a single doorway which seems to lead to a wide open area. 
          """)
    while True:  
        options = ['return to armory', 'follow source of sound']
        userInput = input("What would you like to do? [return to armory/follow source of sound]\n")
        while userInput not in options:
            print('I do not recgonize that command.')
            userInput = input("What would you like to do? [return to armory/follow source of sound]\n")
        if userInput == options[0]:
            armory()
        elif userInput == options[1]:
            options = ['continue', 'go back']
            userInput = input('You are now the final room. Once you pass you cannot go back to continue exploring. If you would like to continue onwards type "continue." If you changed your mind type "go back."\n')
            while userInput not in options:
                print('I do not recogonize that command.')
                userInput = input('You are now entering the final boss fight. Once you enter this fight, you can no longer go back to continue exploring. If you would like to continue onwards type "continue." If you changed your mind type "go back."\n')
            if userInput == options[0]:
                final_room()
            elif userInput == options[1]:
                print("""
                      You decide to continue exploring through the dungeons 
                      before following the source of the sound
                      """)

def armory2():
    global keys
    global greatsword
    if keys:
        if greatsword:
            print("""
    You enter deeper into the armory only to see the empty throne in 
    which the longsword used to liebefore you collected it. With nothing 
    else to do, you exit into the greater armory.
                  """)
            input('press <enter> to continue')
            armory()
        else: 
            print("""
    Deeper inside the armory lies a small room with nothing in it besides 
    a locked gate, which holds a weapon of great beauty. It a longsword, 
    crafted so delicately even in a room with no light one could see 
    it glimmer. 
    
    Recalling the key that you found in the key room, you shuffle through 
    your pocket until you are able to find your key. You insert the 
    key into the keyhole and are surprised to find that the gate 
    unlocks! You set your sword down and grab the greatsowrd carefully, 
    admiring how well it was crafted. This sword is now yours.
    
    You happily exit the room.
    """)
            greatsword = True
            ray_trace(sword, sword_color)
            input('press <enter> to continue')
            armory()         
    else:
        print("""
    Deeper inside the armory lies a small room with nothing in it besides 
    a locked gate, which holds a weapon of great beauty. It a longsword, 
    crafted so delicately even in a room with no light one could see 
    it glimmer. 
    
    You tug on the gate, hoping that it will break apart just like 
    everything else ou have seen so far. But even the gate itself was 
    made guard this sword for a long time. You eventually give up. and 
    leave the room.
              """)
        input('press <enter> to continue')
        armory()

def final_room():
    print("""
    As you step into the outside, you take a deep breath of fresh air. You
    look around to see what was the cause of the thundering sounds you heard 
    from within the dungeon but see nothing. However, you do see a silly 
    little horse tied up in its silly little stable. Feeling a little bit
    silly yourself, you go to the horse and mount it. Then you and your 
    silly little friend rode off into the sunset to have a silly little 
    time.
          """)
    input('press <enter> to continue')
    print("""
                                  THE END
          """)
    input('press <enter> to continue')
    print("""
    Did you enjoy that ending Jason? 
          """)
    input('press <enter> to continue')
    print("""
    I really did try to make a serious and like a dark/gory kind of game 
    but it took SOOOOO long to get the ray tracing thing to work. Crazy 
    thing is... it doesnt even look like I ray traced anything. Idk if you 
    looked at the rendered objects yet but they look like if I was trying to make an 
    8-bit game instead. Oh well...  See ya!
          """)
    input('press <enter> to exit the game')
    quit()



# INTRO SEQUENCE
print("""
    You wake up with a headache, confused, and wearing a bunch of armor
        
    "Where am I?" You ask yourself quietly
        
    You hear a weak voice from across the room
    
    "What is your name young man?" Asks an old knight. Though he is old, 
     he is not weak, even under his armour you can notice that he is in 
     good shape for his age. He is hurt,, bleeding from a slash through his 
     stomach. Even someone who has never seen war would be able to tell that 
     he does not have long to live. 
        """)
       
name = input("""
    "what is your name?" he asks again\n
        """)
        
print("""
    " """ + name+ """... Hah! That name suits you well soldier. I don't have 
    much time left, so I will tell you all that I know of this place. This 
    dungeon that we are in, its not normal. I have spent long enough in here
    to understand that all those who end up in here do not know how they got 
    here, however, there is a way out of this place. Some of those that I 
    have met before have seen it. I do not know the way there, that is up to 
    you to figure out. The exit is guarded by a creature thats not of 
    earthrealm, you must defeat it to escape.  You will have to be careful 
    on the way there, creatures unlike anything you have ever seen roam these
    dungeons, and you will have to fight them. Now go on, """+ name +""", 
    take my sword. It's not what it used to be, but it will get the job done.
    """)
     
input("Press <enter> to continue\n")

print("""
    You get up to leave the room, not before grabbing the sword that the 
    injured knight gave you. The sword was heavy, but balanced, and sturdy 
    enough so that you could attack an enemy and be confident in its ability
    to hurt it. But the sword was by no means in good condition, the years 
    have begun to wear on it and it has clearly lost some of the effectiveness
    that it used to have. Before leaving the room you look back at the knight,
    and he gives you a nod of approval. You go on.
      """)

input("Press <enter> to continue\n")


intro_hall()

