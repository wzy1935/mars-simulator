from fengyong import Assembler
from fengyong import DisAssembler

def getCode(str) :
    code = restructCode(str)
    return hex(int(Assembler.encode(code).bin,2))

def restructCode(str) :
    str = str.replace("\t"," ")
    arr = str.split()
    if (len(arr) == 0) : return ""
    code = str
    if (arr[0] == "led") : code = "sw "+ arr[1] + ", -13119("+ arr[1] +")"
    if (arr[0] == "seg"): code = "sw " + arr[1] + ", -13118(" + arr[1] + ")"
    if (arr[0] == "print"): code = "sw " + arr[1] + ", -13117(" + arr[1] + ")"
    if (arr[0] == "scan"): code = "lw " + arr[1] + ", -13120(" + arr[1] + ")"
    return code

def getCodes(strs) :
    arr = strs.split('\n')
    output = ""
    for i in range(0, len(arr)) :
        o = restructCode(arr[i])
        arr[i] = o
        #print(getCode(o))
        output += ("\n" + arr[i])

    return output

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def things_to_send(str) :
    return bitstring_to_bytes("00000011000000100000000000000000" +
                              Assembler.encode(getCodes(str) + "\n beq $t3,$t3,-1").bin
                              + "00000000000000000000000000000000"
                              )

if __name__ == '__main__':

    print(DisAssembler.decode(int("20a50001",16)))