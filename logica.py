import os
import subprocess
from Objetos.MBR import MBR

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
    printInfo("Leyendo fdisk")
    if args.delete is not None and args.add is not None:
        raise Exception("Parametros delete y add no pueden estar en la misma linea")
    elif args.delete is not None:
        if(args.delete != "full"):
            raise Exception("Parametro delete debe llevar full")
        else:
            if(printWarning("Desea eliminar la partición?")):
                fdiskDelete(args)
            else:
                printInfo("Operación cancelada")

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
                if partition.name == args.name.decode().rstrip('\x00'):
                    mbr.partitions.remove(partition)
                    break
        except Exception as e:
            printError(e)