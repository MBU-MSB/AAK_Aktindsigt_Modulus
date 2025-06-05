"""henter alle fil id'er på en borgers sag."""
import json
import os
from urllib.parse import urlparse
import requests


def get_fileids_by_case_api(cookie: str, caseid: str) -> list:
    """henter alle fil id'er på en borgers sag."""

    url = f"https://aarhus.modulussocial.dk/odata/SflDocument/Default.GetByCase(Id={caseid})?$select=title,fileSize,fileType,finalized,journalized,remarkRegardingSubjectAccess,id,isSensitive,type&$orderby=journalized%20desc&$skip=0&$top=20&$count=true"

    payload = {}
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;odata.metadata=none',
    'Expires': '0',
    'Pragma': 'no-cache',
    'Referer': 'https://aarhus.modulussocial.dk/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-ExportData': 'false',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': cookie
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=20)

    # Parse the JSON response
    data = json.loads(response.text)

    # Extract all "id" values
    id_list = [item['id'] for item in data.get('value', [])]

    return id_list


def get_filelinks_by_fileid_api(cookie: str, fileid: int, serial, cpr):
    """henter alle fil id'er på en borgers sag."""

    url = f"https://aarhus.modulussocial.dk/api/activityDocuments/edit/{fileid}"

    payload = {}
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://aarhus.modulussocial.dk/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': cookie
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=20)

    print(response.text)

    file_link = response.text.strip('"')

    # Handle MS-Word protocol links
    if file_link.startswith('ms-word:'):
        # Extract the actual URL from the ms-word protocol handler
        # Format is typically: ms-word:ofe|u|https://actual-url-here
        parts = file_link.split('|')
        if len(parts) >= 3:
            file_link = parts[2]  # Extract the actual URL
            print(f"Extracted actual URL: {file_link}")
        else:
            raise ValueError(f"Could not parse MS-Word protocol URL: {file_link}")

    # Now file_link should be a direct HTTP/HTTPS URL
    if not file_link.startswith(('http://', 'https://')):
        raise ValueError(f"Invalid URL format after processing: {file_link}")

    # Make a request to the file link
    file_response = requests.get(file_link, timeout=20)

    # Parse the URL to extract the document name and extension
    parsed_url = urlparse(file_link)
    file_path = parsed_url.path
    document_name_with_extension = os.path.basename(file_path)

    # Define the directory path
    directory_path = rf"\\srvsql46\INDBAKKE\AAK_Aktindsigt\{serial}_{cpr}\Modulus"

    # Create the directory if it does not exist
    os.makedirs(directory_path, exist_ok=True)

    # Save the file content to a local file
    file_save_path = os.path.join(directory_path, document_name_with_extension)
    with open(file_save_path, 'wb') as file:
        file.write(file_response.content)

    print(f"File saved as {file_save_path}")
