# Calculate function that for given usb_size and
# memes = List(Tuple(str , int,  int))
#                    name, size, worth
# returns highest possible worth of an usb stick and names of memes in format:
# Tuple(int, Set(strings))
#       worth,   MemeName

def calculate(usb_size, memes):
# Declaring constants to easier read algorithm
    NAME = 0
    SIZE = 1
    WORTH = 2

    VALUE = 0
    NAMES = 1


    
    usb_size *= 1024 #GiB -> MiB

    
    # Preparing list in format List(List(int, Set(string*))*)
    # An inner list is created for every usb_size in <0, usb_size>
    # That list will contain Best Value for this size and
    # Set of meme names, that are needed to get this worth
    tab = [] 
    for i in range(usb_size+1):
        tab.append([0, set([])])

    # Calculating Value and adding Meme Names to set
    # for every size
    for meme in memes:
        for pos in range(usb_size,-1,-1):
            if (pos + meme[SIZE] <= usb_size and (tab[pos][VALUE] != 0 or pos == 0) and
                tab[pos + meme[SIZE]][VALUE] < tab[pos][VALUE] + meme[WORTH]):
                tab[pos + meme[SIZE]][VALUE] = tab[pos][VALUE] + meme[WORTH]
                tab[pos + meme[SIZE]][NAMES] = set([])
                for name in tab[pos][NAMES]:
                    tab[pos + meme[SIZE]][NAMES].add(name)
                tab[pos + meme[SIZE]][NAMES].add(meme[NAME])
    # Picking list with best Value
    best_answer = tab[0] 
    for answer in tab:
        if answer[VALUE] > best_answer[VALUE]:
            best_answer = answer
        # return Tuple(int, Set(string*))
    return (best_answer[VALUE], best_answer[NAMES]) 

def handtests():
    print(calculate(0, []))
    print(calculate( 0, [("Mickey Mouse", 0, 100), ("Mickey Donald", 1, 200)] ) )
    #What happens if worth is negative?
    print(calculate(0, [("Very Bad Meme :(", 0, -10), ("Good Meme :)", 0, 10)]))
#handtests()
