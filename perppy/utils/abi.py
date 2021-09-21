import json
import importlib_resources

from perppy.utils.singleton import Singleton


class AbiFactory(metaclass=Singleton):
    def __init__(self):
        # self.abis_files = importlib_resources.files()
        pass

    def get_contract_abi(self, contract_name: str):
        abi_file = importlib_resources.files('perppy.abis').joinpath(f'{contract_name}.json').read_text()
        json_data = json.loads(abi_file)

        return json_data['abi']