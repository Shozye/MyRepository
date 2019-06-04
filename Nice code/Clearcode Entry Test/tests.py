from main import calculate
import itertools
# Main Example
# usb_size = 1
# memes = [
#   ('rollsafe.jpg', 205, 6),
#   ('sad_pepe_compilation.gif', 410, 10),
#   ('yodeling_kid.avi', 605, 12)
# ]
# expected : (22, {'sad_pepe_compilation.gif', 'yodeling_kid.avi'})
class Meme:
    __init__(self, name, size, worth):
        self.name = name
        self.size = size
        self.worth = worth
class Subset:
    __init__(self, memes): #memes is list of memes
        self.worth = 0
        self.size = 0
        self.names = {}
        for meme in memes:
            self.worth += meme.worth
            self.size += meme.size
            self.names.add(meme.name)
class Test:
    __init__(self, usb_size, memes, expected = []):
        self.usb_size = usb_size
        self.memes = []
        for meme in memes:
            self.memes.append( Meme(meme[0], meme[1], meme[2]) )
        self.expected = expected
        if self.expected == []:
            best_subset = Subset([self.memes[0]])
            for i in range(1, len(memes)+1):
                combinations = list(itertools.combinations(self.memes, i))
                for subset in combinations:
                    tmp = Subset(subset)
                    if (tmp.size < self.usb_size) && (tmp.worth > best_subset.worth):
                        best_subset = tmp
            self.expected.append(self.worth)
            self.expected.append(self.names)
            
        
tests = []


file = open("testlog.txt", "w+")
test_position = 1 
for test in tests:
    if (test.expected == calculate(test.size, test.memes)):
        file.write(f"Test {test_position} passed")
    else:
        file.write(f"Test {test_position} didn't pass   ===   FLAG   ===")
    test_position++
file.close()



