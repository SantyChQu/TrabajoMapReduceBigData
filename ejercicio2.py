from mre import Job

root_path = "./"
inputDirEstandar = root_path + "apuestas/input/estandar"

inputDirPremium = root_path + "apuestas/input/platinium"

outputDir = root_path + "apuestas/outputEjercicio2"

def fmap(key, value, context):
    valores = value.split()
    equipoLocal = key     #no lo uso realmente, lo puedo eliminar
    equipoVisitante = valores[0]
    cantVotosLocal = valores[1]
    cantVotosVisitante = valores[2]

    if int(cantVotosLocal) < int(cantVotosVisitante):
          context.write(int(equipoVisitante), "E")

def fmap2(key, value, context):
    valores = value.split()
    equipoLocal = key
    equipoVisitante = valores[0]
    cantVotosLocal = valores[1]
    cantVotosVisitante = valores[2]

    if int(cantVotosLocal) < int(cantVotosVisitante):
        context.write(int(equipoVisitante), "P")


def fcombiner(key, values, context):  #para reducir la cantidad de datos que se envian al reducer
                                      #no se si realmente se saca una ventaja para este caso

     totalE=0

     totalP=0

     for v in values:

          if v[0] == "E":
                totalE=totalE+1
          elif v[0] == "P":
                totalP=totalP+1 

     #pongo condicional para no enviar datos incorrectos al reducer
     #ejemplo puede ser que un equipo no tenga votos de un tipo y si del otro
     if (totalE > 0):            
       context.write(key, "E")
     if (totalP > 0):
       context.write(key, "P")


def fred(key, values, context):

    contEstandar = 0
    contPlatinium = 0
   

    for v in values:

       if(v == "E"):
            contEstandar=contEstandar+1

       elif (v == "P"):

            contPlatinium=contPlatinium+1

       if(contEstandar > 0 and contPlatinium >0): #para evitar procesar todos los valores dentro del for
            break     

    if contEstandar > 0 and contPlatinium > 0: #en  el caso de que salga del for sin haber entrado al if, hacemos esta consulta
                                               #para evitar incosistencia

                                             
         context.write(key,"")             

         


job = Job(inputDirEstandar, outputDir, fmap, fred)

job.addInputPath(inputDirPremium,fmap2)
         
success = job.waitForCompletion()

#revisado