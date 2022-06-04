import asyncio
import socket
import sys

from connnect_protocol import TCP


class Sender:
    def __init__(self, host, port, connection=TCP):
        self.reader = None
        self.writer = None
        self.host = host
        self.port = port
        self.buff = []

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def is_connected(self):
        return self.writer is not None and self.reader is not None and not self.writer.is_closing()

    async def close(self):
        if self.writer.is_closing():
            return
        else:
            self.writer.close()
            await self.writer.wait_closed()

    async def flush(self):
        if len(self.buff) == 0:
            return
        for item in self.buff:
            self.writer.write(item)
            await self.writer.drain()


async def example():
    se = Sender("127.0.0.1", 9009)
    await se.connect()
    print(await se.is_connected())
    await se.close()
    print(await se.is_connected())
    await se.connect()
    print(await se.is_connected())
    try:
        se.buff.append('test,col1=symbol8,col2=symbol9 col3="ussr5",col4=2322\n'.encode('utf-8'))
        se.buff.append('test,col1=symbol9,col2=symbol8 col4=1111\n'.encode('utf-8'))
        await se.flush()
    except Exception as e:
        sys.stderr.write(f'Got error: {e}')
    await se.writer.drain()


asyncio.run(example())
