from app import create_app
from config import TestConfig

def test_dog_image_route():
    app = create_app(TestConfig)  
    client = app.test_client()

    with app.app_context():
        response = client.get('/api/dog-image')
        assert response.status_code == 200
        data = response.get_json()
        assert "image_url" in data
        assert data["status"] == "success"
