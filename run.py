# -*- coding: utf-8 -*-
import os

from app import app, manager

if __name__ == "__main__":
    manager.run()
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 8080))
