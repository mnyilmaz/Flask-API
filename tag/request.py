import requests

url = 'http://localhost:5000/tagAPI'
data = {
        'title': 'yeni kırılım eklenmesi',
        'issue': 'verilen ücret komisyonlar altına ptt komisyonu alt kırılımının eklenmesini talep eder'}
headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': 'the-csrf-token'  # Replace 'the-csrf-token' with the actual CSRF token value
}

response = requests.post(url, json=data, headers=headers)
print(data)
print(response.json())
