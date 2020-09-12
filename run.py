# -*- coding: utf-8 -*-
import os

from app import app, db

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 8080))
    db.drop_all()
    db.create_all()
