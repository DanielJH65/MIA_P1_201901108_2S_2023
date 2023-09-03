def printError(output) -> None:
    print("\033[31mError: " + str(output) + "\033[0m")


def printInfo(output) -> None:
    print("\033[36mInfo: " + str(output) + "\033[0m")


def printSuccess(output) -> None:
    print("\033[32mCompleto: " + str(output) + "\033[0m")


def printWarning(output) -> bool:
    while True:
        confirm = input("\033[33mPrecaución: " +
                        str(output) + "(s/n) \033[0m » ")
        if confirm == "s":
            return True
        elif confirm == "n":
            return False


def calSize(size, unit) -> int:
    if unit == "k":
        return size * 1024
    elif unit == "m":
        return size * 1024 * 1024
    elif unit == "b":
        return size
    else:
        return 0


def writeSize(file, size) -> None:
    for i in range(0, size):
        file.write(b'\0')


def writeObjDisplacement(file, displacement, obj) -> None:
    data = obj.serialize()
    file.seek(displacement)
    file.write(data)


def readObjDisplacement(file, displacement, obj) -> None:
    try:
        file.seek(displacement)
        data = file.read(obj.size)
        obj.deserialize(data)
    except Exception as e:
        printError(e)


def encodeStr(string, size) -> bytes:
    return string.encode("utf-8")[:size].ljust(size, b'\0')
