# gestionnaire-blockchain

il doit aussi y avoir un fichier "blockchain" contenant des json sous ce format:

{
	"block": {
		"header": {
			"version": 0,
			"flags": [
				"a","b","c"
			],
			"hashPrevBlock": "",
			"hashTransactions": "",
			"timestamp": 0,
			"nonce": 42
		},
		"transactions": []
	},
	"hash": "1",
	"chain_length": 1
}
