# recent_files.py
import json
import os
from PyQt5.QtWidgets import QAction

# فایل برای ذخیره تاریخچه فایل‌ها
recent_files_file = 'recent_files.json'

def save_recent_file(file_path):
    """ذخیره فایل اخیر در JSON"""
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return
    
    # بارگذاری فایل‌های اخیر
    if os.path.exists(recent_files_file):
        try:
            with open(recent_files_file, 'r') as f:
                recent_files = json.load(f)
        except json.JSONDecodeError:
            recent_files = []
    else:
        recent_files = []

    # اضافه کردن فایل به لیست
    file_entry = {'file_path': file_path}
    recent_files = [entry for entry in recent_files if entry['file_path'] != file_path]
    recent_files.insert(0, file_entry)

    # ذخیره فایل‌های اخیر (تا 5 فایل)
    try:
        with open(recent_files_file, 'w') as f:
            json.dump(recent_files[:5], f, indent=4)
    except Exception as e:
        print(f"Error saving recent files: {e}")

def load_recent_files():
    """بارگذاری فایل‌های اخیر از JSON"""
    if os.path.exists(recent_files_file):
        try:
            with open(recent_files_file, 'r') as f:
                recent_files = json.load(f)
            return [entry['file_path'] for entry in recent_files if os.path.exists(entry['file_path'])]
        except json.JSONDecodeError:
            return []
    return []

def populate_recent_menu(recent_menu, load_callback):
    """پر کردن منوی Open Recent"""
    recent_menu.clear()
    for fnt_file in load_recent_files():
        action = QAction(fnt_file, recent_menu)
        action.triggered.connect(lambda checked, file=fnt_file: load_callback(file))
        recent_menu.addAction(action)