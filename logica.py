import os
import subprocess
from Objetos.MBR import MBR
from Objetos.Partition import Partition

from utilidades import calSize, printError, printInfo, printWarning, readObjDisplacement, writeObjDisplacement, writeSize


def mkdisk(args) -> None:
    sizeBytes = calSize(args.size, args.unit)

    folder_path = os.path.dirname(args.path)
    subprocess.run(f"mkdir -p {folder_path}", shell=True)
    try:
        archivo = open(args.path, "wb")
        writeSize(archivo, sizeBytes)
        newMBR = MBR()
        newMBR.setInfo(sizeBytes, args.fit)
        writeObjDisplacement(archivo, 0, newMBR)
        archivo.close()
    except Exception as e:
        printError(e)


def rmdisk(args) -> None:
    if printWarning("Desea eliminar el disco?"):
        try:
            os.remove(args.path)
        except Exception as e:
            printError(e)
    else:
        printInfo("Operación cancelada")


def fdisk(args) -> None:
    if args.delete is not None and args.add is not None:
        raise Exception(
            "Parametros delete y add no pueden estar en la misma linea")
    elif args.delete is not None:
        if (args.delete != "full"):
            raise Exception("Parametro delete debe llevar full")
        else:
            if (printWarning("Desea eliminar la partición?")):
                fdiskDelete(args)
            else:
                printInfo("Operación cancelada")
    elif args.add is not None:
        pass
    elif args.add is None and args.delete is None:
        if args.size is not None:
            fdiskNew(args)
        else:
            raise Exception("Parametro size es requerido al crear partición")


def fdiskNew(args) -> None:
    try:
        mbr = MBR()
        archivo = open(args.path, "rb+")
        archivo.seek(0)
        readObjDisplacement(archivo, 0, mbr)
        index = 0
        start = len(MBR().serialize())
        libre = mbr.size - start
        cantExt = 0
        cantTotal = 0
        for partition in mbr.partitions:
            if partition.size != -1:
                if (partition.name.decode().rstrip('\x00') == args.name):
                    archivo.close()
                    raise Exception("Ya existe una partición con ese nombre")
                start = partition.start + partition.size
                libre -= partition.size
                index += 1
            else:
                break
        sizeComplete = calSize(args.size, args.unit)
        if libre < sizeComplete:
            archivo.close()
            raise Exception("No hay espacio suficiente en el disco")
        else:
            for partition in mbr.partitions:
                if partition.size != -1:
                    cantTotal += 1
                    if partition.type.decode() == 'e':
                        cantExt += 1
            if cantTotal == 4:
                archivo.close()
                raise Exception("Ya se alcanzo el número máximo de particiones")
            elif cantExt == 1 and args.type == 'e':
                archivo.close()
                raise Exception("Ya se alcanzo el námero máximo de particiones extendidas")
            elif args.type == 'l' and cantExt == 0:
                raise Exception("No se puede crear una partición lógica sin una partición extendida")

            newPartition = Partition()
            newPartition.setInfo('1', args.type, args.fit,
                                 start, sizeComplete, args.name)
            mbr.partitions[index] = newPartition
            writeObjDisplacement(archivo, 0, mbr)
            archivo.close()

    except Exception as e:
        printError(e)
        return


def fdiskDelete(args) -> None:
    if not os.path.exists(args.path):
        printError("El disco no existe")
        return
    else:
        try:
            mbr = MBR()
            archivo = open(args.path, "rb+")
            archivo.seek(0)
            readObjDisplacement(archivo, 0, mbr)
            for partition in mbr.partitions:
                if partition.name.decode().rstrip('\x00') == args.name:
                    # mbr.partitions.remove(partition)
                    return
            archivo.close()
            raise Exception("No se encontro la partición")
        except Exception as e:
            printError(e)
