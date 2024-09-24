import unittest
from unittest.mock import patch, Mock
from src.wb_parser import WBReview


class TestWBReview(unittest.TestCase):

    def setUp(self):
        # Выполняется перед каждым тестом
        self.sku = "190597734"
        self.review_parser = WBReview(string="https://wildberries.ru/catalog/190597734/detail.aspx")

    @patch('requests.get')
    def test_get_root_id_success(self, mock_get):
        # Настройка заглушки для успешного ответа API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "products": [
                    {"root": "root_id_example"}  # Заглушка для успешного ответа
                ]
            }
        }
        mock_get.return_value = mock_response

        root_id = self.review_parser.get_root_id(sku=self.sku)
        self.assertEqual(root_id, "root_id_example")

    @patch('requests.get')
    def test_get_root_id_failure(self, mock_get):
        # Настройка заглушки для неуспешного ответа API
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "data": {
                "products": []
            }
        }
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.review_parser.get_root_id(sku=self.sku)
        self.assertTrue("Can't get root_id from sku: 190597734" in str(context.exception))

    @patch('requests.get')
    def test_get_item_name_success(self, mock_get):
        # Настройка заглушки для успешного получения имени товара
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "products": [
                    {"name": "Test Item"}  # Заглушка для успешного ответа
                ]
            }
        }
        mock_get.return_value = mock_response

        item_name = self.review_parser.get_item_name(sku=self.sku)
        self.assertEqual(item_name, "Test Item")

    @patch('requests.get')
    def test_get_item_name_failure(self, mock_get):
        # Настройка заглушки для неуспешного получения имени товара
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.review_parser.get_item_name(sku=self.sku)
        self.assertTrue("Can't get item_name from sku: 190597734" in str(context.exception))

    def test_get_sku(self):
        # Проверяем, что метод get_sku правильно извлекает SKU
        expected_sku = "190597734"
        actual_sku = self.review_parser.get_sku(string="https://wildberries.ru/catalog/190597734/detail.aspx")
        self.assertEqual(actual_sku, expected_sku)

if __name__ == "__main__":
    unittest.main()