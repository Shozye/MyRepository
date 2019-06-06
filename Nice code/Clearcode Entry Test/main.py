# Clearcode Work

def calculate(usb_size, memes):
    NAME = 0
    SIZE = 1
    WORTH = 2

    VALUE = 0
    NAMES = 1
    
    usb_size *= 1024 #GiB -> MiB
    tab = []
    for i in range(usb_size+1):
        tab.append([0, set([]) ])

    for meme in memes:
        for pos in range(usb_size,-1,-1):
            if (pos + meme[SIZE] <= usb_size and (tab[pos][VALUE] != 0 or pos == 0) and
                tab[pos + meme[SIZE]][VALUE] < tab[pos][VALUE] + meme[WORTH]):
                tab[pos + meme[SIZE]][VALUE] = tab[pos][VALUE] + meme[WORTH]
                tab[pos + meme[SIZE]][NAMES] = set([])
                for name in tab[pos][NAMES]:
                    tab[pos + meme[SIZE]][NAMES].add(name)
                tab[pos + meme[SIZE]][NAMES].add(meme[NAME])
    best_answer = tab[0]
    pos = 0
    best_pos = 0
    for answer in tab:
        if answer[VALUE] > best_answer[VALUE]:
            best_answer = answer
            best_pos = pos
        pos += 1

    print(best_pos, usb_size)
    return (best_answer[VALUE], best_answer[NAMES])    
    pass

