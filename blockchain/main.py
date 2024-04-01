import os
from typing import Dict, Optional

import websockets
from fastapi import Body, FastAPI, WebSocket, status
from fastapi.responses import RedirectResponse

from blockchain.chain import BlockChain
from blockchain.p2p_server import GetP2PServer, P2PServer
from wallet.transaction_pool import TransactionPool
from wallet.wallet import Wallet
from wallet.wallet_tx import create_transaction

PORT = int(os.environ.get("PORT", 8000))
app = FastAPI()
bc = BlockChain()

wallet = Wallet()
tp = TransactionPool()

app.add_websocket_route("/ws", GetP2PServer(bc, tp), name="p2p")
# app.add_websocket_route("/ws", P2PServer, name="p2p")


@app.get("/blocks")
async def blocks():
    return bc.blocks


@app.get("/public-key")
async def public_key():
    return {"public_key": wallet.public_key}


@app.get("/transactions")
async def transactions():
    return tp.transactions


@app.post("/transact")
async def transact(data: Dict = Body(...)):
    recipient = data["recipient"]
    amount = data["amount"]
    create_transaction(wallet, recipient, amount, tp)

    async with websockets.connect(f"ws://localhost:{PORT}/ws") as ws:
        await ws.send('{"type": "transaction"}')

    return RedirectResponse("/transactions", status_code=status.HTTP_302_FOUND)


@app.post("/mine")
async def mine(data: Dict = Body(...)):
    bc.add_block(data["data"])

    # sync chain by emitting websocket event
    async with websockets.connect(f"ws://localhost:{PORT}/ws") as ws:
        await ws.send('{"type": "chain"}')

    return RedirectResponse("/blocks", status_code=status.HTTP_302_FOUND)
