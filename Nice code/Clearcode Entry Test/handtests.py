from main import calculate

def handtests():
    print(calculate(0, []))
    print(calculate( 0, [("Mickey Mouse", 0, 100), ("Mickey Donald", 1, 200)] ) )
    #What happens if worth is negative?
    print(calculate(0, [("Very Bad Meme :(", 0, -10), ("Good Meme :)", 0, 10)]))

    # Now example test given in statement
    usb_size = 1
    memes = [
      ('rollsafe.jpg', 205, 6),
      ('sad_pepe_compilation.gif', 410, 10),
      ('yodeling_kid.avi', 605, 12)
    ]
    print(calculate(usb_size, memes))

    
handtests()
