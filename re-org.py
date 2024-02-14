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

def createRe_Org(expectedBlockReOrgHeight):
    # Setup the connection to the Bitcoin regtest
    rpc_connection = connect_to_node()

    # Get some addresses
    address1 = rpc_connection.getnewaddress()
    address2 = rpc_connection.getnewaddress()
    address3 = rpc_connection.getnewaddress()

    # Mine some blocks
    rpc_connection.generatetoaddress(101, address1)

    # Get the unspent transactions
    unspent = rpc_connection.listunspent()

    # Create two transactions that spend the same coins
    tx1_hex = rpc_connection.createrawtransaction([{"txid": unspent[57]['txid'], "vout": 0}], {address2: 5})
    tx2_hex = rpc_connection.createrawtransaction([{"txid": unspent[57]['txid'], "vout": 0}], {address3: 5})

    fundedtx1_hex = rpc_connection.fundrawtransaction(tx1_hex, {'feeRate': 0.00002})
    fundedtx2_hex = rpc_connection.fundrawtransaction(tx2_hex, {'feeRate': 0.00003})

    # Sign the transactions
    tx1_hex_signed = rpc_connection.signrawtransactionwithwallet(fundedtx1_hex['hex'])
    tx2_hex_signed = rpc_connection.signrawtransactionwithwallet(fundedtx2_hex['hex'])

    # Broadcast the first transaction and mine it into a block
    rpc_connection.sendrawtransaction(tx1_hex_signed['hex'])
    rpc_connection.generatetoaddress(1, address1)
    blockhash_before = rpc_connection.getblockhash(expectedBlockReOrgHeight)

    # Use invalidateblock on the hash from step 4. This will make your node consider the block and its descendants as invalid, and the tip will be the block from step 2.
    rpc_connection.invalidateblock(blockhash_before)
    #rpc_connection.generatetoaddress(101, address1)

    # Broadcast the second transaction and mine it into a longer chain in private
    rpc_connection.sendrawtransaction(tx2_hex_signed['hex'])
    rpc_connection.generatetoaddress(101, address1)

    blockhash_after = rpc_connection.getblockhash(expectedBlockReOrgHeight)

    # Use reconsiderblock on the hash from step 4. This will make your node consider the previously invalidated block as valid again.
    rpc_connection.reconsiderblock(blockhash_before)

    

    if blockhash_before != blockhash_after:
        print("A re-org has occurred.")
    else:
        print("No re-org.")

print(createRe_Org(836))