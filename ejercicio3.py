from mre import Job

root_path = "./"
inputDirEstandar = root_path + "apuestas/input/platinium"

inputDirPremium = root_path + "apuestas/input/premium"

outputDir = root_path + "apuestas/outputEjercicio3"

def fmap(key, value, context):
    valores = value.split()
    equipoLocal = key
    equipoVisitante = valores[0] #no lo uso realmente, lo puedo eliminar
    cantVotosLocal = valores[1]
    cantVotosVisitante = valores[2]

    if  int(cantVotosLocal) > (int(cantVotosVisitante) * context["parametroApuesta"]):
          context.write(int(equipoLocal),  "PL")

def fmap2(key, value, context):
    valores = value.split()
    equipoLocal = key
    equipoVisitante = valores[0]
    cantVotosLocal = valores[1]
    cantVotosVisitante = valores[2]

    if int(cantVotosLocal) > (int(cantVotosVisitante) * context["parametroApuesta"]):
        context.write(int(equipoLocal), "PR")   

def fcombiner(key, values, context): #uso combiner para reducir la cantidad de datos que se envian al reducer unicamente
    contPremium = 0
    contPlatinium = 0

    for v in values:

       if(v == "PR"):
            contPremium=contPremium+1
       elif (v == "PL"):

            contPlatinium=contPlatinium+1

    if (contPremium > 0):   
      context.write(key, "PR")
    if (contPlatinium > 0):
      context.write(key, "PL")

def fred(key, values, context):

    contPremium = 0
    contPlatinium = 0

    for v in values:

       if(v == "PR"):
            contPremium=contPremium+1
       elif (v == "PL"):

            contPlatinium=contPlatinium+1

       if(contPremium >0): #para evitar procesar todos los valores dentro del for
            break     
       
    if (contPremium == 0 and contPlatinium >0):
        
         context.write(key,"")             

         


job = Job(inputDirEstandar, outputDir, fmap, fred)

job.addInputPath(inputDirPremium,fmap2)
job.setCombiner(fcombiner)
x=2
job.setParams({"parametroApuesta": x})
success = job.waitForCompletion()

#revisado