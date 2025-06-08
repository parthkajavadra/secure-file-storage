import logging
from typing import Optional, Dict, Tuple
import pyclamd


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.warning("This is a test warning log for virus detection")

def scan_file_for_virus(file_path: str) -> Optional[Dict[str, Tuple[str, str]]]:
    """
    Scans the given file for viruses using ClamAV via TCP socket.

    Args:
        file_path (str): Absolute path to the file to be scanned.

    Returns:
        dict: Result of the scan if a virus is found or an error occurs.
              Example: {'/path/to/file': ('FOUND', 'Eicar-Test-Signature')}
        None: If no virus is found.
    """
    try:
        clamav = pyclamd.ClamdNetworkSocket(host="127.0.0.1", port=3310)

        if not clamav.ping():
            logger.error("ClamAV daemon is not responding to ping.")
            return {"error": "ClamAV daemon did not respond"}

        logger.info("ClamAV daemon is responsive.")
        result = clamav.scan_file(file_path)
        logger.debug(f"Scan result returned: {result}")

        if result:
            logger.warning(f"Virus detected: {result}")
        else:
            logger.info("No virus detected.")

        return result
    except Exception as e:
        logger.exception("Virus scanning failed.")
        return {"error": str(e)}