from datetime import datetime

import struct

BASE_YEAR = 2000

class MessageBuilder:

    def __init__(self):
        self._message = bytearray()
    
    def to_bytes(self) -> bytes:
        """ Gets the encoded message as a byte array """
        return bytes(self._message)

    def append_hello(self, dead_interval: int):
        """ Encodes a HELLO field in the message """
        print("Appending Hello")
        self._message.extend((b'\x02'))
        interval2 = (dead_interval % 256)
        interval1 = (int(dead_interval / 256))
        print(f"interval1: {interval1}")
        print(f"interval2: {interval2}")
        self._message.extend(struct.pack('>B', (interval1)))
        self._message.extend(struct.pack('>B', (interval2)))
        #self._message.extend(struct.pack('>B', int(interval1)))
        #self._message.extend(struct.pack('>B', int(interval2)))
        #self._message.extend(hex(dead_interval))
        print(f"Appended Hello: {self._message}")

    def _crunch(self, string: str):
        b = bytes.fromhex(string)
        self._message.append(b)


    def append_date(self, dt: datetime):
        """ Encodes a DATE field in the message """
        print("Appending Date")
        self._message.extend(bytes(b'\x14'))

        century = (int((dt.year - BASE_YEAR) / 100)) * 8
        year = dt.year % 100
        print(f"Year: {year}")
        month = dt.month
        #month = '{:0^{width}}'.format(dt.month, width=2)
        day_month = '{:0^{width}}'.format(dt.day, width=2)
        week_day = dt.weekday()


        pack1 = int(f"{century}{week_day}")
        pack1 = hex(pack1)[2:]
        print(f"pack 1 : {pack1}")
        #self._message.extend(bytes(pack1, 'utf-8'))
        self._message.extend(struct.pack('>B', int(pack1, 16)))

        year_hex = int((int(year / 10) * 16) + (year % 10))
        pack2 = hex(year_hex)[2:]
        print(f"pack 2 : {pack2}")
        self._message.extend(struct.pack('>B', int(pack2, 16)))

        print(month)
        pack3 = hex(int(month))[2:]
        print(f"pack 3 : {pack3}")
        self._message.extend(struct.pack('>B', int(pack3, 16)))

        pack4 = hex(int(day_month))[2:]
        print(f"pack 4 : {pack4}")
        self._message.extend(struct.pack('>B', int(pack4, 16)))

        print(f"appended date: {self._message}")

    def append_time(self, dt: datetime):
        """ Encodes a TIME field in the message """
        self._message.extend(bytes(b'\x24'))
        hour = dt.hour
        minute = dt.minute
        second = dt.second
        centi = dt.microsecond % 100
        #hour = '{:0^{width}}'.format(dt.hour, width=2)
        #minute = '{:0^{width}}'.format(dt.minute, width=2)
        #second = '{:0^{width}}'.format(dt.second, width=2)
        #centi = '{:0^{width}}'.format(str(dt.microsecond)[:2], width=2)
        #mid = int(dt.microsecond / 10000) % 255
        #print(f"centi : {dt.microsecond}")
        #print(f"mid: {mid}")
        #hexes = "" + hour + " " + minute + " " + second + " " + centi

        hour_hex = int((int(hour / 10) * 16) + (hour % 10))
        pack1 = hex(hour_hex)[2:]
        print(f"pack 1 : {pack1}")
        #self._message.extend(bytes(pack1, 'utf-8'))
        self._message.extend(struct.pack('>b', int(pack1, 16)))

        minute_hex = int((int(minute / 10) * 16) + (minute % 10))
        pack2 = hex(minute_hex)[2:]
        print(f"pack 2 : {pack2}")
        self._message.extend(struct.pack('>B', int(pack2, 16)))

        second_hex = int((int(second / 10) * 16) + (second % 10))
        pack3 = hex(second_hex)[2:]
        print(f"pack 3 : {pack3}")
        self._message.extend(struct.pack('>B', int(pack3, 16)))

        centi_hex = int((int(centi / 10) * 16) + (centi % 10))
        pack4 = hex(centi_hex)[2:]
        print(f"pack 4 : {pack4}")
        self._message.extend(struct.pack('>B', int(pack4, 16)))

        print(f"appended time: {self._message}")