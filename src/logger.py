import logging
import os
from datetime import datetime

log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path = os.path.join(os.getcwd(),"logs", log_file)
os.makedirs(logs_path,exist_ok=True)


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s" ,filename=logs_path)
