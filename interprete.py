import argparse
import re
import shlex
from logica import fdisk, mkdisk, rmdisk
from utilidades import printError, printInfo, printWarning


def Commnads(input_command) -> None:

    input_command = re.sub(r"[#][^\n]*", "", input_command)
    if input_command == "":
        return None
    elif input_command == "exit":
        exit()

    commandType(input_command)


def commandType(input_command) -> None:
    try:
        input_command = input_command.lower()
        args = shlex.split(input_command)
        command = args.pop(0)
        if command == "mkdisk":
            comMkdisk(args)
        elif command == "rmdisk":
            comRmdisk(args)
        elif command == "fdisk":
            comFdisk(args)
    except Exception as e:
        printError(e)
        return None


def comMkdisk(args) -> None:
    printInfo("Leyendo mkdisk")
    try:
        parser = argparse.ArgumentParser(description="mkdisk")
        parser.add_argument("-size", required=True, type=int)
        parser.add_argument("-path", required=True)
        parser.add_argument("-fit", default='f')
        parser.add_argument("-unit", default='m')
        args = parser.parse_args(args)

        args.fit = args.fit[:1]

        if args.fit not in ['f', 'w', 'b']:
            raise Exception("Error en el parametro fit")
        if args.unit not in ['m', 'k']:
            raise Exception("Error en el parametro unit")
        if re.search("[.][d|D][s|S][k|K]", args.path) is None:
            raise Exception("La extensión del archivo debe ser .dsk")

        mkdisk(args)

    except SystemExit:
        printError("Argumentos de mkdisk")
        return None
    except Exception as e:
        printError(e)
        return None

def comRmdisk(args) -> None:
    printInfo("Leyendo rmdisk")
    try:
        parser = argparse.ArgumentParser(description="rmdisk")
        parser.add_argument("-path", required=True)
        args = parser.parse_args(args)

        if re.search("[.][d|D][s|S][k|K]", args.path) is None:
            raise Exception("La extensión del archivo debe ser .dsk")
        rmdisk(args)
    except SystemExit:
        printError("Argumentos de rmdisk")
        return None
    except Exception as e:
        printError(e)
        return None
    
def comFdisk(args) -> None:
    printInfo("Leyendo fdisk")
    try:
        parser = argparse.ArgumentParser(description="fdisk")
        parser.add_argument("-size", type=int)
        parser.add_argument("-path", required=True)
        parser.add_argument("-name", required=True)
        parser.add_argument("-unit", default='k')
        parser.add_argument("-type", default='p')
        parser.add_argument("-fit", default='w')
        parser.add_argument("-delete")
        parser.add_argument("-add")
        args = parser.parse_args(args)

        args.fit = args.fit[:1]

        if re.search("[.][d|D][s|S][k|K]", args.path) is None:
            raise Exception("La extensión del archivo debe ser .dsk")
        
        fdisk(args)

    except SystemExit:
        printError("Argumentos de fdisk")
        return None
    except Exception as e:
        printError(e)
        return None