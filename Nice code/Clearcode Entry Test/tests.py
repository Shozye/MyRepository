from main import calculate
from itertools import combinations
import time
import random

# CONFIGURATION
AMOUNT_OF_TESTS = 500
MAX_MEME_AMOUNT = 23
MIN_USB_SIZE = 0
MAX_USB_SIZE = 20 #in GiB
MIN_USB_SIZE = 0
MAX_MEME_SIZE = 5000 # in MiB
MIN_USB_WORTH = -5
MAX_MEME_WORTH = 60
# CONFIGURATION END

class Meme:
    def __init__(self, tuple):  #insert tuple([str, int, int]) representing meme
        self.name = tuple[0]
        self.size = tuple[1]
        self.worth = tuple[2]
        
class Subset:
    def __init__(self, memesList): #insert List of Meme objects
        self.worth = 0
        self.size = 0
        self.names = set([])
        for meme in memesList:
            self.worth += meme.worth
            self.size += meme.size
            self.names.add(meme.name)
        self.answer = (self.worth, self.names) # answer in an expected format
class Test:
    def __init__(self, usb_size_GiB, memes): #memes is a raw List of Tuples
        self.usb_size = usb_size_GiB*1024 # GiB => MiB
        self.usb_size_GiB = usb_size_GiB
        self.rawMemes = memes 
        self.memes = []
        for memeTuple in memes:
            self.memes.append( Meme(memeTuple) )
            
        start_time = time.time()
        #Testing by taking easier algorithm, which is easier to understand but slower
        #Algorithm with 2**n complexity

        best_subset = Subset([Meme(("TestMeme",0,0))])
        for amount_of_elements in range(1, len(memes)+1):
            subsetList = [Subset(j) for j in combinations(self.memes, amount_of_elements)]
            #takes EVERY subset of self.memes and checks it's worth.
            for subset in subsetList:
                if (subset.size <= self.usb_size) and (subset.worth > best_subset.worth):
                    best_subset = subset
        #return subset with highest worth
        self.expected = best_subset.answer
        # elapsed time of 2**n algorithm
        self.expected_elapsed_time = round(time.time() - start_time,2)
class TestGenerator:
    def __init__(self, amountMemesCAP):
        self.amountMemesCap = amountMemesCAP
        self.memeNames = [ #35 names
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
            "HiszpanskaInkwizycja.png", "It's Over 9000.jpeg", "Nosacz.png",
        ]
    def generate(self):
        tmp_names = []
        #tmp list to remove used names
        for name in self.memeNames:
            tmp_names.append(name)
        usb_size = random.randint(MIN_USB_SIZE,MAX_USB_SIZE) # in GiB, with 0<usb_size constraint
        #assuming that 0<amount_of_memes
        amount_of_memes = random.randint(1,self.amountMemesCap)

        memesList = []
        for i in range(amount_of_memes):
            #randomize name and delete it from list
            randName = tmp_names[random.randint(0,len(tmp_names)-1)]
            tmp_names.remove(randName)
            
            memesList.append(
                (randName,
                 random.randint(MIN_USB_SIZE,MAX_MEME_SIZE),
                 random.randint(MIN_USB_WORTH,MAX_MEME_WORTH))
            )
        return Test(usb_size, memesList)
    
tests = []
Generator = TestGenerator(MAX_MEME_AMOUNT)

for i in range(AMOUNT_OF_TESTS):
    
    # Elapsed time of generating test
    start_test_creating_time = time.time()
    tests.append(Generator.generate())
    end_test_creating_time = round(time.time() - start_test_creating_time,2)
    
    print(f"Test Generated in {end_test_creating_time}, amount of memes = {len(tests[-1].memes)}")

# Saving All Informations in two files
# In test_passed_file, only information if testpassed
# in test_log informations about every test
test_passed_file = open("testpassed.txt", "w+")
test_log = open("testlog.txt", "w+")
test_position = 0
for test in tests:
    start_time = time.time()
    algorithm_answer = calculate(test.usb_size_GiB, test.rawMemes)
    calculate_elapsed_time = round(time.time() - start_time,2)

    if algorithm_answer == test.expected:
        test_passed_file.write(f" Test {test_position} passed \n")
    elif algorithm_answer[0] == test.expected[0]:
        test_passed_file.write(f" Test {test_position} passed Same USB Stick Value: {test.expected[0]}, but not same names\n")
    else:
        test_passed_file.write(f" Test {test_position} not passed ======== FLAG ========= \n")


    test_log.write(f" === Test {test_position} Amount of memes {len(test.memes)} === : \n")
    test_log.write(f" usb_size = {test.usb_size_GiB} memes = {test.rawMemes} \n")
    test_log.write(f" Expected: {test.expected} \n")
    test_log.write(f" Got: {algorithm_answer} \n")
    test_log.write(f" 2**n time execution: {test.expected_elapsed_time}, n**2 time execution {calculate_elapsed_time} \n")
    test_position += 1
    
    
test_passed_file.close()
test_log.close()



