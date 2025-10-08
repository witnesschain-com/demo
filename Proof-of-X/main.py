
from witnesschain import api

# Initialize the WitnessChain client
wtns_client = api("mainnet","pol")

# Login to the WitnessChain
wtns_client.login()

watchtower_address = "IPv4/0x939744500de04b4e2d5d68d233617a5ac6968aa0"

proof_type = "pol"


# Request a challenge
response = wtns_client.request_challenge(watchtower_address, 1, proof_type)

# Print the response for challenge request
print(response)

# Get the challenge status
response = wtns_client.challenge_status(response["challenge_id"])

# Print the response for challenge status
print(response)
