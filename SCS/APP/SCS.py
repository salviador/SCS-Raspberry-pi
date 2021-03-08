from abc import ABC, abstractmethod
from enum import Enum
from struct import *
import asyncio
from asyncserial import Serial
import time
import Timerelapsed
 

#BYTES MANIPULATION
def bitwise_and_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") & int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

def bitwise_or_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") | int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

def bitwise_xor_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") ^ int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

def bitwise_shiftleft_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") << int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")


class TYPE_INTERfACCIA(Enum):
    on_off = "on_off"
    dimmer = "dimmer"
    serrande_tapparelle = "serrande_tapparelle"
    gruppi = "gruppi"
    sensori_temperatura = "sensori_temperatura"
    termostati = "termostati"
    serrature = "serrature"
    campanello_porta = "campanello_porta"
    

class SCSDevice(ABC):
    def __init__(self):
        self.buffer = bytearray([])
        super().__init__()
        self._mnomeDevice = ""

    def Set_Nome_Attuatore(self, mnome ):
        self._mnomeDevice = mnome
    def Get_Nome_Attuatore(self ):
        return self._mnomeDevice
 

    #@abstractmethod
    def Set_Type(self, TYPE_INTERfACCIAt ):
        self._type = TYPE_INTERfACCIAt
    #@abstractmethod
    def Get_Type(self ):
        return self._type
    #@abstractmethod
    def Set_Address_A(self, A ):
        self.Address_A = A
    #@abstractmethod
    def Set_Address_PL(self, PL ):
        self.Address_PL = PL
    #@abstractmethod
    def Set_Address(self, A , PL):
        self.Address_A = A
        self.Address_PL = PL
    #@abstractmethod
    def Get_Address_A(self ):
        return self.Address_A
    #@abstractmethod
    def Get_Address_PL(self ):
        return self.Address_PL
    #@abstractmethod
    def Get_Address(self ):
        return (self.Address_A * 16) + self.Address_PL
    #@abstractmethod
    def address(self, A, PL):
        raise NotImplementedError()
    #@abstractmethod
    def Set_Stato(self, stato):
        self._statoInterfaccia = stato
        self._CHANGEstatoInterfaccia = True
    #@abstractmethod
    def Get_Stato(self):
        return self._statoInterfaccia
    #@abstractmethod
    def Is_Change_Stato(self):
        if(self._CHANGEstatoInterfaccia == True):
            self._CHANGEstatoInterfaccia = False
            return True
        return False
    #@abstractmethod
    def Reset_Change_Stato(self):
        self._CHANGEstatoInterfaccia = False




# seriale uart
class SCSshield(object):
    __instance = None
    STATE_MACHINE_Read_TRAMA = 0
    _ctn_interfacee = 0
    list_scsdevice = list()
    BYTE_TRAMA = bytearray()
    data_RX_receiver = bytearray()

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if SCSshield.__instance == None:
            SCSshield()
        return SCSshield.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SCSshield.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SCSshield.__instance = self

        #SCSshield._ctn_interfacee = 0
        #SCSshield.list_scsdevice = list()

        #SCSshield.STATE_MACHINE_Read_TRAMA = 0
        #SCSshield.BYTE_TRAMA = bytearray()
        #SCSshield.data_RX_receiver = bytearray()


    #BYTES MANIPULATION
    def bitwise_and_bytes(a, b):
        result_int = int.from_bytes(a, byteorder="big") & int.from_bytes(b, byteorder="big")
        return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

    def bitwise_or_bytes(a, b):
        result_int = int.from_bytes(a, byteorder="big") | int.from_bytes(b, byteorder="big")
        return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

    def bitwise_xor_bytes(a, b):
        result_int = int.from_bytes(a, byteorder="big") ^ int.from_bytes(b, byteorder="big")
        return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

    def bitwise_shiftleft_bytes(a, b):
        result_int = int.from_bytes(a, byteorder="big") << int.from_bytes(b, byteorder="big")
        return result_int.to_bytes(max(len(a), len(b)), byteorder="big")



    def SetUART(self, ser):
        self.uartport = ser


    def Rec_QuequeUartRx(self, q):
        self.QuequeUartRx = q

    async def interfaccia_send_COMANDO(self, A, PL, stato, attendi_risposta):
        #print("interfaccia_send_COMANDO " + str(A))

        checkbytes = b'\x00'

        old_stato = stato

        address = b'\x00'
        address = SCSshield.bitwise_and_bytes(bytes([A]), b'\x0F')
        address = SCSshield.bitwise_shiftleft_bytes(address , b'\x04')
        address = SCSshield.bitwise_and_bytes(address, b'\xF0')
        address = SCSshield.bitwise_or_bytes(address, bytes([PL]) )

        mret = old_stato

        for i in range(8):


            checkbytes = b'\x00'
            checkbytes = address
            checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, b'\x00')
            checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, b'\x12')
            checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bytes([stato]))

            #bufferTxscs = [b'\xA8', address, b'\x00', b'\x12', bytes([stato]), checkbytes, b'\xA3']
            bufferTxscs = [ int.from_bytes(b'\xA8', "big") , int.from_bytes(address, "big") , int.from_bytes(b'\x00', "big"), int.from_bytes(b'\x12', "big") , int.from_bytes(bytes([stato]), "big") , int.from_bytes(checkbytes, "big") , int.from_bytes(b'\xA3', "big") ]

            #ser.flushInput()
            #ser.flushOutput()
            #await self.uartport.flushInput()

            #async with self.QuequeUartRx:
            for _ in range(self.QuequeUartRx.qsize()):
                # Depending on your program, you may want to
                # catch QueueEmpty
                self.QuequeUartRx.get_nowait()
                self.QuequeUartRx.task_done()


            await self.uartport.write(  bufferTxscs  ) # Drop anything that was already received
            await asyncio.sleep(0) # Let's be a bit greedy, should be adjust to your needs


            mret = old_stato
            
            if(attendi_risposta == 1):
                #line = await self.uartport.read() # Read a line
                

                try:
                    #print("wait rx uart")
                    v = await asyncio.wait_for(self.QuequeUartRx.get(), timeout=0.1)
                    if(v == b'\xA5'):
                        #print("CCCCCCOOOOOOORRRRRRRRREEEEEEEETTTTTT")

                        if(stato == 1):
                            return 0
                        elif(stato == 0):
                            return 1
                        else:
                            return stato
                except asyncio.TimeoutError:
                    #await asyncio.sleep(0.7)
                    mret = old_stato

                    #print("£TIMEOUTTTTTTTTTTTTTTTTTTT")


                except Exception as e:
                    print("EEEEEEERRRRRRROOOOORRRRRRRRRRRR")   
                    print(e)

            else:
                if(i == 2):
                    if(stato == 1):
                        stato = 0
                    else:
                        stato = 1
                    return stato

            
        return mret


    async def interfaccia_send_COMANDO_7_RAW(self, bufferval):
        #print("interfaccia_send_COMANDO_7_RAW ")

        checkbytes = b'\x00'
        checkbytes = bufferval[1]
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[2])
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[3])
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[4])

        sendBuffer = [int.from_bytes(bufferval[0], "big"),int.from_bytes(bufferval[1], "big"),int.from_bytes(bufferval[2], "big"),int.from_bytes(bufferval[3], "big"),int.from_bytes(bufferval[4], "big"),int.from_bytes(checkbytes, "big"),int.from_bytes(bufferval[6], "big")]
        await self.uartport.write(  sendBuffer  ) # Drop anything that was already received
        await asyncio.sleep(0) # Let's be a bit greedy, should be adjust to your needs

    async def interfaccia_send_COMANDO_11_RAW(self, bufferval):
        #print("interfaccia_send_COMANDO_11_RAW ")

        checkbytes = b'\x00'
        checkbytes = bufferval[1]
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[2])
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[3])
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[4])
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[5])
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[6])
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[7])
        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, bufferval[8])

        sendBuffer = [int.from_bytes(bufferval[0], "big"),int.from_bytes(bufferval[1], "big"),
                    int.from_bytes(bufferval[2], "big"),int.from_bytes(bufferval[3], "big"),
                    int.from_bytes(bufferval[4], "big"),int.from_bytes(bufferval[5], "big"),
                    int.from_bytes(bufferval[6], "big"),int.from_bytes(bufferval[7], "big"),
                    int.from_bytes(bufferval[8], "big"),int.from_bytes(checkbytes, "big"),
                    int.from_bytes(bufferval[10], "big")]
        
        await self.uartport.write(  sendBuffer  ) # Drop anything that was already received
        await asyncio.sleep(0) # Let's be a bit greedy, should be adjust to your needs



    """
    #esempio x debuc xa8 x01 x05 x08 x10 x1C xa3
        a8 B8 64 00 01 DD a3
        a8 B8 64 00 00 DC a3
    """

    def search_TRAMA(val, START, FINISH):
        #print("search_TRAMA " )
        risultato = 0

        #print("**1*** search_TRAMA DA{}" .format(val))
        #print("**1*** search_TRAMA TY{}" .format(type(val)))

        for i,e  in enumerate(range(len(val))):
            v = bytes([val.pop(0)])
            
            #print("**2*** for loop v.pop = {}" .format(v))
            #print("**2*** for loop v.pop type= {}" .format(type(v)))

            if(SCSshield.STATE_MACHINE_Read_TRAMA == 0):
                #find A8
                #print("**3*** FIND A8 ")

                #print("**3*** v =  {}" .format(v))
                #print("**3*** v =  {}" .format(START))
                #print("**3*** v =  {}" .format(v == START))

                if(v == START):
                    #print("**3*** FIND A8 --- METCH!!! ")
                    SCSshield.BYTE_TRAMA = list()
                    SCSshield.BYTE_TRAMA.append(v)
                    SCSshield.STATE_MACHINE_Read_TRAMA = 1
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 1):
                SCSshield.BYTE_TRAMA.append(v)
                SCSshield.STATE_MACHINE_Read_TRAMA = 2
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 2):
                SCSshield.BYTE_TRAMA.append(v)
                SCSshield.STATE_MACHINE_Read_TRAMA = 3
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 3):
                SCSshield.BYTE_TRAMA.append(v)
                SCSshield.STATE_MACHINE_Read_TRAMA = 4
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 4):
                SCSshield.BYTE_TRAMA.append(v)
                SCSshield.STATE_MACHINE_Read_TRAMA = 5
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 5):
                SCSshield.BYTE_TRAMA.append(v)
                SCSshield.STATE_MACHINE_Read_TRAMA = 6
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 6):
                SCSshield.BYTE_TRAMA.append(v)
                if(v != FINISH):
                    #print("**4*** TRAMA ESTESA TROVATA!!! ")

                    SCSshield.STATE_MACHINE_Read_TRAMA = 7
                else:
                    if(v == FINISH):
                        #Verifica checksum se corretto
                        checkbytes = SCSshield.bitwise_xor_bytes(SCSshield.BYTE_TRAMA[1]  , SCSshield.BYTE_TRAMA[2])
                        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, SCSshield.BYTE_TRAMA[3])
                        checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, SCSshield.BYTE_TRAMA[4])
                        if(checkbytes == SCSshield.BYTE_TRAMA[5]):
                            #print("**4*** CHECK SUM   CORRRETTTOOOO!!! ")
                            risultato = 1                            
                    SCSshield.STATE_MACHINE_Read_TRAMA = 0
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 7):
                SCSshield.BYTE_TRAMA.append(v)
                SCSshield.STATE_MACHINE_Read_TRAMA = 8
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 8):
                SCSshield.BYTE_TRAMA.append(v)
                SCSshield.STATE_MACHINE_Read_TRAMA = 9
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 9):
                SCSshield.BYTE_TRAMA.append(v)
                SCSshield.STATE_MACHINE_Read_TRAMA = 10
            elif(SCSshield.STATE_MACHINE_Read_TRAMA == 10):
                SCSshield.BYTE_TRAMA.append(v)
                if(v == FINISH):
                    #Verifica checksum se corretto
                    checkbytes = SCSshield.bitwise_xor_bytes(SCSshield.BYTE_TRAMA[1]  , SCSshield.BYTE_TRAMA[2])
                    checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, SCSshield.BYTE_TRAMA[3])
                    checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, SCSshield.BYTE_TRAMA[4])
                    checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, SCSshield.BYTE_TRAMA[5])
                    checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, SCSshield.BYTE_TRAMA[6])
                    checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, SCSshield.BYTE_TRAMA[7])
                    checkbytes = SCSshield.bitwise_xor_bytes(checkbytes, SCSshield.BYTE_TRAMA[8])
                    if(checkbytes == SCSshield.BYTE_TRAMA[9]):
                        risultato = 2   #TRAMA ESTESA
                        #print("**4*** CALCOLO CHECKSUM TRAMA ESTESA!!! {}" .format(checkbytes))
                SCSshield.STATE_MACHINE_Read_TRAMA = 0
            else:
                SCSshield.STATE_MACHINE_Read_TRAMA = 0

            if(risultato > 0):
                #print("**5*** BREAK search_TRAMA , MATCH FIND!!! ")
                break

        return val, risultato






    #Lista DEVICE
    def addDevice(self, mdevice):
        SCSshield.list_scsdevice.append(mdevice)
        #debug
        #print("ADD DEVICE")
        #print(mdevice.Get_Nome_Attuatore() )

    def clearDevice(self):
        SCSshield.list_scsdevice = list()

    def getDevices(self):
        return SCSshield.list_scsdevice

    #GESTIONE SERIALE
    def __await__(self):
        # see: https://stackoverflow.com/a/33420721/1113207
        return self._async_init().__await__()

    async def uart_rx(self, jqueqe):
        #await self.uartport.read() # Drop anything that was already received
        while True:
            line = await self.uartport.read() # Read a line

            #print("*1******* SERIALE DATA RECEIVER: {}" .format(line))
            #print("*1******* SERIALE DATA RECEIVER TYPE: {}" .format(type(line)))


            await self.QuequeUartRx.put(line)

            SCSshield.data_RX_receiver = SCSshield.data_RX_receiver + line

            #print("*2******* DATA RECEIVER, somma buffer: {}" .format(SCSshield.data_RX_receiver))

            #ic = 0

            while(len(SCSshield.data_RX_receiver) > 0 ):
                SCSshield.data_RX_receiver, risultato = SCSshield.search_TRAMA(SCSshield.data_RX_receiver, b'\xA8', b'\xA3')

                #print("*2******* DATA RECEIVER, buffer rimanenti da prosessare: {}" .format(SCSshield.data_RX_receiver))
                #print("*3******* DATA RECEIVER, risultato: {}" .format(risultato))

                if(risultato > 0):
                    #Trama Trovata
                    #SCSshield.BYTE_TRAMA #qui il dato

                    await jqueqe.put(SCSshield.BYTE_TRAMA)

                    #print("*4******* DATA RECEIVER, TRAMA TROVATAAAAAAAAAAAAA: {}" .format(SCSshield.BYTE_TRAMA))
                    SCSshield.BYTE_TRAMA = bytearray()
                    await asyncio.sleep(0)

                    #ic = ic + 1
                    #print(ic)

            #print("*2******* DATA RECEIVER, buffer rimanenti da prosessare: {}" .format(SCSshield.data_RX_receiver))
            #print("*3******* DATA RECEIVER, risultato: {}" .format(risultato))

            """
            if(risultato == 1):
                #Trama Trovata
                #SCSshield.BYTE_TRAMA #qui il dato
                print("*4******* DATA RECEIVER, TRAMA TROVATAAAAAAAAAAAAA: {}" .format(SCSshield.BYTE_TRAMA))
                SCSshield.BYTE_TRAMA = bytearray()
            """


            #print("[+] Serial read: {}".format(line))
            await asyncio.sleep(0) # Let's be a bit greedy, should be adjust to your needs
            #await asyncio.sleep(3) # Let's be a bit greedy, should be adjust to your needs











"""
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------

SWITCH

------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
"""

class Switch(SCSDevice):
    def __init__(self, scsshield):
        self.scsshield = scsshield
        #self.lock_uartTX = lock_uartTX

        super().__init__()
        super().Set_Type(TYPE_INTERfACCIA.on_off)
        super().Set_Stato(0)
        super().Reset_Change_Stato()
    
    async def On(self,look):        
        #print("WAIT MUTEX --> [Switch.On] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Switch.On] " +  super().Get_Nome_Attuatore())
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 0, 1)
            
            #print("STATO: " + str(stato))

            super().Set_Stato(stato)
            super().Reset_Change_Stato()
            await asyncio.sleep(0)

    async def Off(self,look):
        #print("WAIT MUTEX --> [Switch.Off] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Switch.Off] " +  super().Get_Nome_Attuatore())
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 1, 1)
            super().Set_Stato(stato)
            super().Reset_Change_Stato()
            await asyncio.sleep(0)

    async def Toggle(self,look):
        #print("WAIT MUTEX --> [Switch.Toggle] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Switch.Toggle] " +  super().Get_Nome_Attuatore())
            stato = 1
            if (super().Get_Stato()== 1):
                stato = 0
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), stato, 1)
            super().Set_Stato(stato)
            super().Reset_Change_Stato()
            await asyncio.sleep(0)


    def Stato(self):
        stato = 1
        if (super().Get_Stato()== 1):
            stato = 0
        return stato



"""
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------

SERRANDE/TAPPARELLE

------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
"""

class Serranda(SCSDevice):
    def __init__(self, scsshield):
        self.scsshield = scsshield
        #self.lock_uartTX = lock_uartTX

        super().__init__()
        super().Set_Type(TYPE_INTERfACCIA.serrande_tapparelle)
        super().Set_Stato(0)
        super().Reset_Change_Stato()

        self.timer_salita_ = 4000
        self.timer_discesa_ = 4000
        self.stato_percentuale = 0

        self.timer = None #Timerelapsed.Timer(10, self._timerCallback_elapsed)
        self.timerSTOP = 0
        self.timerSTARTmove = 0
        self.statoComando = 0
        self.lastComando = 0

        self.cmd1 = None 
        self.mqttclient = None
        self.loop = None

    def register_MQTT_POST(self, mqttclient, loop):
        self.mqttclient = mqttclient
        self.loop = loop

    async def _timerCallback_elapsed(self):
        #print("TIMERRRRRRRRR   OUTTTTTTTTTTTTTTTTTTTTTTT")
        self.Ricalcolo_Percent_from_timerelaspe()


    def start_timer(self, time):
        if((self.timer == None)or(self.timer.done()==True)):
            #print("START TIMER")
            self.timer = Timerelapsed.Timer(time, self._timerCallback_elapsed)            
        else:
            #print("START gia in azione TIMER")
            pass


    def stop_timer(self):
        if(self.timer != None):
            if(self.timer.done()==False):
                self.timer.cancel()
                #print("Force to cancel")


    def RecTimer(self, action):
        if(self.lastComando == 0):
            self.timerSTARTmove = time.time_ns() / 1000000  # in mS
            self.statoComando = action
            self.lastComando = action
        else:
            #print("STESSO COMANDO, NIENTE AZIONE")
            #stesso comando precedente ma ripetuto
            pass

    def Ricalcolo_Percent_from_timerelaspe(self):
        if(self.lastComando != 0):
            timerATTUALE = time.time_ns() / 1000000  # in mS
            timerElapsed = timerATTUALE - self.timerSTARTmove

            #print("SERRANDA Stop , timerElapsed:  " + str(timerElapsed))
            #print("SERRANDA Stop , statoComando:  " + str(self.statoComando))


            if(self.statoComando == 1):
                #APRI
                if(timerElapsed > self.timer_salita_):
                    timerElapsed = self.timer_salita_

                calcoloperc = (100.0 / self.timer_salita_) * timerElapsed
                self.stato_percentuale = self.stato_percentuale + calcoloperc

                if(self.stato_percentuale > 100):
                    self.stato_percentuale = 100

                #print("SERRANDA Stop, [apri] , new % :  " + str(self.stato_percentuale))


            elif(self.statoComando == -1):
                #CHIUDI
                if(timerElapsed > self.timer_discesa_):
                    timerElapsed = self.timer_discesa_
            
                calcoloperc = (100.0 / self.timer_discesa_) * timerElapsed
                self.stato_percentuale = self.stato_percentuale - calcoloperc

                if(self.stato_percentuale < 0 ):
                    self.stato_percentuale = 0

                #print("SERRANDA Stop, [chiudi] , new % :  " + str(self.stato_percentuale))
        
            self.statoComando = 0
            self.lastComando = 0


            if(self.mqttclient != None):                
                self.loop.create_task(self.mqttclient.post_to_MQTT( "/scsshield/device/" + super().Get_Nome_Attuatore() + "/status", "{:.0f}".format(self.stato_percentuale)  ))


        else:
            #print("STESSO COMANDO, NIENTE AZIONE")
            #stesso comando precedente ma ripetuto
            pass

    async def Azione(self, value_percent, look):
        pattuale = self.stato_percentuale
        delta = value_percent - pattuale

        if(delta>=0):
            #sali di "delta" %
            # converti in tempo
            millisecond_action = delta / (100 / self.timer_salita_) 
            
            await self.Alza(millisecond_action, look)

        else:
            #scendi di "delta"
            # converti in tempo
            millisecond_action = abs(delta) / (100 / self.timer_discesa_) 

            await self.Abbassa(millisecond_action, look)

    async def Stop(self,look):
        #print("WAIT MUTEX --> [Serranda.Stop] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Serranda.Stop] " +  super().Get_Nome_Attuatore())
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 10, 1)
            await asyncio.sleep(0)


    async def Alza(self, timevalue, look):
        #print("WAIT MUTEX --> [Serranda.Alza] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Serranda.Alza] " +  super().Get_Nome_Attuatore())
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 10, 1)

            #print("STATO_1: " + str(stato))

            if(stato == 10):
                await asyncio.sleep(0.5)
                stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 8, 1)
                #print("STATO_2: " + str(stato))

            super().Set_Stato(stato)
            super().Reset_Change_Stato()

        #print("aspetto serranda tempo: " + str(timevalue))

        await asyncio.sleep(timevalue/1000)

        await self.Stop(look)


        await asyncio.sleep(0)


    async def Abbassa(self, timevalue, look):
        #print("WAIT MUTEX --> [Serranda.Abbassa] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Serranda.Abbassa] " +  super().Get_Nome_Attuatore())
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 10, 1)


            #print("STATO: " + str(stato))

            if(stato == 10):
                await asyncio.sleep(0.5)
                stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 9, 1)

            super().Set_Stato(stato)
            super().Reset_Change_Stato()

        #print("aspetto serranda tempo: " + str(timevalue))

        await asyncio.sleep(timevalue/1000)

        await self.Stop(look)

        await asyncio.sleep(0)

    def get_percentuale(self):
        return self.stato_percentuale

    def set_Timer(self, timer_salita, timer_discesa):
        self.timer_salita_ = timer_salita
        self.timer_discesa_ = timer_discesa
        



"""
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------

dimmer

------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
"""

                            #10%       20%     30%      40%     50%       60%     70%      80%     90%      100%
dimmerCodifica = [b'\x01', b'\x0D', b'\x1D' ,b'\x2D', b'\x3D', b'\x4D', b'\x5D', b'\x6D', b'\x7D', b'\x8D', b'\x9D']


class Dimmer(SCSDevice):
    def __init__(self, scsshield):
        self.scsshield = scsshield
        #self.lock_uartTX = lock_uartTX

        super().__init__()
        super().Set_Type(TYPE_INTERfACCIA.dimmer)
        super().Set_Stato(0)
        super().Reset_Change_Stato()


    
    async def On(self,look):        
        #print("WAIT MUTEX --> [Dimmer.On] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Dimmer.On] " +  super().Get_Nome_Attuatore())
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 0, 1)
            
            #print("STATO: " + str(stato))

            super().Set_Stato(stato)
            super().Reset_Change_Stato()
            await asyncio.sleep(0)

    async def Off(self,look):
        #print("WAIT MUTEX --> [Dimmer.Off] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Dimmer.Off] " +  super().Get_Nome_Attuatore())
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 1, 1)
            super().Set_Stato(stato)
            super().Reset_Change_Stato()
            await asyncio.sleep(0)

    async def Toggle(self,look):
        #print("WAIT MUTEX --> [Dimmer.Toggle] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Dimmer.Toggle] " +  super().Get_Nome_Attuatore())
            stato_dimmer = super().Get_Stato()

            if((stato_dimmer > 1)or(stato_dimmer == 0)):
                stato_rele = 1
            else:
                stato_rele = 0
            
            stato_rele = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), stato_rele, 1)

            super().Set_Stato(stato_rele)
            super().Reset_Change_Stato()
            await asyncio.sleep(0)

    async def Set_Dimmer_percent(self, val, look):
        percentuale = int(val)
 
        #print("WAIT MUTEX --> [Dimmer.set_Dimmer] " +  super().Get_Nome_Attuatore() )
        if(percentuale > 100):
            percentuale = 100
        if(percentuale < 0):
            percentuale = 0

        """
            0% = 10
            100& = 100%
        """

        async with look:      
            try:  
                #print("--------------> [Dimmer.set_Dimmer] " +  super().Get_Nome_Attuatore())

                percmod = self.valmap(percentuale,0,100,10,100)       #percentuale varia da 0:100 a --> 10:100

                v = int(percmod / 10)
                valueDimmer = dimmerCodifica[v]

                stato_rele = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(),  int.from_bytes(valueDimmer, "big"), 1)

                super().Set_Stato(int.from_bytes(valueDimmer, "big"))
                super().Reset_Change_Stato()
                await asyncio.sleep(0)
            except Exception as e:
                print("EEEEEEEEEEEEEEEEEEEEEE")
                print(e)

    def valmap(self, value, istart, istop, ostart, ostop):
        return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


    def Get_Dimmer_percent(self):
        stato_dimmer = super().Get_Stato()
        """
        if(type(stato_dimmer) == bytes):
            stato_dimmer = int.from_bytes(stato_dimmer, "big")
        """

        stato = 0

        if(stato_dimmer == 0):
            #Acceso
            stato = 1
        elif(stato_dimmer == 1):
            #Spento
            stato = 0
        elif(stato_dimmer > 1):
            #Acceso con dimmerazione
            for i, _ in enumerate(dimmerCodifica):
                #print(i, _)
                if(_ == bytes([stato_dimmer])):
                    stato = i*10        #ritorna PERCENTUALE
                    #percmod = self.valmap(stato,0,90,0,100)       #percentuale varia da 0:100 a --> 10:100
                    #stato = percmod
                    break
        return stato  


"""
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------

Sensori Temperatura

------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
"""

class Sensori_Temperatura(SCSDevice):
    def __init__(self, scsshield):
        self.scsshield = scsshield

        super().__init__()
        super().Set_Type(TYPE_INTERfACCIA.sensori_temperatura)
        super().Set_Stato(0)
        super().Reset_Change_Stato()


    async def Forza_la_lettura_Temperatura(self, look):

        try:
            #print("WAIT MUTEX --> [Sensori_Temperatura.Forza_la_lettura_Temperatura] " +  super().Get_Nome_Attuatore() )

            async with look:        
                #print("--------------> [Sensori_Temperatura.Forza_la_lettura_Temperatura] " +  super().Get_Nome_Attuatore())

                address = b'\x00'
                address = SCSshield.bitwise_and_bytes(bytes([super().Get_Address_A()]), b'\x0F')
                address = SCSshield.bitwise_shiftleft_bytes(address , b'\x04')
                address = SCSshield.bitwise_and_bytes(address, b'\xF0')
                address = SCSshield.bitwise_or_bytes(address, bytes([super().Get_Address_PL()]) )

                bufval = [b'\xA8',b'\x99',address,b'\x30',b'\x00',b'\x00',b'\xA3']

                await self.scsshield.interfaccia_send_COMANDO_7_RAW( bufval )
                await asyncio.sleep(0.1)
        except Exception as e:
            print("EEEEEEEEEEEEE")
            print(e)


"""
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------

Termostati

------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
"""

class Termostati(SCSDevice):
    def __init__(self, scsshield):
        self.scsshield = scsshield

        super().__init__()
        super().Set_Type(TYPE_INTERfACCIA.termostati)
        super().Set_Stato(0)
        super().Reset_Change_Stato()

        self.Temperatura_Termostato = 0
        self.Modalita_Termostato = 0

        self.sensoreT = None

        
    def Set_obj_SensoreTemp(self, objSensore):
        self.sensoreT = objSensore
    def Get_obj_SensoreTemp(self):
        return self.sensoreT


    class MODALITA(Enum):
        OFF = "OFF"
        INVERNO = "INVERNO"
        ESTATE = "ESTATE"


    def Set_Temperatura_Termostato(self, value):
        self.Temperatura_Termostato = value

    def Set_Modalita_Termostato(self, value):
        self.Modalita_Termostato = value

    def Get_Temperatura_Termostato(self):
        return self.Temperatura_Termostato

    def Get_Modalita_Termostato(self):
        return self.Modalita_Termostato

  
    async def set_temp_termostato(self, temp, look):
        try:
            #print("WAIT MUTEX --> [Termostati.set_temp_termostato] " +  super().Get_Nome_Attuatore() + "  temp=" + str(temp))

            val = (((temp - 3) / 0.5) + 6)


            async with look:        
                #print("--------------> [Termostati.set_temp_termostato] " +  super().Get_Nome_Attuatore())

                address = b'\x00'
                address = SCSshield.bitwise_and_bytes(bytes([super().Get_Address_A()]), b'\x0F')
                address = SCSshield.bitwise_shiftleft_bytes(address , b'\x04')
                address = SCSshield.bitwise_and_bytes(address, b'\xF0')
                address = SCSshield.bitwise_or_bytes(address, bytes([super().Get_Address_PL()]) )

                bufval = [b'\xA8',b'\xD1',address,b'\x03',b'\x02',b'\xC1',b'\x02',bytes([int(val)]),b'\x00',b'\x00',b'\xA3']

                await self.scsshield.interfaccia_send_COMANDO_11_RAW( bufval )
                await asyncio.sleep(0.1)
        except Exception as e:
            print("EEEEEEEEEEEEE")
            print(e)

    async def set_modalita_termostato(self, modalita, look):
        try:
            #print("WAIT MUTEX --> [Termostati.set_modalita_termostato] " +  super().Get_Nome_Attuatore() + "   modalita: " + modalita)

            address = b'\x00'
            address = SCSshield.bitwise_and_bytes(bytes([super().Get_Address_A()]), b'\x0F')
            address = SCSshield.bitwise_shiftleft_bytes(address , b'\x04')
            address = SCSshield.bitwise_and_bytes(address, b'\xF0')
            address = SCSshield.bitwise_or_bytes(address, bytes([super().Get_Address_PL()]) )

            if(modalita.lower() == 'off'):
                bufval = [b'\xA8',b'\xD1',address,b'\x03',b'\x02',b'\xC1',b'\x06',b'\x00',b'\x00',b'\x00',b'\xA3']
            elif(modalita.lower() == 'inverno'):
                bufval = [b'\xA8',b'\xD1',address,b'\x03',b'\x02',b'\xC1',b'\xF1',b'\x00',b'\x00',b'\x00',b'\xA3']          
            elif(modalita.lower() == 'estate'):
                bufval = [b'\xA8',b'\xD1',address,b'\x03',b'\x02',b'\xC1',b'\xF0',b'\x00',b'\x00',b'\x00',b'\xA3']          
            else:
                bufval = []

            async with look:        
                #print("--------------> [Termostati.set_modalita_termostato] " +  super().Get_Nome_Attuatore())
                if(len(bufval)>0):
                    await self.scsshield.interfaccia_send_COMANDO_11_RAW( bufval )
                    await asyncio.sleep(0.1)
        except Exception as e:
            print("EEEEEEEEEEEEE")
            print(e)






"""
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------

GRUPPI

------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
"""

class Gruppi(SCSDevice):
    def __init__(self, scsshield):
        self.scsshield = scsshield
        #self.lock_uartTX = lock_uartTX

        super().__init__()
        super().Set_Type(TYPE_INTERfACCIA.gruppi)
        super().Set_Stato(0)
        super().Reset_Change_Stato()
    
    async def On(self,look):        
        #print("WAIT MUTEX --> [Switch.On] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Switch.On] " +  super().Get_Nome_Attuatore())
            stato = 0
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 0, 0)
            
            #print("STATO: " + str(stato))

            super().Set_Stato(stato)
            super().Reset_Change_Stato()
            await asyncio.sleep(0)

    async def Off(self,look):
        #print("WAIT MUTEX --> [Switch.Off] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Switch.Off] " +  super().Get_Nome_Attuatore())
            stato = 1
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), 1, 0)
            super().Set_Stato(stato)
            super().Reset_Change_Stato()
            await asyncio.sleep(0)

    async def Toggle(self,look):
        #print("WAIT MUTEX --> [Switch.Toggle] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Switch.Toggle] " +  super().Get_Nome_Attuatore())
            stato = 1
            if (super().Get_Stato()== 1):
                stato = 0
            stato = await self.scsshield.interfaccia_send_COMANDO(super().Get_Address_A(), super().Get_Address_PL(), stato, 0)
            super().Set_Stato(stato)
            super().Reset_Change_Stato()
            await asyncio.sleep(0)







"""
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------

SERRATURE

------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
"""

class Serrature(SCSDevice):
    def __init__(self, scsshield):
        self.scsshield = scsshield
        #self.lock_uartTX = lock_uartTX

        super().__init__()
        super().Set_Type(TYPE_INTERfACCIA.serrature)
        super().Set_Stato(0)
        super().Reset_Change_Stato()
    
    async def Sblocca(self,look):        
        #print("WAIT MUTEX --> [Serratura.On] " +  super().Get_Nome_Attuatore() )

        async with look:        
            #print("--------------> [Serratura.On] " +  super().Get_Nome_Attuatore())

            address = b'\x00'
            #address = SCSshield.bitwise_and_bytes(bytes([super().Get_Address_A()]), b'\x0F')
            address = SCSshield.bitwise_and_bytes(b'\x0A', b'\x0F')
            address = SCSshield.bitwise_shiftleft_bytes(address , b'\x04')
            address = SCSshield.bitwise_and_bytes(address, b'\xF0')
            address = SCSshield.bitwise_or_bytes(address, bytes([super().Get_Address_A()]) )

            bufval = [b'\xA8',b'\x96',address,b'\x6F',b'\xA4',b'\x00',b'\xA3']

            await self.scsshield.interfaccia_send_COMANDO_7_RAW( bufval )
            
            #print("STATO: " + str(stato))

            super().Reset_Change_Stato()
            await asyncio.sleep(0)



"""
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------

CAMPANELLO

------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
"""

class Campanello(SCSDevice):
    def __init__(self, scsshield):
        self.scsshield = scsshield
        #self.lock_uartTX = lock_uartTX

        super().__init__()
        super().Set_Type(TYPE_INTERfACCIA.campanello_porta)
        super().Set_Stato(0)
        super().Reset_Change_Stato()
    
        self.timer = None #Timerelapsed.Timer(10, self._timerCallback_elapsed)
        self.mqttclient = None
        self.loop = None

    def register_MQTT_POST(self, mqttclient, loop):
        self.mqttclient = mqttclient
        self.loop = loop

    async def _timerCallback_elapsed(self):
        if(self.mqttclient != None):                
            self.loop.create_task(self.mqttclient.post_to_MQTT( "/scsshield/device/" + super().Get_Nome_Attuatore() + "/status", "0"))

    def start_timer(self, time):
        if((self.timer == None)or(self.timer.done()==True)):
            #print("START TIMER")
            self.timer = Timerelapsed.Timer(time, self._timerCallback_elapsed)
            if(self.mqttclient != None):                
                self.loop.create_task(self.mqttclient.post_to_MQTT( "/scsshield/device/" + super().Get_Nome_Attuatore() + "/status", "1"))

    def stop_timer(self):
        if(self.timer != None):
            if(self.timer.done()==False):
                self.timer.cancel()
                if(self.mqttclient != None):                
                    self.loop.create_task(self.mqttclient.post_to_MQTT( "/scsshield/device/" + super().Get_Nome_Attuatore() + "/status", "0"))




























"""
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------

Test

------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
------------------------------------------------------------------------------
"""


class objsTYPE():
    def __init__(self, o):
        self.o = o
    def Get_Type(self ):
        return self.o.Get_Type()





if __name__ == "__main__":    
    print("*****scs library*****")
    
    s1 = Switch()
    s1.Set_Address_A(3)
    s2 = Switch()
    s2.Set_Address_A(5)
    

    print(s1.Get_Address_A())
    print(s2.Get_Address_A())
    print(s1.Get_Type())
    print(s2.Get_Type())
    print(s1.Get_Type())

    print("*****scs library*****")

    poliformismo = objsTYPE(s2)
    print( poliformismo.Get_Type() )
    

    shield = SCSshield()
    #shield.SetUART()

    s1 = Termostati(shield)
    s1.Set_Address(3,2)
    s1.Set_Nome_Attuatore("termooo")


