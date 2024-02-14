
from decimal import Decimal

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def connect_to_node():
    """Connect to a Bitcoin node running on WSL."""
    try:
        # Replace 'user' and 'password' with your RPC user and password
        rpc_connection = AuthServiceProxy("http://%s:%s@localhost:18443" % ("itoro", "itoro"))
        print("connected to regtest")
        return rpc_connection
    except JSONRPCException as json_exception:
        print(json_exception.error)
   

def createTransactions():
    rpc_connection = connect_to_node()
     # Replace with your funded address and desired output address
    # funded_address = "bcrt1qx0rcu8qhapchww7dyznqj8se5lhk63sq6wp95j"
    output_address = "bcrt1qfcjtjle6fs0xmwm6ly9rcnkmwr0z07w8ma7zz5"
    #input = [{"txid": "865bbd2cffba6bdd44259d1ec7a82086126b57abc4e7cc8ced7ad5e37a28328f", "vout": 0}]
    input = [{"txid": "45b34492cd8f0069a5bc152c1e8660fcabbcc27f70734f2a1b81e0a96a93148c", "vout": 0}]
    amount = 0.001  # Amount to send (in BTC)
    fee_rates = [0.00002, 0.0001, 0.00015] #1 sat = 0.00000001 , 1vbyt = 0.001 , 2 sat/vb = 0.00000002 / 0.001 = 0.00002 BTC/KB
    absolute_fee_sats = 10000

    for fee_rate in fee_rates:
        raw_tx = rpc_connection.createrawtransaction(input, {output_address: amount})
        funded_tx = rpc_connection.fundrawtransaction(raw_tx, {'feeRate': fee_rate})
        signed_tx = rpc_connection.signrawtransactionwithwallet(funded_tx['hex'])
        tx_hash = rpc_connection.sendrawtransaction(signed_tx['hex'])
        print(f"Transaction hash: {tx_hash}")

def createTransactionWithAbsoluteFee(txid, voutNumber, outputAddress):
        input = [{"txid": txid, "vout": voutNumber}]
        output_address = outputAddress
        absolute_fee_sats = 10000
        amount = 0.001 

        rpc_connection = connect_to_node()

        raw_tx = rpc_connection.createrawtransaction(input, {output_address: amount})  # replace with your inputs and outputs
        funded_tx = rpc_connection.fundrawtransaction(raw_tx, {'subtractFeeFromOutputs': [0]})  # subtract fee from first output
        print(funded_tx['fee'])
        if int(funded_tx['fee'] * Decimal(1e8)) > absolute_fee_sats:
            print("The absolute fee is too low for this transaction.", absolute_fee_sats, funded_tx['fee'] * Decimal(1e8))
        else:
            signed_tx = rpc_connection.signrawtransactionwithwallet(funded_tx['hex'])
            tx_hash = rpc_connection.sendrawtransaction(signed_tx['hex'])
            print(f"Transaction sent with absolute fee {absolute_fee_sats} sats, txid: {tx_hash}", funded_tx['fee'] * Decimal(1e8))

#node = connect_to_node()
#print(node.getblockchaininfo())
createTransactions()
createTransactionWithAbsoluteFee("5ecb9344dfbb002d68e44e2ddcfc7cebeb01b6c01f53b6476dae544110d4aef0",0,"bcrt1qfcjtjle6fs0xmwm6ly9rcnkmwr0z07w8ma7zz5")
