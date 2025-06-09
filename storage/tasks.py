from celery import shared_task
from .utils.virus_scan import scan_file_for_virus

@shared_task
def async_scan_file(file_path):
    result = scan_file_for_virus(file_path)
    return result