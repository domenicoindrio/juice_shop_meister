# Captcha Bypass
*Submit 10 or more customer feedbacks within 20 seconds*
#### Category: Broken Anti Automation
#### Difficulty: ★★★
#### Walktrough: [Video](https://go.screenpal.com/watch/cOhl2yntreb) - Duration 3:21 min

## Table of Contents:
- [Vulnerability Overview](#vulnerability-overview-broken-anti-automation)
- [Risk and Impact](#risk-and-impact)
- [Reproduction Steps](#reproduction-steps)
- [Remediation](#remediation)
- [Optional notes](#optional-notes)

> [!WARNING]  
> The content provided in this repository is for educational and ethical security testing purposes only. All demonstrations were performed in a controlled, local environment using the OWASP Juice Shop, a deliberately insecure web application. Unauthorized access to computing systems is illegal. The author is not responsible for any misuse of this information. Always obtain explicit permission before testing any system that you do not own.

# Vulnerability Overview: Broken Anti-Automation
Broken Anti-Automation occurs when a security control intended to prevent automated scripts, is implemented incorrectly. In this case, the Captcha serves (in theory) as the anti-automation mechanism.

The flaw lies in the Captcha lifecycle: the server validates the correctness of the answer but fails to enforce its uniqueness. Because the server doesn't ivalidate the Captcha ID after one successful use, the protection becomes useless and the system stays open for any number of automated requests.

## Risk and Impact
- **Database Inflation**: Attackers can automate the creation of thousands of records, leading to storage costs and database performance degradation.

- **Trust Erosion**: Automated spam in feedback or reviews ruins the reliability of user-generated content.

- **Resource Exhaustion**: Without anti-automation and rate-limiting, the server is vulnerable to **Application Layer DoS** attacks, where a simple script can consume all available backend processing threads.

## Reproduction Steps
### 1. Intercept the "Human" Proof
Submit a feedback at `http://127.0.0.1:3000/#/contact`, and inspect the request in the Burp Suite.
```json
{
    "UserId":23,
    "captchaId":2,
    "captcha":"20",
    "comment":"I've found 2 worms in my juice (***tomer@abc.com)",
    "rating":1
}
```
This provides a valid `captchaId` and `captcha` answer that the server has already *approved*.

### 2. Test the Anti-Automation Logic
Send the Feedback POST request to Burp Repeater, submit it multiple times and analyze the responses behaviour.

Observe how each request returns `201 Created`, even though they are all using the **same** Captcha. This confirms that the anti-automation mechanism does not track if a specific solution has already been used.

Double check further the feedbacks creation, by inspecting their section at `http://127.0.0.1:3000/#/about`.

### 3. Exploitation
To satisfy the challenge (10 feedbacks within 20 seconds), either use Burp Intruder or a Python script:  

#### Burp Intruder:
- Send the Feedback POST request from the Burp Repeater to Burp Intruder.
- Highlight a section of the Feedback `"comment"` field and click on `Add§`.
- Create or Load a string list containing at least 10 elements in the payload section.
- `Start attack` to launch the attack and solve the challenge.

#### Python script:
- Copy the JSON data from the Feedback POST request.
- Create a simple python script (like [this](./Scripts/captcha-bypass.py)) that uses a `for` loop to send multiple POST Requests to the Feedback endpoint (using the JSON data copied earlier as the payload).
- Launch the script and solve the challenge.
- Escalate this further by successfully sending 100 instead of 10 requests, confirming lack of rate-limiting measures too.

### 4. Confirm the Feedback Creation
Navigate again to `http://127.0.0.1:3000/#/about` and observe how the feedback section is flooded with several feedbacks, confirming the attack worked. 


## Remediation
- **Atomic Captcha Invalidation**: The backend must delete the Captcha solution from the session or database the millisecond it is verified.

- **Per-Action Rate Limiting**: Implement a *Cooldown* period for the `/api/Feedbacks/` endpoint.

- **Non-Replayable Tokens**: Use CSRF tokens or unique transaction IDs that must be refreshed for every single submission, preventing simple **replay** attacks.

## Optional Notes
Using a Python script firing >100 requests demonstrates that the vulnerability isn't just about reusing a Captcha, it's also about the server's inability to distinguish between a human typing and a script running a for loop, highliting additionally the lack of rate-limiting measures.


<--[Main Readme](/README.md)