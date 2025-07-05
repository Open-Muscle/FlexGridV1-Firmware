# Hardware Open Muscle FlexGrid - (FlexGrid) V1
# 60 Sensor 15x4 Velostat pressure sensor matrix
# Software version 0.1.0
# Coded for ESP32-S3
# 07-05-2025 - TURFPTAx


# boot.py

import uasyncio as asyncio
import flexgrid
import logger

logger.info("Booting FlexGrid system…")
loop = asyncio.get_event_loop()
loop.create_task(flexgrid.main())
loop.run_forever()
