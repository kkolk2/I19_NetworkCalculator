
import convertions as conv
import networks as nets
import functions as f

v = input('Podaj adres IP: ')
try:
    print (nets.ToList(v))
    print (nets.ToDotDec(nets.ToList(v)))
    print (nets.IPv4AddressToDec(v))
    print (conv.DecToAny(nets.IPv4AddressToDec(v),2,32))
    
    addr_bin = nets.AddressToBin(v)	
except nets.InvalidOctetsNumber as invOctNum:
    #wydzielenie parametrów przekazanych wraz z wyjątkami
    msg, num = invOctNum.args
    print("Błąd! ", msg, ": ", num)
    
except nets.InvalidOctetValue as invOctVal:
    #wydzielenie parametrów przekazanych wraz z wyjątkami
    msg, nr, val = invOctVal.args
    #TODO: poprawić komunikat
    print("Błąd! ", msg +" nr "+ str(nr) + ":", val)
#gdy nie zostanie zgłoszony wyjątek
else:
    print()