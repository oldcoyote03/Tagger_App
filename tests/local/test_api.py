"""
pytest /app/tests/local/test_api.py

"""

from uuid import UUID
from itertools import product, count
import pytest
from flask import url_for
from tests.local.data import MockData


@pytest.mark.usefixtures("client_example_memory")
class TestExampleApi:
    """ Test the Example API """

    def test_get_example(self, get_data, log):
        """ Test the get single bookmark endpoint """
        test_item_raw = MockData.EXAMPLE_DATA[1]
        test_item = {
            "id": str(test_item_raw.get("id")),
            "attr_str": test_item_raw.get("attr_str"),
            "attr_int": test_item_raw.get("attr_int"),
            "attr_bool": test_item_raw.get("attr_bool"),
            "created_at": str(test_item_raw.get("created_at")),
        }
        response = self.client.get(url_for("example-item", item_id=test_item.get("id")))  # pylint: disable=no-member
        log.info(f"test_item : {test_item}")
        log.info(f"response     : {get_data(response)}")
        assert get_data(response) == test_item

    def test_delete_item_found(self, get_data):
        """ Test the delete endpont """
        test_item = MockData.EXAMPLE_DATA[1]
        test_item_id = str(test_item.get("id"))
        response = self.client.delete(url_for("example-item", item_id=test_item_id))  # pylint: disable=no-member
        assert response.status_code == 204
        assert get_data(response) == ""

    def test_delete_item_not_found(self, get_data, log):
        """ Test the delete endpont """
        test_item_id = "9f03ef77-6501-449f-8902-0eca657e9db9"
        response = self.client.delete(url_for("example-item", item_id=test_item_id))  # pylint: disable=no-member
        log.info(f"response: {get_data(response)}")
        assert response.status_code == 404
        expected_data = f"SQL Not Found: model=Example; record ID: {test_item_id}"
        assert get_data(response) == expected_data

    def test_add_item(self, get_data):
        """ Test the add item endpoint """
        test_item = {"attr_str": "test_attr_str"}
        response = self.client.post(url_for("example-group"), json=test_item)  # pylint: disable=no-member
        assert response.status_code == 200
        assert UUID(get_data(response))

        # Adding the same item raises an IntegrityError
        response = self.client.post(url_for("example-group"), json=test_item)  # pylint: disable=no-member
        assert response.status_code == 400
        expected_exc = "Add example error: UNIQUE constraint failed: example.attr_str"
        assert get_data(response) == expected_exc

    def test_get_group_no_filter(self, get_data):
        """ Test the get group endpoint - all items """
        test_group = MockData.EXAMPLE_DATA
        response = self.client.get(url_for("example-group"))  # pylint: disable=no-member
        assert response.status_code == 200
        assert len(get_data(response)) == len(test_group)

    @pytest.mark.parametrize(
        "uri, item_num",
        [
            (f"flag={flag}&quantity={quantity}", item_num)
            for (flag, quantity,), item_num in zip(product([True, False], range(3)), count(1))
        ]
    )
    def test_get_group_filters(self, uri, item_num, get_data):
        """ Test the get group endpoint - with filters """
        response = self.client.get(f"{url_for('example-group')}?{uri}")  # pylint: disable=no-member
        assert response.status_code == 200
        assert len(get_data(response)) == 1
        assert get_data(response)[0].get("name") == f"item{item_num}"
