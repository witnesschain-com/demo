import os
import sys
import json
import requests

from eth_account.messages import encode_defunct
from eth_account import Account

class api:
#
	def __init__(self, network, proof_type):
	#
		self.proof_type	= proof_type

		if network == "testnet":
			self.BASE_URL	= "https://" + network + ".witnesschain.com/proof/v1/" + proof_type
		else:
			self.BASE_URL	= "https://" + network + "-playgrounds.infinitywatch.ai/proof/v1/" + proof_type

		self.session = requests.Session()

		if "PRIVATE_KEY" not in os.environ:
			print("===> \033[91mPRIVATE_KEY\033[0m environment variable not found")
			sys.exit(-1)

		self.private_key = os.environ["PRIVATE_KEY"]

		try:
			self.address = Account.from_key(self.private_key).address
		except:
			print("===> Invalid \033[91mPRIVATE_KEY\033[0m")
			sys.exit(-1)
	#

	def sign(self,msg):
	#
		# Create the message hash
		msghash = encode_defunct(text=msg)

		# Sign the message
		signed_message = Account.sign_message(msghash, self.private_key)

		s = signed_message.signature.hex()

		if s.startswith("0x"):
			return signed_message.signature.hex()
		else:
			return "0x" + signed_message.signature.hex()
	#

	def do_post (self, api, body, extra_headers = None):
	#
		headers = {
			"content-type" : "application/json"
		}

		if extra_headers != None:
			for key in extra_headers:
				headers[key] = extra_headers[key]

		print("Sending",self.BASE_URL + "/" +  api, headers)

		r = self.session.post (
			url	= self.BASE_URL + "/" + api,
			data	= body,
			headers = headers
		)

		print(r.headers)

		if r.status_code == 200:
			print("\033[92mSUCCESS\033[0m",r.url)
			print(r.text)
		else:
			print("\033[91mFAILURE\033[0m",r.status_code,r.url)
			print(r.text)
			return None


		j	= json.loads(r.text.encode())
		result	= j["result"]

		return result
	#

	def login (self):
	#
		r = self.do_post (
			"pre-login",
			json.dumps({
				"role"			: "payer",
				"keyType"		: "ethereum",
				"publicKey"		: self.address,
				"clientVersion"		: "9999999999",
				"walletPublicKey"	: {
					"ethereum" : self.address
				}
			})
		)

		signature = self.sign(r["message"])

		r = self.do_post (
			"login",
			json.dumps({
				"signature" : signature
			})
		)

		return r
	#

	def get_balance (self):
	#
		r = self.do_post (
			"my-balance",
			json.dumps({})
		)

		return r
	#

	def get_campaigns (self):
	#
		r = self.do_post (
			"campaigns",
			json.dumps({})
		)

		return r
	#

	def create_campaign (self,campaign_data):
	#
		r = self.do_post (
			"create-campaign",
			json.dumps(campaign_data)
		)

		return r
	#

	def create_apikey (self, name, valid_till_days):
	#
		r = self.do_post (
			"create-apikey",
			json.dumps({
				"name"			: name,
				"valid_till_days"	: valid_till_days
			})
		)

		return r
	#

	def get_all_apikeys (self):
	#
		r = self.do_post (
			"get-all-apikeys",
			"{}"
		)

		return r
	#

	def delete_apikey (self, name):
	#
		r = self.do_post (
			"delete-apikey",
			json.dumps({
				"name" : name
			})
		)

		return r
	#

	def request_challenge (self, prover, num_challengers, challenge_type = None, apikey = None):
	#
		headers = {}

		body = {
			"prover"		: prover,
			"challenge_type"	: challenge_type,
			"num_challengers"	: num_challengers,
		}

		if apikey != None:
			headers['Authorization'] = "Bearer " + apikey

		if challenge_type == None:
			body["challenge_type"] = self.proof_type

		r = self.do_post (
			"challenge-request",
			json.dumps(body),
			headers
		)

		return r
	#

	def challenge_status (self, challenge_id):
	#
		headers = {}

		body = {
			"challenge_id" : challenge_id
		}

		r = self.do_post (
			"challenge-status",
			json.dumps(body),
		)

		return r
	#

#