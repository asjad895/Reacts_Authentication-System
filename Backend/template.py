import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
    "app/__init__.py",
    "app/models.py",
    "app/views/__init__.py",
    "app/views//auth.py",
    "app/views/profile.py",
    "app/views/email.py",
    "app/views/password_reset.py",
    "app/utils/__init__.py",
    "app/utils/helpers.py",
    "config.py",
    "run.py",
    "requirements.txt",
    "app/prompt.py",
    ".env",
    "setup.py",
    "research/test.ipynb",
    "app.py",
    "store_index.py",
    "static/.gitkeep",
    "templates/chat.html"

]


for filepath in list_of_files:
   filepath = Path(filepath)
   filedir, filename = os.path.split(filepath)

   if filedir !="":
      os.makedirs(filedir, exist_ok=True)
      logging.info(f"Creating directory; {filedir} for the file {filename}")

   if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
      with open(filepath, 'w') as f:
         pass
         logging.info(f"Creating empty file: {filepath}")

   else:
      logging.info(f"{filename} is already created")
      
      
    