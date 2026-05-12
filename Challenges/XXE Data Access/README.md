# XXE Data Access
*Retrieve the content of C:\Windows\system.ini or /etc/passwd from the server*
#### Category: XXE
#### Difficulty: ★★★
#### Walktrough: [Video](https://go.screenpal.com/watch/cOh1btnthRC) - Duration 2:20 min

## Table of Contents:
- [Vulnerability Overview](#vulnerability-overview-xml-external-entity-xxe)
- [Risk and Impact](#risk-and-impact)
- [Reproduction Steps](#reproduction-steps)
- [Remediation](#remediation)
- [Optional notes](#optional-notes)

> [!WARNING]  
> The content provided in this repository is for educational and ethical security testing purposes only. All demonstrations were performed in a controlled, local environment using the OWASP Juice Shop, a deliberately insecure web application. Unauthorized access to computing systems is illegal. The author is not responsible for any misuse of this information. Always obtain explicit permission before testing any system that you do not own.

## Vulnerability Overview: XML External Entity (XXE)
XXE occurs when an XML parser is configured to process external entities within a Document Type Definition (DTD). An attacker can define a custom entity (it works like defining a variable) that points to a sensitive file on the server's local file system or an internal network resource. When the application parses the XML, it replaces the entity with the contents of that file.

In the Juice Shop, the vulnerability exists in the deprecated B2B interface, which still accepts XML uploads but fails to disable the processing of external entities.

## Risk and Impact
- **Arbitrary File Disclosure**: Attackers can read sensitive system files like `/etc/passwd` (on Linux) or `C:\Windows\system.ini` (on Windows), which reveal user accounts and system configurations.

- **Server-Side Request Forgery (SSRF)**: Attackers can use the server as a proxy to scan the internal network or access internal services that aren't exposed to the internet.

- **Information Leakage**: Even if the file isn't fully displayed, error messages (as seen in this challenge) can leak significant portions of the requested data.

## Reproduction Steps
### 1. Identify the Entry Point  
Navigate to the B2B **Complaint** interface at `http://127.0.0.1/#/complain`.  

This feature allows users to upload either a `*.zip` or a `*,pdf` a file. The interface is  *deprecated* though, and the backend still accepts and processes XML files before returning an error.

### 2. Prepare the Malicious Payload
Create a file (e.g., `xxe-payload.xml`) with a DTD that defines an external entity named `&secret;`

```xml
<?xml version="1.0"?>
<!DOCTYPE XXE [
    <!ENTITY secret SYSTEM "/etc/passwd">
]>
<name>&secret;</name>
```
### 3. Execute the Attack
Upload the file through the complaint interface.

### 4. Observe the Response
Monitor the traffic in Burp Suite and observe the response.  
The server returns a `410 Gone` error message. However, the error message includes the reflected content of your XML file, with the `&secret;` entity successfully resolved leaking actual content of the server's `/etc/passwd` file.

## Remediation
- **Disable DTDs**: The most effective defense is to completely disable `Document Type Definitions` (DTDs) in the XML parser configuration.

- **Disable External Entities**: If DTDs are required, specifically disable the support for External Entities and Parameter Entities.

- **Use Safer Formats**: Whenever possible, replace XML with less complex data formats like JSON, which do not support entity expansion by design.

- **Update Libraries**: Ensure that the XML parsing libraries being used are up to date and configured with secure defaults.

## Optional Notes
- **Entity Syntax**: For the attack to work, the reference inside the XML body, must match the definition happening in the header. In this case `&secret;` and `<!ENTITY secret ...>`.


<--[Main Readme](/README.md)