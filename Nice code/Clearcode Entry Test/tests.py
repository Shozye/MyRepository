from main import calculate
from itertools import combinations
import random
class Meme:
    def __init__(self, tuple):
        self.name = tuple[0]
        self.size = tuple[1]
        self.worth = tuple[2]
class Subset:
    def __init__(self, memesList):
        self.worth = 0
        self.size = 0
        self.names = set([])
        for meme in memesList:
            self.worth += meme.worth
            self.size += meme.size
            self.names.add(meme.name)
        self.answer = (self.worth, self.names)
class Test:
    def __init__(self, usb_size, memes, expected = None):
        self.usb_size = usb_size*1024 # GiB => MiB
        self.rawMemes = memes
        self.memes = []
        for memeTuple in memes:
            self.memes.append( Meme(memeTuple) )
        self.expected = expected
        if self.expected == None:
            best_subset = Subset([Meme(("TestMeme",0,0))])
            for amount_of_elements in range(1, len(memes)+1):
                subsetList = [Subset(j) for j in combinations(self.memes, amount_of_elements)]
                for subset in subsetList:
                    if (subset.size < self.usb_size) and (subset.worth > best_subset.worth):
                        best_subset = subset
            self.expected = best_subset.answer
        if self.expected == calculate(usb_size, memes):
            self.passed = True
        else:
            self.passed = False

class TestGenerator:
    def __init__(self, amountMemesCAP):
        self.amountMemesCap = amountMemesCAP
        self.memeNames = [ #33 names
            "sad_pepe.png", "sad_frog.jpg", "metamorphosis.png",
            "footballMessi.png", "AmericaOil.jpg", "Mao.png",
            "Hitler.jpg", "Stalin.png", "JanKazimierz.png",
            "PolandIntoSpace.jpg", "Nazi.png", "JanuszMalpa.png",
            "skocznia.png", "pride.jpg", "AsterixObelix.png",
            "NaWalbrzych.avi", "LewNieSprzymierzaSieZKojotem.avi",
            "PoczujWSobieSileLwa.png", "DziwniCiRzymianie.png",
            "FranceWar.png", "Chernobyl.jpg", "RickMorty.png",
            "Dog.png", "Cat.jpg", "hanuszka.png", "Spongebob.png",
            "Urban.png", "WaznaWiadomosc.avi", "Tesla.png",
            "Mussolini.jpg", "Smolensk.png", "AndrzejDuda.png",
        ]
    def generate(self):
        tmp_names = []
        for name in self.memeNames:
            tmp_names.append(name)
        usb_size = random.randint(1,10)
        amount_of_memes = random.randint(1,self.amountMemesCap)
        memesList = []
        for i in range(amount_of_memes):
            randName = tmp_names[random.randint(0,len(tmp_names)-1)]
            tmp_names.remove(randName)
            memesList.append(
                (randName,
                 random.randint(1,2000),
                 random.randint(1,20))
            )
        return Test(usb_size, memesList)
tests = []
Generator = TestGenerator(10)
for i in range(1000):
    tests.append(Generator.generate())



file = open("testlog.txt", "w+")
test_position = 0
for test in tests:
    if (test.expected == calculate(test.usb_size, test.memes)):
        file.write(f"Test {test_position} passed\n")
    else:
        file.write(f"Test {test_position} didn't pass   ===   FLAG   ===\n")
        file.write(f"{[test.usb_size, test.rawMemes]}\n")
    
    test_position+=1
file.close()



