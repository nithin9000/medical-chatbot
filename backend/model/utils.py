import os
import time
import psutil

EMBEDDING_MODEL_NAME = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
showMessage = True

def log_time(message):
	if showMessage:
		print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]{message}")

def check_memory_usage(threshold = 80):
	memory = psutil.virtual_memory()
	return memory.percent < threshold

def count_pdfs_in_folder(folder_path):
	total_pdfs = 0

	for root,dirs,files in os.walk(folder_path):
		pdf_count = len([file for file in files if file.lower().endswith('.pdf')])
		total_pdfs += pdf_count
		print(f"Found {pdf_count} PDFs in {root}")