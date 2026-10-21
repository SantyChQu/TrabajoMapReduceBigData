from mre import Job

root_path = "./"
inputDirEstandar = root_path + "apuestas/input/estandar"

inputDirPremium = root_path + "apuestas/input/premium"

inputDirPlatinium = root_path + "apuestas/input/platinium"

outputDir = root_path + "apuestas/outputEjercicio4"

def fmap(key, value, context):

    equipoLocal = key

    context.write((int(equipoLocal)), "E")

def fmap2(key, value, context):

    equipoLocal = key

    context.write((int(equipoLocal)), "PR")

def fmap3(key, value, context):

    equipoLocal = key

    context.write((int(equipoLocal)), "PL")  

def fcombiner(key, values, context): #unicamente para ahorrarle trabajo al reduce, no se si vale la pena

    contPremium = 0
    contPlatinium = 0
    contEstandar = 0
    for v in values:

       if(v == "PR"):
            contPremium=contPremium+1
       elif (v == "PL"):
            contPlatinium=contPlatinium+1
       elif (v == "E"):
            contEstandar=contEstandar+1

    if (contPremium > 0):    
      context.write(key,("PR",contPremium))
    if (contPlatinium > 0):
      context.write(key,("PL",contPlatinium))
    if (contEstandar > 0):
      context.write(key,("E",contEstandar))


def fred(key, values, context):

    #creo que en definitiva no requiero de un combiner para este ejercicio ni en el 2),
    #ya que en si la cantidad total calculada no la uso para hacer una suma del total definitivo,
    #me serviria unicamente si realmente el combiner me permite ir mas rapido en tiempo, caso contrario lo debo de borrar: consultar
    contPremium = 0
    contPlatinium = 0
    contEstandar = 0

    for v in values:

       if(v== "PR"):
            contPremium=contPremium+1
       elif (v == "PL"):

            contPlatinium=contPlatinium+1
       elif (v  == "E"):
            contEstandar=contEstandar+1

       if(contPremium > 0 and contPlatinium > 0 and contEstandar > 0):
            break
         
    if (contPremium > 0 and contPlatinium == 0 and contEstandar == 0):
        context.write(key,"")

    if (contPremium == 0 and contPlatinium > 0 and contEstandar == 0):
        context.write(key,"")    

    if (contPremium == 0 and contPlatinium == 0 and contEstandar > 0):
        context.write(key,"")    


job = Job(inputDirEstandar, outputDir, fmap, fred)

job.addInputPath(inputDirPremium,fmap2)

job.addInputPath(inputDirPlatinium,fmap3)

success = job.waitForCompletion()