from main import calculate

def handtests():
    tests = [
        calculate(0, []),
        calculate( 0, [("Mickey Mouse", 0, 100), ("Mickey Donald", 1, 200)] ),
        calculate(0, [("Very Bad Meme :(", 0, -10), ("Good Meme :)", 0, 10)]),
        calculate(1, [('rollsafe.jpg', 205, 6),('sad_pepe_compilation.gif', 410, 10),('yodeling_kid.avi', 605, 12)] )
        ]
    solutions = [
        (0, set([])),
        (100, set(["Mickey Mouse"])),
        (10, set(["Good Meme :)"])),
        (22, set(["sad_pepe_compilation.gif", "yodeling_kid.avi"]))
    ]
    passed = 0
    not_passed = 0
    for TestNum in range(len(tests)):
        if tests[0] == solutions[0]:
            print(f"Test {TestNum + 1} passed")
            passed += 1
        else:
            print(f"Test {TestNum + 1} not passed")
            not_passed += 1
    print(f"Tests passed : {passed} \nTests not passed: {not_passed}")
handtests()
