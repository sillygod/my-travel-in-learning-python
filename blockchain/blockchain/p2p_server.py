import json
import os
from enum import Enum
from typing import Any

import websockets
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel, validator
from starlette.endpoints import WebSocketEndpoint

from wallet.transaction import Transaction
from wallet.transaction_pool import TransactionPool

from .chain import BlockChain

PEERS = os.environ.get("PEERS", "").split(",")  # array of ws address


class MsgType(str, Enum):

    CHAIN = "chain"
    TRANSACTION = "transaction"


class Msg(BaseModel):

    type: MsgType
    content: str

    @validator("type")
    def _t(cls, v):
        return v.value


def GetP2PServer(chain: BlockChain, transaction_pool: TransactionPool):
    P2PServer.blockchain = chain
    P2PServer.transaction_pool = transaction_pool
    return P2PServer


class P2PServer(WebSocketEndpoint):

    blockchain: BlockChain = None
    transaction_pool: TransactionPool = None
    peer_connected = False
    encoding = "text"  # type: ignore

    def __init__(self, *args, **kwargs):
        self.sockets = []
        super().__init__(*args, **kwargs)

    async def connect_to_peers(self):
        for peer in PEERS:
            if peer != "":
                # uri = "ws://localhost:8765"
                async with websockets.connect(peer) as websocket:
                    ws = WebSocket(
                        {"type": "websocket"}, websocket.recv, websocket.send
                    )
                    self.sockets.append(ws)

    async def message_handler(self, websocket: WebSocket, data: Any) -> None:
        obj = json.loads(data)
        print(f"!!! I received the {obj}")
        self.blockchain.replace_chain(BlockChain.from_blocks(obj))

    async def sync_chain(self):
        for socket in self.sockets:
            # TODO: resolve issue fail to send message here
            msg = Msg(type=MsgType.CHAIN, content=self.blockchain.to_json()).dict()
            await socket.send_json(msg)

    async def send_transaction(socket, transaction: Transaction):
        msg = Msg(type=MsgType.TRANSACTION, content=transaction.to_json()).dict()
        await socket.send_json(msg)

    async def broadcast_transaction(self, transaction):
        for socket in self.sockets:
            await self.send_transaction(socket, transaction)

    async def on_connect(self, websocket: WebSocket) -> None:
        if not P2PServer.peer_connected:
            P2PServer.peer_connected = True
            await self.connect_to_peers()

        await websocket.accept()
        self.sockets.append(websocket)
        await websocket.send_json(self.blockchain.to_json())

    async def on_receive(self, websocket: WebSocket, data: Any) -> None:
        obj = json.loads(data)
        msg = Msg.parse_obj(obj)
        if msg.type == MsgType.CHAIN:
            await self.sync_chain()
            await self.message_handler(websocket, data)

        elif msg.type == MsgType.TRANSACTION:
            # TODO: need to make transaction serializable.
            transaction = msg.content
            self.transaction_pool.update_or_add_transaction(transaction)
            await self.message_handler(websocket, data)
