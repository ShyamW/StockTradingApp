# Import app variable from our app package
from app import app


app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
