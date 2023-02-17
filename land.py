import datetime
import hashlib
import json
from flask import Flask, jsonify, request , url_for
from werkzeug.wrappers import response


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_Block(owner='creator', Reg_no='0001',
                          proof=1, previous_hash='0')

        def create_Block(self, owner, Reg_no, proof, previous_hash):
            block = {'owner': owner,
                     'Reg_no': Reg_no,
                     'index': len(self.chain)+1,
                     'timestamp': str(datetime.datetime.now()),
                     'proof': proof,
                     'previous_hash': previous_hash
                     }
            self.chain.append(block)
            return block

            def proof_of_work(self, previous_proof):
                new_proof = 1
                check_proof = False
                while check_proof is False:
                    hash_val = hashlib.sha256(
                        str(new_proof**2 - previous_proof**2).encode()).hexdigest()
                    if hash_val[:4] == '0000':
                        check_proof = True
                    else:
                        new_proof += 1

                        return new_proof

            def hash(self, block):
                encoded_block = json.dumps(block).encode()
                return hashlib.sha256(encoded_block).hexdigest()

            def is_chain_valid(self, chain):
                previous_block = chain[0]
                block_idx = 1

                while block_idx < len(chain):
                    block = chain[block_idx]
                    if block['previous_hash'] != self.hash(previous_block):
                        return False
                        previous_proof = previous_block['proof']
                        proof = block['proof']

                        hash_val = hashlib.sha256(
                            str(proof**2-previous_proof**2).encode()).hexdigest()
                    if hash_val[:4] != '0000':
                        return False
                    previous_block = block
                    block_idx += 1

                    return True

    def get_last_block(self):
        return self.chain[-1]


app = Flask(__name__)



@app.route('/get_chain', method=['SET'])
def get_chain():
    response = {
        'chain': Blockchain.chain,
        'length': len(Blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = Blockchain.is_chain_valid(Blockchain.chain)

    if is_valid:
        response = {'message': 'All good.THe ledger is valid'}
    else:
        response = {'message': 'sir , we have the problem'}

        return jsonify(response), 200

@app.route('/mine_block', method=['POST'])
def mine_block():
    values = request.get_json()
    print(request.form.get['location'])
    required = ['owner', 'Reg_no']

    if not all(k in values for k in required):
        return 'missing values', 400

    owner = values['owner']
    Reg_no = values['Reg_no']
    previous_block = Blockchain.get_last_block()
    previous_proof = previous_block['proof']
    proof = Blockchain.proof_of_work(previous_proof)
    previous_hash = Blockchain.hash(previous_block)
    block = Blockchain.create_block(owner, Reg_no, proof, previous_hash)
    response = {'message': 'record is loaaded'}
    return jsonify(response), 200

app.run(host='1.2.1.1', port=5000, debug=True)
