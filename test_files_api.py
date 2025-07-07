#!/usr/bin/env python3
import requests
import json
import os

BASE_URL = "http://localhost:8000/api"

def test_login(username="filetest", password="filetest123"):
    """Test user login"""
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/token", data=data)
    print(f"Login Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Login successful: {response.json()}")
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.json()}")
    return None

def test_upload_file(token, file_path):
    """Test file upload"""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(f"{BASE_URL}/files/upload", headers=headers, files=files)
    
    print(f"Upload Response: {response.status_code}")
    if response.status_code == 200:
        print(f"File uploaded successfully: {response.json()}")
        return response.json()
    else:
        print(f"Upload failed: {response.text}")
    return None

def test_list_files(token, search=None):
    """Test listing files"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"search": search} if search else {}
    
    response = requests.get(f"{BASE_URL}/files", headers=headers, params=params)
    print(f"List Files Response: {response.status_code}")
    if response.status_code == 200:
        files_data = response.json()
        print(f"Found {files_data['total']} files:")
        for file_info in files_data['files']:
            print(f"  - {file_info['original_filename']} ({file_info['size']} bytes)")
        return files_data['files']
    else:
        print(f"List files failed: {response.text}")
    return []

def test_download_file(token, file_id, filename):
    """Test file download"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/files/{file_id}", headers=headers)
    print(f"Download Response: {response.status_code}")
    
    if response.status_code == 200:
        download_filename = f"downloaded_{filename}"
        with open(download_filename, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded as: {download_filename}")
        return True
    else:
        print(f"Download failed: {response.text}")
    return False

def test_delete_file(token, file_id):
    """Test file deletion"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.delete(f"{BASE_URL}/files/{file_id}", headers=headers)
    print(f"Delete Response: {response.status_code}")
    
    if response.status_code == 200:
        print(f"File deleted successfully: {response.json()}")
        return True
    else:
        print(f"Delete failed: {response.text}")
    return False

def create_test_file():
    """Create a test file for upload"""
    test_content = """Este é um arquivo de teste para verificar
a funcionalidade de upload de arquivos.

Conteúdo:
- Data: 2024
- Sistema: AWS Project
- Funcionalidade: Upload de arquivos
"""
    
    with open('test_file.txt', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("Test file 'test_file.txt' created")
    return 'test_file.txt'

if __name__ == "__main__":
    print("=== Testing File Management API ===")
    
    # Test login
    print("\n1. Testing Login...")
    token = test_login()
    
    if not token:
        print("Cannot proceed without valid token")
        exit(1)
    
    # Create test file
    print("\n2. Creating test file...")
    test_file = create_test_file()
    
    # Test upload
    print("\n3. Testing File Upload...")
    uploaded_file = test_upload_file(token, test_file)
    
    if uploaded_file:
        file_id = uploaded_file['id']
        
        # Test list files
        print("\n4. Testing List Files...")
        files = test_list_files(token)
        
        # Test search
        print("\n5. Testing File Search...")
        search_files = test_list_files(token, search="test")
        
        # Test download
        print("\n6. Testing File Download...")
        test_download_file(token, file_id, uploaded_file['original_filename'])
        
        # Test delete
        print("\n7. Testing File Delete...")
        test_delete_file(token, file_id)
        
        # Test list again to confirm deletion
        print("\n8. Verifying Deletion...")
        files_after_delete = test_list_files(token)
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\nCleaned up test file: {test_file}")
    
    if os.path.exists('downloaded_test_file.txt'):
        os.remove('downloaded_test_file.txt')
        print("Cleaned up downloaded file")
