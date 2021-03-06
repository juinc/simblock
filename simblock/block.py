from .utils import sha3_256, simple_encode

class Block():
    def __init__(self, header=None, transactions=None):
        if not header:
            raise ValueError("Argument 'header' is not provided.")
        self.header = header
        self.transactions = transactions or []

        # Flag to indicate if the block is a candidate
        self._is_candidate = False

    def from_prevstate(self, state=None, timestamp=None):
        if not state:
            raise ValueError("Argument 'state' is not provided.")

        prev_header = state.prev_headers[0]
        next_header = {
            "number": prev_header.number + 1,
            "timestamp": timestamp or prev_header.timestamp + 1,
            "prevhash": prev_header.hash,
            "difficulty": prev_header.difficulty,
            "nonce": ""
        }

        self.header.number = next_header["number"]
        self.header.timestamp = next_header["timestamp"]
        self.header.prevhash = next_header["prevhash"]
        self.header.difficulty = next_header["difficulty"]
        self.header.nonce = next_header["nonce"]

        return self

    def make_roots(self, state):
        self.header.state_root = state.root_hash
        self.header.tx_root = sha3_256(simple_encode([dict(tx) for tx in self.transactions]))

        # Mark the block as a candidate
        self._is_candidate = True

    @property
    def is_candidate(self):
        return self._is_candidate

    def mine(self, start_nonce=0, max_nonce=2**64):
        """
        Simple proof-of-work algorithm
        """

        # Check if the block is a candidate
        assert self.is_candidate, "Block should be a candidate in order to perform pow mining."

        # calculate the difficulty target
        target = (2**256 // self.header.difficulty) - 1
        block_hash = self.header.hash

        for nonce in range(max_nonce):
            hash_result = sha3_256(block_hash + bytes(nonce))

            # check if this is a valid result, below the target
            num = int.from_bytes(hash_result, byteorder="big")
            if num < target:
                self.header.nonce = nonce
                return nonce

        return None

    def validate(self):
        return True

    def verify(self):
        return True

    def __iter__(self):
        return iter([
            ("header", dict(self.header)),
            ("transactions", [dict(tx) for tx in self.transactions])
        ])
