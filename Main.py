import numpy as np
import operator
import pandas as pd
import random
from matplotlib import pyplot as plt
from City import City
from Fitness import Fitness


#Gera um camminho (sequencia de cidades a seguir) aleatório
def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route


#Gerar x caminhos iniciais (População inicial)
def initialPopulation(popSize, cityList):
    population = []
    print(f"Gerando %s rotas iniciais" %popSize)
    for i in range(0, popSize):
        population.append(createRoute(cityList))
    print("Rotas iniciais geradas")
    return population

#Ranquear rotas
def rankRoutes(population):
    print("Ranqueando rotas")
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

#Indice das melhores rotas
def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100 * random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

#Pool de melhores rotas
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, int(len(selectionResults))):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool


#Gerar filhos
def breed(parent1, parent2):
    children = []
    for i in range(0,2):
        child = []
        childP1 = []
        childP2 = []

        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(startGene, endGene):
            childP1.append(parent1[i])

        childP2 = [item for item in parent2 if item not in childP1]

        child = childP1 + childP2
        children.append(child)
    return children

#Gerar nova população
def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    print("Aplicando elitismo")
    #Aplicar elitismo
    for i in range(0, eliteSize):
        children.append(matingpool[i])
    print(f"%s individuos selecionados para persistir" %eliteSize)

    print("Gerando filhos")
    #Gerar filhos
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child[0])
        children.append(child[1])
    print("Novos filhos gerados")
    return children


#Mutar individuo
def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        #
        if (random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swapWith]

            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


#Mutar populução
def mutatePopulation(population, mutationRate):
    print(f"Mutando %s%% da população" %mutationRate )
    mutatedPop = []

    for ind in range(0, len(population)):
        #mutar individuo
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

#Gerar nova geração
def nextGeneration(currentGen, eliteSize, mutationRate):
    print("Gerando nova geração")
    #Selecionar 50 melhores ranqueados
    popRanked = rankRoutes(currentGen)[0:50]
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    print("50 melhores individuos (Rotas) selecionadas")

    #Gerar filhos da população anterior
    children = breedPopulation(matingpool, eliteSize)

    #Gerar nova geração
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration


def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
    print("INICIANDO ALGORITIMO GENÉTICO PARA DETERMINAR MENOR ROTA PASSANDO POR TODAS AS CIDADES E RETORNANDO À CIDADE INICIAL")
    print()
    print("Cidades selecionadas: ")
    print("\t", end="")
    for i in range(0, len(population)):
        print(population[i].name, end=", ")
    print()

    #Gerar população inicial (rotas)
    pop = initialPopulation(popSize, population)
    for route in pop:
        print(route)
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])


    currentDistance = 0
    countToBreak = 0

    #Percorreger gerações
    for i in range(0, generations):
        print("\t GERAÇÃO #%s" %i)
        if i == 0:
            pass
        else:
            print("Verificando se houve alteração no melhor caminho")
        #Verificar se houve alteração no resultado
        if currentDistance != progress[-1]:
            currentDistance = progress[-1]
            countToBreak = 0
            print("Novo melhor caminho encontrado")
        else:
            print(f"Não houve melhoras no resultado há %s geração(ões)" %countToBreak )
            # Incrementa quando não há alteração do resultado
            countToBreak += 1
        #Criar nova geração
        pop = nextGeneration(pop, eliteSize, mutationRate)

        #Adicionar melhor resultado encontrado na geração à lista
        rankedRoutes = rankRoutes(pop)
        progress.append(1 / rankedRoutes[0][1])



        #Se o resultado se mantiver constante por 10 iterações, parar de gerar novas gerações
        if countToBreak == 10:
            print("Limite de 10 gerações com mesmo resultado alcançado.")
            print("Encerrando processamento")
            print()
            print("Melhor rota encontrada:")
            print("\t", end="")
            print(pop[0])
            print("Menor distância:")
            print("\t", end="")
            print(str(progress[-1]) + "KM")
            break

    #Gerar gráfico
    plt.plot(progress)
    plt.ylabel('Distance (KM)')
    plt.xlabel('Generation')
    plt.show()

# Seleção de cidades com coordenadas reais
cityList = []

cityList.append(City("São bento do una", -8.51825331291702, -36.459560389017874))  #São bento do una
cityList.append(City("Belo Jardim", -8.329911388442437, -36.41037469340696))   #Belo Jardim
cityList.append(City("Pesqueira", -8.355028928564858, -36.68168933693814))   #Pesqueira
cityList.append(City("São josé", -8.464899091221097, -36.78323399884455))   #São josé
cityList.append(City("Venturosa", -8.577875694823003, -36.859392495274356))  #Venturosa
cityList.append(City("Capoeiras", -8.737868277249483, -36.60711747585063))  #Capoeiras
cityList.append(City("Garanhuns", -8.891869402244335, -36.48548478266028))   #Garanhuns
cityList.append(City("Lajedo", -8.655207219573613, -36.31443880786136))   #Lajedo
cityList.append(City("Caruaru", -8.271725918653804, -35.989451455743406)) #Caruaru
cityList.append(City("Agrestina", -8.454115125349727, -35.93053561997933))   #Agrestina
cityList.append(City("União dos Palmares", -9.152453449605217, -36.02609682433778))   #União dos Palmares
cityList.append(City("Catende", -8.664601439153888, -35.71577789606512))   #Catende
cityList.append(City("Canhotinho", -8.88060320904562, -36.18900509300881))   #Canhotinho
cityList.append(City("Bom Conselho", -9.1771628800083, -36.673635354939094))    #Bom Conselho
cityList.append(City("Águas Belas", -9.107737294857102, -37.1145538677541))    #Águas Belas

geneticAlgorithmPlot(population=cityList, popSize=100, eliteSize=10, mutationRate=0.01, generations=100)

