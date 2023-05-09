from .nordigen_data_loader import NordigenDataLoader
from .data_loader import DataLoader


def create_data_loader(data_loader_type: str) -> DataLoader:
    """
    Factory function for creating data loaders.

    :param data_loader_type: The type of data loader to create.

    :return: The data loader.
    """
    if data_loader_type == "nordigen":
        return NordigenDataLoader()
    else:
        raise ValueError(f"Data loader type {data_loader_type} not supported.")
