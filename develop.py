# -*- coding: utf-8 -*-
"""
    develop
    ~~~~~~~

    run app in debug mode.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""

from website import app
app.run(debug=True, host='0.0.0.0', port=2333)
