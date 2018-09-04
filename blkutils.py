from block import Block
from merkleroot import create_merkle_root
from txutils import generate_coinbase, isValid

"""
Add import 
"""
########################################################################################################################
from Crypto.Hash import keccak ## add import
import time
########################################################################################################################

"""
# Method that calculates the vout's values
def Calculate_block_vouts(self, tx_id, index):
    # if there is no key-value data in db
    if RawBlock._raw_block.get(str(index).encode(),default=None) is None:
        return 0

    #if there is key-value data in db
    else:
        total_val=0
        tmpbl_Data=json.loads(RawBlock._raw_block.get(str(index).encode()),default=None)
        tmptx_set=json.loads(tmpbl_Data["tx_set"])
        for i in range(0,len(tmptx_set)):
            tmptx_set_el=json.loads(tmptx_set[i])
            if tmptx_set_el.tx_id == tx_id:
                tmptx_vout=tmptx_set_el.vout
                break
        for i in range(0,len(tmptx_vout)):
            total_val += tmptx_vout.value
        return total_val
"""


def getLatestBlock():
    if Block._BlockHeight > 10:
        return Block._BlockChain[9]
    else:
        return Block._BlockChain[Block._BlockHeight - 1]


def get_difficulty(index, prev_diff):

    '''
    print("Get Difficulty")
    print(str(index))
    print(str(prev_diff))
    print("End set difficulty")
    '''

    if index > 6:
        if index > 9:
            elapsed = Block._BlockChain[9].timestamp - Block._BlockChain[3].timestamp
        else:
            elapsed = Block._BlockChain[index - 1].timestamp - Block._BlockChain[index - 6].timestamp
        return int(elapsed / 40 * prev_diff)
    else:
        return 0x00008fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff


def get_candidateblock():
    # warning for poinint class var
    block_index = Block._BlockHeight
    previous_block = getLatestBlock()

    tx_set = []
    total_fee = 12.5

    # get tx_set from MemPool greedy
    # calculate total commission of tx_set(total_fee)
    # Transaction priority required

    coinbase = generate_coinbase(total_fee)
    tx_set.insert(0, coinbase)

    merkle_root = create_merkle_root(tx_set)
    difficulty = get_difficulty(Block._BlockHeight, previous_block.difficulty)

    return Block(block_index, '0', previous_block.block_hash, merkle_root, difficulty, 0, 0, tx_set)


# Require block fork management methods

# Block validation
########################################################################################################################
def Block_Validation(index, block_hash, previous_block, merkle_root, difficulty, timestamp, nonce, tx_set, prev_diff):
    """
       Key of DB       : str(index).encode()
        Args:
        index           : int
        block_hash      : string
        previous_block  : string
        merkle_root     : string
        difficulty      : int
        timestamp       : int
        nonce           : int
        tx_set          : list[Transaction()]
        """
    # Block Format check
    ####################################################################################################################
    if index == None or \
            block_hash == None or \
            previous_block == None or \
            merkle_root == None or \
            difficulty == None or \
            timestamp == None or \
            nonce == None or \
            tx_set == None:
        print("Format Error")
        return False

    # Block Difficulty check
    ####################################################################################################################
    #print("Block Validation" + str(index) + "##################################################################")
    tmp_diff = get_difficulty(index, prev_diff)
    if tmp_diff != difficulty :
        print("Difficulty Value")
        '''
        print(str(index))
        print(str(tmp_diff))
        print(str(difficulty))
        '''
        return False

    # Nonce value check
    ####################################################################################################################
    hash_input = str(previous_block) + \
                str(merkle_root) + \
                str(difficulty) + \
                str(nonce)

    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(hash_input.encode('ascii'))

    if block_hash != keccak_hash.hexdigest():
        print("Nonce value")
        return False

    # 2 hours timestamp
    ####################################################################################################################
    current_time = int(time.time())
    elapsed_time = int(current_time - timestamp)
    if elapsed_time > 7200 :
        print("Timestamp")
        return False

    # Is it coinbase transaction?
    ####################################################################################################################
    coinbase_tx = tx_set[0]
    if coinbase_tx.in_num != 0 :
        print("Coinbase transaction")
        return False

    # Is it all transaction are right?
    # transaction valid is not make
    ####################################################################################################################
    """
    for tx in tx_set:
        if isValid(tx) != True :
            print("Transaction right")
            return False
    """
    max_num = 5
    # length of list
    ####################################################################################################################
    if len(tx_set) > max_num :
        print("Tx num")
        return False

    return True