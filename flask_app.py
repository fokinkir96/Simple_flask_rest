from app import app, db
from app.models import User
import os

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

# app.run(debug=True)
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))