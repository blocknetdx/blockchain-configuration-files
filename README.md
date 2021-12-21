# Blocknet's Blockchain Configuration Files
This repository contains:
 * The blockchain configuration files needed for trustless exchange(XBridge) on the Blocknet Protocol;
 * An overview of the file structure and contents;
 * Directions on how to create configuration files from scratch;
 * Directions on how to setup configuration files for use of the Blocknet Protocol;
 * Directions on how to test a blockchain for compatibility with XBridge;

[Website](https://blocknet.co) | [API](https://api.blocknet.co) | [Documentation](https://docs.blocknet.co) | [Discord](https://discord.gg/2e6s7H8)
-------------------------------|----------------------------------------------|--------------------------------------|--------------------------------------


Table of contents
--------------------------------------
<!-- UPDATE with   `doctoc .`   in the README.md directory -->
<!-- doctoc repo: https://github.com/thlorenz/doctoc/blob/master/README.md -->
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Blocknet's Blockchain Configuration Files](#blocknets-blockchain-configuration-files)
  - [Table of contents](#table-of-contents)
  - [Major update to workflow](#major-update-to-workflow)
  - [Configuration File Overview](#configuration-file-overview)
    - [Manifest File](#manifest-file)
    - [XBridge and Wallet Configuration Files](#xbridge-and-wallet-configuration-files)
    - [XBridge Configuration Files](#xbridge-configuration-files)
    - [Wallet Configuration Files](#wallet-configuration-files)
  - [Creating Configuration Files](#creating-configuration-files)
    - [Creating the coin.base.j2 file](#creating-the-coinbasej2-file)
  - [Setup Servicenode or Trading Node Configuration Files](#setup-servicenode-or-trading-node-configuration-files)
    - [Setup xbridge.conf](#setup-xbridgeconf)
    - [Setup Wallet Files](#setup-wallet-files)
  - [Testing a Blockchain for Compatibility](#testing-a-blockchain-for-compatibility)
    - [Successful Exchange](#successful-exchange)
  - [Contributing](#contributing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Major update to workflow
------------------------
The coin update and addition process has been overhauled as of November 2021. New documentation is being prepared to explain the workflow in detail. For now, abbreviated documentation is available in [autobuild/workflow.md](autobuild/workflow.md).

The old documentation is preserved below as reference to the configuration information (which is mostly unchanged except in location).
 

Configuration File Overview
--------------------------------------
The data structure of the configuration files is designed to accommodate for versioning. There are several data sets as follows:

* `manifest-latest.json` - Contains the latest official master data and versioning reference of each blockchain.
* `autobuild/configs/\<coin\>.base.j2` - Contains the Jinja base template file for each blockchain.
* `autobuild/templates/wallet.conf.j2` - Contains the Jinja base wallet template file.
* `autobuild/templates/xbridge.conf.j2` - Contains the Jinja base XBridge template file.
* `wallet-confs` - Contains the versioned wallet configuration files for each blockchain generated from the manifest, config base and wallet template files.
* `xbridge-confs` - Contains the versioned XBridge configuration files for each blockchain generated from the manifest, config base and xbridge template files.
* `manifests` - Contains archived manifest versions that align with Blocknet wallet releases.
* `manifest.json` - Deprecated.


### Manifest File
The `manifest-latest.json` contains an array of objects with each object containing versioning information for each supported blockchain. The format of each object is as follows:
```
{
    "blockchain": "",
    "ticker": "",
    "ver_id": "",
    "ver_name": "",
    "conf_name": "",
    "dir_name_linux": "",
    "dir_name_mac": "",
    "dir_name_win": "",
    "repo_url": "",
    "versions": [],
    "xbridge_conf": "",
    "wallet_conf": ""
}
```

Key               | Description
------------------|------------------
blockchain      | The name of the blockchain: *Blocknet, Dogecoin, Syscoin, etc*. This is user-facing, case-sensitive, and should remain consistent across all version groups for this blockchain.
ticker          | The abbreviation used to represent this blockchain on exchanges: *BLOCK, DOGE, SYS, etc*. Use all uppercase letters.
ver_id          | This ID must be unique, not change, and is case-sensitive. The format used is the wallet's configuration file name (without the extension), followed by a double-hyphen, then the initial wallet version added to this compatibility versioning group: *blocknet--v4.2.0, dogecoin--v1.10.0-dogeparty, syscoin--3.0.5.0, etc*.
ver_name        | User viewable and user friendly name for the blockchain version group. This can be changed/renamed and is used to indicate the blockchain versioning group. For example, Blocknet's current `ver_name` is *Blocknet v4*. If a new version group was created for the next wallet version release, the `ver_name` could be changed to *Blocknet v4-v4.4.0*.
conf_name       | The name of the wallet's configuration file (with the extension): *blocknet.conf, dogecoin.conf, syscoin.conf, etc*. This is case-sensitive and should be written exactly as it is in the file name.
dir_name_linux  | This is the name of the blockchain's folder in the data directory: *blocknet, dogecoin, syscoincore, etc*. This is case-sensitive and should be written exactly as it is in the folder name.
dir_name_mac    | This is the name of the blockchain's folder in the data directory: *Blocknet, Dogecoin, SyscoinCore, etc*. This is case-sensitive and should be written exactly as it is in the folder name.
dir_name_win    | This is the name of the blockchain's folder in the data directory: *Blocknet, Dogecoin, SyscoinCore, etc*. This is case-sensitive and should be written exactly as it is in the folder name.
repo_url        | This is the URL of the wallet’s Github repository: *[https://github.com/BlocknetDX/blocknet](https://github.com/BlocknetDX/blocknet)*, *[https://github.com/dogecoin/dogecoin](https://github.com/dogecoin/dogecoin)*, *[https://github.com/syscoin/syscoin](https://github.com/syscoin/syscoin), etc*. Do not include trailing slashes.
versions        | This is an array of wallet versions compatible with the referenced `xbridge_conf` and `wallet_conf` configuration files. The versioning used is case-sensitive and must be exactly the same as tagged in the Github repo for each release: *[v4.3.0](https://github.com/BlocknetDX/BlockDX/releases/tag/v4.3.0) (Blocknet), [v1.10.0-dogeparty](https://github.com/dogecoin/dogecoin/releases/tag/v1.10.0-dogeparty) (Dogecoin), [3.0.5.0](https://github.com/syscoin/syscoin/releases/tag/3.0.5.0) (Syscoin), etc*.
xbridge_conf    | This is the name of the XBridge configuration file within the `xbridge-confs` folder. The title of this file should be the same as the `ver_id` in all lowercase.
wallet_conf     | This is the name of the wallet configuration file within the `wallet-confs` folder. The title of this file should be the same as the `ver_id` in all lowercase.

**Example Manifest Object**
```
  {
    "blockchain": "Blocknet",
    "ticker": "BLOCK",
    "ver_id": "blocknet--v4.2.0",
    "ver_name": "Blocknet v4",
    "conf_name": "blocknet.conf",
    "dir_name_linux": "blocknet",
    "dir_name_mac": "Blocknet",
    "dir_name_win": "Blocknet",
    "repo_url": "https://github.com/blocknetdx/blocknet",
    "versions": [
      "v4.2.0",
      "v4.3.0",
      "v4.3.1",
      "v4.3.2",
      "v4.3.3"
    ],
    "xbridge_conf": "blocknet--v4.2.0.conf",
    "wallet_conf": "blocknet--v4.2.0.conf"
  }
```

### XBridge and Wallet Configuration Files
These were formerly primary configuration objects but are now derived from the 
Jinja `<coin>.base.j2` file and XBridge and wallet templates. The format and examples of each file are shown below, followed by the Jinja file from which they are generated by 
the [app.py](autobuild/app.py) Python script. 

### XBridge Configuration Files
The XBridge configuration files are versioned for each blockchain using the `manifest` file as a key. The format of each file is as follows:
```
[TICKER]                        # Ticker used to represent the blockchain on exchanges;
Title=                          # Name of the blockchain with spaces removed;
Address=                        # Deprecated, can be left blank;
Ip=127.0.0.1                    # Client IP, localhost or IP of machine(VM/VPS);
Port=                           # Wallet RPC port listed in the wallet conf;
Username=                       # Wallet RPC username created in the wallet conf;
Password=                       # Wallet RPC password created in the wallet conf;
AddressPrefix=                  # Decoded public address, Base58 > HEX(0,2) > decimal;
ScriptPrefix=                   # Decoded P2SH address, Base58 > HEX(0,2) > decimal;
SecretPrefix=                   # Decoded private key, Base58 > HEX(0,2) > decimal;
COIN=                           # Coin precision defined in source code COIN =;
MinimumAmount=0                 # Minimum exchange amount, leave value set to '0';
TxVersion=                      # The `version` value found in raw transactions;
DustAmount=0                    # Leave value set to '0';
CreateTxMethod=                 # Type of transaction method: BTC, SYS, DGB, etc;
GetNewKeySupported=true         # Leave value set to 'true';
ImportWithNoScanSupported=true  # Leave value set to 'true';
MinTxFee=0                      # Leave value set to '0', adjust fee in 'FeePerByte';
BlockTime=                      # The blockchain's block time in seconds;
FeePerByte=                     # The fee per byte to send a transaction;
Confirmations=0                 # Number of confirmations to complete exchange;
```
**Example XBridge File**

*File Name*: `blocknet--v4.2.0.conf`
```
[BLOCK]
Title=Blocknet
Address=
Ip=127.0.0.1
Port=41414
Username=
Password=
AddressPrefix=26
ScriptPrefix=28
SecretPrefix=154
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=true
ImportWithNoScanSupported=true
MinTxFee=10000
BlockTime=60
FeePerByte=20
Confirmations=0
```
The file name should match the value of the `manifest` file's `xbridge_conf` key for the version group that these XBridge values pertain to.


### Wallet Configuration Files
The wallet configuration files are versioned for each blockchain using the `manifest-latest.json` file as a key. The format of each file is as follows:
```
server=1                        # Enable/disable command line and JSON-RPC commands;
listen=1                        # Enable/disable peer connections;
rpcuser=                        # Custom username, must match in xbridge.conf;
rpcpassword=                    # Custom password, must match in xbridge.conf;
rpcallowip=127.0.0.1            # Client IP, localhost or IP of machine(VM/VPS);
port=                           # Port to listen for connections on;
rpcport=                        # Port to listen for JSON-RPC connections on;
txindex=1                       # Transaction index is required for getrawtransaction RPC call
addresstype=legacy              # Required for Segwit activated blockchain;
changetype=legacy               # Required for Segwit activated blockchain;
deprecatedrpc=                  # Custom content depending on the coin; 
```
**Example Wallet File**

*File Name*: `blocknet--v4.2.0.conf`
```
server=1
listen=1
rpcuser=
rpcpassword=
rpcallowip=0.0.0.0/0
port=41412
rpcport=41414
txindex=1
```
The file name should match the value of the `manifest` file's `wallet_conf` key for the version group that these XBridge values pertain to.



Creating Configuration Files
--------------------------------------
You need to create a `<coin>.base.j2` template in the autobuild/configs directory. It is essentially a concatenation of the XBridge and wallet configuration files with some special treatment for:
* substitution variables in the automation workflows
* supporting multiple versions
* certain wallet directives

In the following explanation, Blocknet wallet [v4.3.0](https://github.com/BlocknetDX/BlockDX/releases/tag/v4.3.0) will be used as an example throughout the process of creating a Jinja template configuration file. The name this file is saved as should be the same as the concatenation of the lowercase version of the `ticker` and `.base.j2`. Blocknet example: `"ticker": "BLOCK"` yields `block.base.j2`. The current Blocknet block.base.j2 looks like this:

```
{
    "BLOCK": {
        "Title": "Blocknet",
        "Address": "",
        "Ip": "127.0.0.1",
        "rpcPort": "{{ rpcPort|default(41414)}}",
        "p2pPort": "{{ p2pPort|default(41412)}}",
        "Username": "{{ rpcusername }}",
        "Password": "{{ rpcpassword }}",
        "AddressPrefix": "26",
        "ScriptPrefix": "28",
        "SecretPrefix": "154",
        "COIN": "100000000",
        "MinimumAmount": "0",
        "DustAmount": "0",
        "CreateTxMethod": "BTC",
        "GetNewKeySupported": "true",
        "ImportWithNoScanSupported": "true",
        "MinTxFee": "10000",
        "BlockTime": "60",
        "TxVersion": "1",
        "FeePerByte": "20",
        "Confirmations": "0",
        "versions": {
            "v4.2.0": {
                "legacy": false,
                "deprecatedrpc": false,
                "xbridge_conf": "blocknet--v4.2.0.conf",
                "wallet_conf": "blocknet--v4.2.0.conf",
                "GetNewKeySupported": false
            },
            "v4.3.0": {
                "legacy": false,
                "deprecatedrpc": false,
                "xbridge_conf": "blocknet--v4.2.0.conf",
                "wallet_conf": "blocknet--v4.2.0.conf",
                "GetNewKeySupported": false
            },
            "v4.3.1": {
                "legacy": false,
                "deprecatedrpc": false,
                "xbridge_conf": "blocknet--v4.2.0.conf",
                "wallet_conf": "blocknet--v4.2.0.conf",
                "GetNewKeySupported": false
            },
            "v4.3.2": {
                "legacy": false,
                "deprecatedrpc": false,
                "xbridge_conf": "blocknet--v4.2.0.conf",
                "wallet_conf": "blocknet--v4.2.0.conf",
                "GetNewKeySupported": false
            },
            "v4.3.3": {
                "legacy": false,
                "deprecatedrpc": false,
                "xbridge_conf": "blocknet--v4.2.0.conf",
                "wallet_conf": "blocknet--v4.2.0.conf",
                "GetNewKeySupported": false
            }
        }
    }
}
```


### Creating the coin.base.j2 file
The file is a JSON format list starting with the coin name
```
{
  "<coin>": {
```

The name is followed by the fields which comprise the XBridge config fragment for the coin.

Directive                                | Comment
-----------------------------------------|----------------
"Title": "Blocknet",                     | The title is the name of the blockchain with the spaces removed. For Blocknet it's simply `Blocknet`.
"Address": "",                           | This address setting is not currently used and can be left blank.
"IP": "127.0.0.1",                       | This is the IP of the client wallet. Default should be set to `127.0.0.1` and if needed, can be changed by the end user when setting up the configuration files for the given environment.
"Port": "{{ rpcPort\|default(41414)}}",  | This is a placeholder for the RPC port for the wallet and a default value. Most Qt wallets will list a default suggested RPC port under Help > Command-line options > Server Options. In here will be a line similar to the following: <br>```Listen for JSON-RPC connections on <port> (default: 41414 or testnet: 41419)```<br>As shown, the RPC port is `41414`. If this port is used by another blockchain, an arbitrary available port may be used.
"Username": "{{ rpcusername }}",         | Substitution value to be supplied by workflow automation.
"Password": "{{ rpcpassword }}",         | Substitution value to be supplied by workflow automation.
"AddressPrefix": "26",                   | There are multiple steps to obtain the address prefix: <br>1) Copy a public address, ie: *BUE65eaeh3NZwNm2p5yKSstxteYvShi4yu*; <br>2) Visit this online Base58 tool: [lenschulwitz.com](http://lenschulwitz.com/base58); <br>3) Paste the address in the Bitcoin Address Base58 Decoder input and decode the address to a HEX string: *1A04CDFFBA976B79C0D25F06C56151FEF6A2A3156BD60F2398*; <br>4) Copy the first 2 characters of the HEX string: *1A*; <br>5) Visit this online HEX converter tool: [binaryhexconverter.com](https://www.binaryhexconverter.com/hex-to-decimal-converter); <br>6) Paste the 2 characters in the HEX value input and convert it to decimal value: *26*; <br>7) The address prefix is `26`;
"ScriptPrefix": "28",                    | The script prefix follows the same process as the address prefix, but with a P2SH public address instead of a regular public address. Follow these steps to obtain the P2SH public address and prefix: <br>1) Open the wallet's debug console; <br>2) Type `validateaddress <pub address>`, replacing `<pub address>` with a public address, and press *Enter*; <br>3) From the JSON output, copy the value of `"pubkey"`; <br>4) In the console type `decodescript <pubkey output>`, replacing `<pubkey output>` with the value copied in the previous step, and press *Enter*; <br>5) From the JSON output, copy the value of `"p2sh"`, which is the P2SH public address; <br>6) Perform the steps provided for *AddressPrefix* using this P2SH public address;
"SecretPrefix": "154",                   | The secret prefix follows the same process as the address prefix also, but with a private key instead of a public address. Follow these steps to obtain the private key and prefix: <br>1) Open the wallet's debug console; <br>2) Type `dumpprivkey <pub address>`, replacing `<pub address>` with a public address, and press *Enter*; <br>3) Copy the console output, which is the private key; <br>4) Perform the steps provided for *AddressPrefix* using this private key;
"COIN": "100000000",                     | Coin precision determined in source code. `COIN=100000000` = `1.00000000` & `COIN=1000000` = `1.000000`
"MinimumAmount": "0",                    | This is the minimum exchange amount. Keep this value set to `0`.
"TxVersion": "1",                        | The transaction version is the value of `"version"` in raw transactions. There are two ways this value can be found. <br>**Method 1**:<br>1) Check if the blockchain explorer has raw transaction JSON in the transaction detail pages. For Blocknet, this can be found in [the explorer *Raw Transaction* tab](https://chainz.cryptoid.info/block/tx.dws?274413.htm). <br>2) In the JSON, the version can be found as the second key-value pair: `"version": 1`. <br>**Method 2**<br>1) Alternatively, the transaction version number can be found using a wallet's debug console. <br>2) Open the wallet's debug console; <br>• Type `getrawtransaction <tx id>`, replacing `<tx id>` with a transaction ID(hash): *060f838a8df0e089350834c1ef541418f2f9e1bca952bdcc0f4dbe64af2188c6*; <br>3) Copy the console output, which is a HEX string that needs to be decoded; <br>4) In the console type `decoderawtransaction <hex string>`, replacing `<hex string>` with the outputted HEX string; <br>5) In the JSON output, the version can be found as the second key-value pair: `"version": 1`.
"DustAmount": "0",                       | This specifies the dust amount threshold. Keep this value set to `0`.
"CreateTxMethod": "BTC",                 | The transaction method refers to the type of transaction procedure that is used for the blockchain. The different types can be found by looking at the variations of `xbridgewalletconnector` files in the [Blocknet Github](https://github.com/BlocknetDX/BlockDX/tree/master/src/xbridge), such as `BTC`, `DGB`, or `SYS`. *Example:* `xbridgewalletconnectordgb.cpp`;
"GetNewKeySupported": "true",            | Keep this value set to `true`.
"ImportWithNoScanSupported": "true",     | Keep this value set to `true`.
"MinTxFee": "0",                         | This can be used to set a minimum transaction fee, but most of the time it works best to keep this value set to `0` and instead adjust the value of `FeePerByte`.
"BlockTime": "60",                       | This is the blockchain's block time in seconds, which is usually readily available. For Blocknet it's 60 seconds. If this is not available then a close estimate can be calculated in two ways: <br>**Method One:**<br>1) Visit the explorer and expand the list to view the last 500 blocks. <br>2) Record how long ago the time of the 500th block was, or the difference in time between the most recent block and the 500th block. 3) The block time would be the time in seconds divided by 500: `BlockTime` = (time in seconds)/500; <br>**Method Two:**<br>1) Open the wallet's debug console; <br>2) Type `getmininginfo` and press *Enter*; <br>3) From the JSON output, copy the values of `difficulty` and `networkhashps`; <br>4) The block time would be 2^32 times the difficulty, divided by the network hashrate: `BlockTime` = 2^32 * `difficulty` / `networkhashps`;
"FeePerByte": "20",                      | The fee per byte is how much to charge per byte for an exchange. This can be calculated by looking in the wallet send function for the recommended fee per byte and then multiplying it by 2-2.5 since there's 2 transactions that take place in an exchange: one transaction from one party's address to the P2SH address and then a second transaction from the P2SH address to the counterparty's address.
"Confirmations": "0",                    | Confirmations is the minimum amount of transaction confirmations required until funds are spent and an exchange is complete. Requiring more confirmations increases the time and exchange take but makes it more secure as the network verifies the data. By default, the number of confirmations required is set to `0`.  
"versions": {}                           | Contains a list of configuration sections for each supported version in this `ver_id`. Each section may have different values depending on the coin version. The format of each section is shown below

Directive                                | Comment
-----------------------------------------|----------------
"vx.y.z": {                              | A specific version number
  "legacy": false,                       | BlockDX does not yet support SegWit because SegWit addresses start with the same prefix as P2SH addresses. This key should be set to `true` for coins which support SegWit. In this case the wallet config will be generated with the following directives which instruct the wallet to use legacy (non-P2SH) addresses.<br>addresstype=legacy<br>changetype=legacy
  "deprecatedrpc": false,                  | Some coin wallets have deprecated or changed the output format of some RPC replies. It may be possible (and perhaps necessary for correct XBridge operation) to restore the old behaviour. Setting this value to `true` will generate the wallet config with the following directive<br>deprecatedrpc=addresses<br>Alternatively, freeform text may be specified in which case the wallet config will be generated with a line containing<br>deprecatedrpc=\<your freeform text\><br>For example, Digibyte requires<br>"deprecatedrpc": "signrawtransaction"
  "xbridge_conf": "blocknet--v4.2.0.conf",| The name of the xbridge file to be generated in repo/xbridge-confs.
  "wallet_conf": "blocknet--v4.2.0.conf", | The name of the wallet file to be generated in repo/wallet-confs.
  "GetNewKeySupported": false             | Leave this set to false


The file finishes with closing parentheses
```
  }
}
```


Setup Servicenode or Trading Node Configuration Files
--------------------------------------
The XBridge and wallet configuration files in this repo are named and organized for versioning. In order to properly set up an environment for use with the Blocknet Protocol's XBridge component, additional steps must be taken. The following instructions describe the legacy/manual approach. We are migrating to a more automated Docker-based approach and that workflow is described in the [Blocknet Doc hub](https://docs.blocknet.co/service-nodes/setup/)


### Setup xbridge.conf
The `xbridge.conf` is a single file includes a main heading, followed by a newline, followed by the contents of all the individual XBridge configuration file of any blockchain being used with each one separated by a newline.

**Heading Format:**

```
[MAIN]
ExchangeWallets=
```
* The heading must be at the top of the file. 
* The leading line `[MAIN]` does not change.
* The `ExchangeWallets=` setting is used to list the blockchains to be supported. In other words, any blockchain that will be used in an exchange must be listed here. If running a Service Node, only the blockchains that the node will support should be listed here. The values taken are the blockchain `[TICKER]` values from the individual XBridge configuration file. 

**Heading Example:**

```
[MAIN]
ExchangeWallets=BTC,SYS,BLOCK,DGB,QTUM,DASH,XZC,BITG,LTC,DOGE,PIVX,XSN,MONA,VIA,LBC
```

After the heading, the contents of the individual XBridge configuration files of the blockchains listed under `ExchangeWallets` are listed. To find the proper XBridge settings for each blockchain, first find the version group in the `manifest` file for each blockchain that has the wallet version to be used listed in the `"versions"` array (if a version is not listed then it is not yet supported). Copy the contents of each file and paste it into the `xbridge.conf` file. For an example of what a complete and properly formatted `xbridge.conf` file looks like, take a look at the `example-xbridge.conf` file in this repo.

Make sure to update the following for each configuration entry:

Setting                         | Procedure
--------------------------------|----------------
IP=127.0.0.1                    | This is the IP of the client wallet and must be the same as the value for `rpcallowip` in the wallet configuration file. In most cases this can be left as localhost `127.0.0.1`, but may need an another IP if using a VM, VPS, or some other non local setup.
Username=Blockhead              | The username is made up and the value must be the same as created in the wallet configuration file.
Password=fa506e4a01a7           | The password is made up and the value must be the same as created in the wallet configuration file.


### Setup Wallet Files
Each blockchain wallet installation has a configuration file; for Blocknet it is `blocknet.conf`. These contents are to be replaced by the contents of the wallet configuration file referenced in the respective `manifest-latest.json` version group. To find the proper wallet configuration for each blockchain, first find the version group in the `manifest-latest.json` file for each blockchain that has the wallet version to be used listed in the `"versions"` array (if a version is not listed then it is not yet supported). Copy the contents of each referenced wallet configuration file and paste it into the configuration file of the downloaded wallet.

Make sure to update the following for each configuration entry:

Setting                         | Procedure
--------------------------------|----------------
rpcallowip=127.0.0.1            | This is the IP of the client wallet and must be the same as the value for `IP` in the `xbridge.conf` entry for this blockchain. In most cases this can be left as localhost `127.0.0.1`, but may need an another IP if using a VM, VPS, or some other non local setup.
rpcuser=Blockhead               | The username is made up and the value must be the same as created in the `xbridge.conf` entry for this blockchain.
rpcpassword=fa506e4a01a7        | The password is made up and the value must be the same as created in the `xbridge.conf` entry for this blockchain.


Testing a Blockchain for Compatibility
--------------------------------------
To attempt an exchange to test compatibility, the following will be needed:

* A small amount above dust value of the blockchain's token, Blocknet's token(BLOCK) for the exchange network fee, and token of a compatible blockchain to trade against, which can also be BLOCK. Depending on the token's unit value, $1-3 USD should work fine.
* Run the full nodes for each of the blockchains being tested on a testnet Service Node with the composed configuration files. Contact a contributor for tBLOCK or see if the chains can be added to existing testnet Service Nodes.
* Two instances of each blockchain used in testing must be run, with each having the respective configuration files. Exchanges cannot be taken by the client that created them.
* Make sure `debug=1` is set in the `blocknet.conf` file to receive full debug logs if there's an issue.

Once the test environment is ready, create an order and conduct a loop exchange by taking the order that was created with the other set of clients. The exchange will either be successful or present errors in the debug log. 


### Successful Exchange
If the exchange is successful, a commit should be made to the respective configuration files. There are a few variations of scenarios:

*New wallet version, existing blockchain, existing configurations, existing version group:*<br>
If a successful exchange was confirmed for a new wallet version using the same `xbridge_conf` and `wallet_conf` listed under a single existing `manifest` version group, then all that is needed is to update that version group `versions` array with the new wallet version as is listed in the tag of the Github release.

*New wallet version, existing blockchain, existing configurations, new version group:*<br>
If a new wallet version is successful using `xbridge_conf` and `wallet_conf` from two different `manifest` version groups, then a new version group must be created. This new version group would have this new wallet as the only version listed under `versions`, as is listed in the tag of the Github release, with a new `ver_id`, the respective XBridge and wallet configuration files used listed for `xbridge_conf` and `wallet_conf`, and any other changes that may be required.

*New wallet version, existing blockchain, new configurations, new version group:*<br>
If a new wallet version is successful using a newly generated XBridge or wallet configuration file, then a new `manifest` version group must be created as well as the new configuration file. This new version group would have this new wallet as the only version listed under `versions`, as is listed in the tag of the Github release, with a new `ver_id`, the respective XBridge and wallet configuration files used listed for `xbridge_conf` and `wallet_conf`, and any other changes that may be required. 

*New blockchain, new configurations, new version group:*<br>
If a successful exchange was confirmed for a new blockchain, then a new `manifest` version group must be created as well as the new configuration files.


Contributing
--------------------------------------
Want to help build the internet of blockchains? Check out our [contributing documentation](https://github.com/blocknetdx/blocknet/blob/master/CONTRIBUTING.md).

