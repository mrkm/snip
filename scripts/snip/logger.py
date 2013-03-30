#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    #filename=os.path.join(settings.PROJECT_ROOT, 'log/nishitetsu.log'),
                    filemode='a')

logger = logging
