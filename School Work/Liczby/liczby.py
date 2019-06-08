def factorial(number):
    if number == 0:
        return 1
    else:
        answer = 1
        
        for i in range(1,number+1):
            answer *= i
    return answer
            
def GDC(a, b):
    if a == 0 : 
        return b  
      
    return GDC(b%a, a) 
    
class Number:
    def __init__(self, number):
        self.number = int(number)
    def isPowOf3(self):
        num = self.number
        while(num != 1):
            if num < 1:
                return False
            if num%3 != 0:
                return False
            num/=3
        return True
    
    def isEqualToSumOfDigitFactorials(self):
        sum = 0
        num = self.number
        while(num!=0):
            sum += factorial(num%10)
            num //= 10
        if sum == self.number:
            return True
        return False
class Solution:
    def __init__(self, inputFilename, outputFilename):
        self.inputFile = open(inputFilename, "r+")
        self.outputFile = open(outputFilename, "w+")
        self.numbers = []
        for i in range(500):
            self.numbers.append(Number(self.inputFile.readline()))
        self.inputFile.close()
        self.best_start = None
        self.best_length = None
        self.best_divider = None
        self.how_many_pows_of_3 = None
        self.ex2_nums = None
    def ex1(self):
        counter = 0
        for num in self.numbers:
            if num.isPowOf3():
                counter+=1
        self.how_many_pows_of_3 = counter

                
    def ex2(self):
        list = []
        for num in self.numbers:
            if num.isEqualToSumOfDigitFactorials():
                list.append(num)
        self.ex2_nums = list
                
    def ex3(self):
        best_start = self.numbers[0].number
        best_length = 1
        best_divider = 1
        for pos in range(len(self.numbers)):
            length = 0
            gdc_of_nums = self.numbers[pos].number
            for pos2 in range(pos, len(self.numbers)-1):
                divider = GDC(gdc_of_nums, self.numbers[pos2+1].number)
                print(divider)
                if divider > 1 and pos2!=len(self.numbers)-1:
                    length += 1
                    divider = gdc_of_nums
                    if best_length < length:
                        best_length = length
                        best_divider = divider
                        best_start = self.numbers[pos].number
                else:
                    if best_length < length:
                        best_length = length
                        best_divider = gdc_of_nums
                        best_start = self.numbers[pos].number
                        break
        self.best_start = best_start
        self.best_length = best_length
        self.best_divider = best_divider
    def giveanswer(self):
        self.ex1()
        self.ex2()
        self.ex3()
        self.outputFile.write(f"Zad 1. Poteg trojki jest {self.how_many_pows_of_3}\n")
        self.outputFile.write("Zad 2. \n")
        for num in self.ex2_nums:
            self.outputFile.write(str(num.number) + "\n")
        self.outputFile.write("Zad 3. \n")
        self.outputFile.write(f"Najlepsza pozycja startowa {self.best_start} \n Najwieksza Dlugosc Ciagu {self.best_length} \n I NWD tego ciagu {self.best_divider}")
        self.outputFile.close()    
Main = Solution("liczby.txt", "wyniki.txt")
Main.giveanswer()




    
