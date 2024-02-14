# Transaction fees and Re-org simulation

In this repo we create transaction with specific transaction fees and fee rates. I also simulate a reorg using regtest.

## Here are a few things to note when running: (transaction-fee-exercise)

1. To connect to your regtest node, please update the url to your regtest url. also change the name and password. Here

       rpc_connection = AuthServiceProxy("http://%s:%s@localhost:18443" % ("youruser", "yourpassword"))

2. Give a txId has input. (give a txId that has funds) and also provide a valid address that exist on your regtest as output

       output_address = "your-output-address"
       input = [{"txid": "your-input-txid", "vout": 0}]

3. (Optional) you can decide to change the amounts and fee rates you want

         amount = 0.001  # Amount to send (in BTC)
         fee_rates = [0.00002, 0.0001, 0.00015]

## Here are a few things to note when running: (re-org)

1. To connect to your regtest node, please update the url to your regtest url. also change the name and password. Here

       rpc_connection = AuthServiceProxy("http://%s:%s@localhost:18443" % ("youruser", "yourpassword"))

2. You can generate new addresses or use existing ones. Here I generate new ones
   ### Get some addresses
         address1 = rpc_connection.getnewaddress()
         address2 = rpc_connection.getnewaddress()
         address3 = rpc_connection.getnewaddress()
3. Get a list of utxos from your regtest and then select which ones you want to use to create a transaction. I have over 100 unspent transactions. I chose index 57 for input and a reasonable amount to spend for out put
   
         tx1_hex = rpc_connection.createrawtransaction([{"txid": unspent[57]['txid'], "vout": 0}], {address2: 5})
         tx2_hex = rpc_connection.createrawtransaction([{"txid": unspent[57]['txid'], "vout": 0}], {address3: 5})
