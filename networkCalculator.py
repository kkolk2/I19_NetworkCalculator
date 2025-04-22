
import conversions as conv
import networks as nets
import functions as f


address = input('Podaj adres IPv4: ')
netmask = input ('Podaj maskę podsieci: ')

#addressPrefix = "192.168.10.10 / 18"
subnets = []
try:    
    #nets.ValidateIPv4Address(address)
    #nets.ValidateIPv4Netmask(netmask)

    #d = nets.ParseIPv4Address(addressPrefix)
    subnetsCount = int(input ('Podaj ilość podsieci: '))
    
    subnets = nets.IPv4Subnetting(address,netmask,subnetsCount)

   
except nets.InvalidOctetsNumber as invOctNum:
    #wydzielenie parametrów przekazanych wraz z wyjątkami
    msg, num = invOctNum.args
    print("Błąd! ", msg, ": ", num)
    
except nets.InvalidOctetValue as invOctVal:
    #wydzielenie parametrów przekazanych wraz z wyjątkami
    msg, nr, val = invOctVal.args
    #TODO: poprawić komunikat
    print("Błąd! ", msg +" nr "+ str(nr) + ":", val)
except nets.NetmaskDiscontinuous as netmaskDiscontinuous:
    print("Błąd!", netmaskDiscontinuous.args[0], netmaskDiscontinuous.args[1])
#gdy nie zostanie zgłoszony wyjątek
else:
    print(nets.NetworkInfo(address,netmask))
    for i in range(len(subnets)):
        print(f"Network {i + 1}:")
        for name, param in subnets[i].items():
            print(f"\t{name}: {param}")
        print("-------------------------")
finally:
    #print (subnets)
    pass

    
        
