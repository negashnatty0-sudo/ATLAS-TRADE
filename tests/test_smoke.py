from app import create_app
def test_health():
    app=create_app()
    c=app.test_client()
    assert c.get('/api/health').json['status']=='ok'
