class Genotype:
    def __init__(self, code):
        self.codeL = code
        self.codeR = code[::-1]
        self.lenght = len(code)
        self.genesL = []
        self.genesR = []
        self.coding_partL = ""
        self.coding_partR = ""
        gene_started = False
        gene_start = 0
        for i in range(self.lenght-1):
            if self.codeL[i] == "A" and self.codeL[i+1] == "A" and not gene_started:
                gene_start = i
                gene_started = True
            elif self.codeL[i] == "B" and self.codeL[i+1] == "B" and gene_started:
                gene_started = False
                self.genesL.append(self.codeL[gene_start:i+2])
        self.coding_partL = "".join(self.genesL)
        gene_started = False
        gene_start = 0
        for i in range(self.lenght-1):
            if self.codeR[i] == "A" and self.codeR[i+1] == "A" and not gene_started:
                gene_start = i
                gene_started = True
            elif self.codeR[i] == "B" and self.codeR[i+1] == "B" and gene_started:
                gene_started = False
                self.genesR.append(self.codeR[gene_start:i+2])
        self.coding_partR = "".join(self.genesR)


    def hasMutation(self):
        for gene in self.genesL:
            if "BCDDC" in gene:
                return True
        return False

    def MaxLenOfGen(self):
        longest = 0
        for gene in self.genesL:
            if len(gene) > longest:
                longest = len(gene)
        return longest

    def is_resistant(self):
        if self.coding_partL == self.coding_partR:
            return True
        else:
            return False
    def is_highly_resistant(self):
        if self.codeL == self.codeR:
            return True
        else:
            return False
class Solution:
    def __init__(self, filename):
        self.filename = filename
        self.genotypes = []
        file = open(self.filename, "r")
        data = file.readlines()
        for row in data:
            if row.endswith("\n"):
                self.genotypes.append(Genotype(row[:len(row)-1]))
            else:
                self.genotypes.append(Genotype(row))
        file.close()
        self.amount_of_different = 0
        self.highest_population_species = 0
        self.amount_of_mutations = 0
        self.biggest_amount_of_genes = 0
        self.longest_gene = 0
        self.amount_of_resistant = 0
        self.amount_of_highly_resistant = 0
        self.answer=""

    def ex1(self):
        amount_tab = []
        for i in range(500):
            amount_tab.append(0)
        for genotype in self.genotypes:
            amount_tab[genotype.lenght-1]+=1
        for i in amount_tab:
            if i>0:
                self.amount_of_different+=1
        self.highest_population_species = max(amount_tab)

    def ex2(self):
        for genotype in self.genotypes:
            if genotype.hasMutation():
                self.amount_of_mutations+=1
    def ex3(self):
        for genotype in self.genotypes:
            if len(genotype.genesL) > self.biggest_amount_of_genes:
                self.biggest_amount_of_genes = len(genotype.genesL)
            if genotype.MaxLenOfGen() > self.longest_gene:
                self.longest_gene = genotype.MaxLenOfGen()
    def ex4(self):
        for genotype in self.genotypes:
            if genotype.is_resistant():
                self.amount_of_resistant+=1
            if genotype.is_highly_resistant():
                self.amount_of_highly_resistant+=1
        
    def give_answer(self):
        self.ex1()
        self.ex2()
        self.ex3()
        self.ex4()
        self.answer = f"Ad1. {self.amount_of_different} {self.highest_population_species} \n Ad2. {self.amount_of_mutations} \n Ad3. {self.biggest_amount_of_genes} {self.longest_gene} \n Ad4. {self.amount_of_resistant} {self.amount_of_highly_resistant}"

        writer = open("wyniki.txt", "w+")        
        writer.write(self.answer)
        writer.close()

Main = Solution("dane_geny.txt")
Main.give_answer()


