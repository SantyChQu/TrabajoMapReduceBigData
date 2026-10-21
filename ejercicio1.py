from mre import Job

root_path = "./"
inputDirEstandar = root_path + "apuestas/input/estandar"

inputDirPremium = root_path + "apuestas/input/premium"

outputDir = root_path + "apuestas/outputEjercicio1"

def fmap(key, value, context):
    valores = value.split()
    equipoLocal = key
    equipoVisitante = valores[0]
    cantVotosLocal = valores[1]
    cantVotosVisitante = valores[2]

    if int(cantVotosLocal) > int(cantVotosVisitante):
          context.write(int(equipoLocal), 1)

    elif int(cantVotosLocal) < int(cantVotosVisitante):
          context.write(int(equipoVisitante), 1)

def fmap2(key, value, context):
    valores = value.split()
    equipoLocal = key
    equipoVisitante = valores[0]
    cantVotosLocal = valores[1]
    cantVotosVisitante = valores[2]

    if int(cantVotosLocal) > int(cantVotosVisitante):
          context.write(int(equipoLocal), cantVotosLocal)

    elif int(cantVotosLocal) < int(cantVotosVisitante):
          context.write(int(equipoVisitante), cantVotosVisitante)

def fcombiner(key, values, context):
    total = 0
    for v in values:
      total += int(v)
    context.write(key, total)


def fred(key, values, context):
    total = 0
    for v in values:
        total += int(v)
    if(total > context["parametroApuesta"]):    
      context.write(key, total)


job = Job(inputDirEstandar, outputDir, fmap, fred)
x=5000
job.setCombiner(fcombiner)
job.addInputPath(inputDirPremium,fmap2)
job.setParams({"parametroApuesta": x})
success = job.waitForCompletion()
#revisado