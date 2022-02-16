from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.model import EnergyComponentType
from tests.utils import data_generator as data_gen
from tests.utils.assertions import assert_energy_component


def test_create_energy_conversion(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy conversion.
    """
    create_request = data_gen.random_energy_conversion_create(db)
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK

    created_conversion = response.json()
    assert_energy_component(created_conversion["component"], create_request, EnergyComponentType.CONVERSION)
    assert created_conversion["commodity_unit"]["name"] == create_request.commodity_unit


def test_create_existing_energy_conversion(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a existing energy conversion.
    """
    create_request = data_gen.random_energy_conversion_create(db)
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_energy_conversion_unknown_dataset(client: TestClient, normal_user_headers: Dict[str, str], db: Session):
    """
    Test creating a energy conversion.
    """
    create_request = data_gen.random_energy_conversion_create(db)
    create_request.ref_dataset = 132456  # ungültige Anfrage
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_energy_conversion_unknown_commodity(client: TestClient, normal_user_headers: Dict[str, str],
                                                    db: Session):
    """
    Test creating a energy conversion.
    """
    create_request = data_gen.random_energy_conversion_create(db)
    create_request.commodity_unit = "0"  # ungültige Anfrage
    response = client.post("/conversions/", headers=normal_user_headers, data=create_request.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO Add more test cases
