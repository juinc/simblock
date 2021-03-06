from .utils import sort_dict

class Account():
    empty_data = {
        "balance": 0,
        "nonce": 0,
        "code": "",
        "storage": {}
    }

    def __init__(self, address="", env=None):
        if not env:
            raise ValueError("Argument 'env' is not provided.")

        self.address = address
        self.db = env.state_db

        # Check if the account exists
        try:
            self.data
        except KeyError:
            self.db.put(self.address, sort_dict((dict(self.empty_data))))

    @property
    def data(self):
        return self.db.get(self.address)

    def set_data(self, data):
        for key in data:
            if key == "balance":
                self.set_balance(data[key])
            if key == "nonce":
                self.set_nonce(data[key])

    def set_balance(self, value):
        self.data["balance"] = value

    def set_code(self, value):
        self.data["code"] = value

    def set_nonce(self, value):
        self.data["nonce"] = value

    def set_storage(self, value):
        self.data["storage"] = value
