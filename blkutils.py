from block import Block
from transaction import Transaction
from merkleroot import create_merkle_root
from txutils import generate_coinbase

# Method that calculates the vout's values
def Calculate_block_vouts(self, tx_id):

    for i in range(1,Block._BlockHeight+1):
        if Block._raw_block.get(str(i).encode(),default=None) is None:
            return 0;
        else:
            index=i
            break


    #if there is key-value data in db
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

def getLatestBlock():
    if Block._BlockHeight > 10:
        return Block._BlockChain[9]
    else:
        return Block._BlockChain[Block._BlockHeight-1]


def get_difficulty(index, prev_diff):
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
    
    Block_Size=4
    i=0
    # get tx_set from MemPool greedy
    for key , value in Transaction._MemoryPool.iterator():
        tx_val = json.loads(value)
        txid=tx_val["tx_id"]
        tx_set.append(txid)
        i=i+1
        if i == Block_Size-1:
            break
    output_comm=0
    input_comm=0

    for tx in tx_set:
        output_comm += Caculate_curBlock(tx)
        input_comm += Calculate_mem_vouts(tx) + Calculate_block_vouts(tx)

    commission=input_comm=output_comm
    total_fee += commission

      

    # calculate total commission of tx_set(total_fee)
    # Transaction priority required

    coinbase = generate_coinbase(total_fee)
    tx_set.insert(0, coinbase)

    merkle_root = create_merkle_root(tx_set)
    difficulty = get_difficulty(Block._BlockHeight, previous_block.difficulty)

    return Block(block_index, '0', previous_block.block_hash, merkle_root, difficulty, 0, 0, tx_set)


def create_merkle_root(tx_set):
    num=len(tx_set)
    relist=[]
    if num==1:
        return tx_set[0]
    i=0
    if num %2 ==1:
        tx_set[num]=tx_set[num-1]
        num=num+1
    keccak_hash=keccak.new(digest_bits=256)

    while True:
        keccak_hash.update(tx_set[i].encode('ascii'))
        tmp1=keccak_hash.hexdigest()
        keccak_hash.update(tx_set[i+1].encode('ascii'))
        tmp2=keccak_hash.hexdigest()

        keccak_hash.update((tmp1+tmp2).encode('ascii'))
        relist.append(keccak_hash.hexigest())
        
        i=i+2
        if i >= num:
            break

    create_merkle_root(relist)


    


        


        






#Require block fork management methods
