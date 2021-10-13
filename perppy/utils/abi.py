import json
import importlib_resources

from perppy.utils.singleton import Singleton


class AbiFactory(metaclass=Singleton):
    """
    AbiFactory singleton class is used to
    read ad return abi from json abi files.
    """
    def __init__(self):
        """
        Initiates the AbiFactory singleton class.
        """
        # self.abis_files = importlib_resources.files()
        pass

    def get_contract_abi(self, contract_name: str):
        """
        Get conntract abi for `contract_name`.

        :param contract_name: Name of the contract
        """
        abi_file = importlib_resources.files('perppy.abis').joinpath(f'{contract_name}.json').read_text()
        json_data = json.loads(abi_file)

        return json_data['abi']