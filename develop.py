# -*- coding: utf-8 -*-
"""
    develop
    ~~~~~~~

    run app in debug mode.
"""

from website import app
app.run(debug=True, host='0.0.0.0', port=2333)
