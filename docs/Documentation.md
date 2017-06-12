# Union Board Documentation

## Table of contents:
* [Requests](#requests)
* [API Endpoints](#api-endpoints)
* [POST Request content](#post-request-content)
* [Database Design](#database-design)

## Requests:

Verb | Description
---------|----------
 GET | Used for retrieving resources.
 POST | Used for creating resources
 PUT | Used for changing/replacing resources
 DELETE | Used for deleting resources

## API Endpoints:

Method | Endpoint | Usage | Returns | Authentication
---------|----------|--------- | ---------- | ---------
 GET | `/companies` | Get all companies' information | Arrays of companies | OAuth
 GET | `/companies/{company_id}` | Get a company information | Object including name, founders' email and bio | OAuth
 GET | `/companies/{company_id}?fields={name,emails,website,bio}` | Get a company information based on particular parameters | Object including fields specified in the request parameter | OAuth
 GET | `/companies/{company_id}/sales` | Get a company's weekly sales information | Company's name and sales | OAuth
 GET | `/companies/{company_id}/traffic` | Get a company's weekly traffic information | Company's name and web traffic | OAuth
 GET | `/companies/{company_id}/customers` | Get a company's weekly customers information | Company's name and customers | OAuth
 GET | `/companies/{company_id}/emails` | Get a company's weekly emails information | Company's name and emails | OAuth
 POST | `/companies` | Create a new company | success/error message and company object | OAuth
 POST | `/companies/{company_id}` | Add KPI metrics to a company | success/error message and the metrics recently added | OAuth
 PUT | `/companies/{company_id}` | Update a company's information including name, bio, website, and KPI metrics | success/error message and data recently updated | OAuth

## POST Request content:

`POST /companies`

Request:
```json
{
    "name": "Demo",
    "founders": [
        {
            "name": "Tu Tran",
            "email": "tu@demo.com",
            "role": "CTO"
        },
        {
            "name": "John Average",
            "email": "john@demo.com",
            "role": "CEO"
        }
    ],
    "website": "http://www.demo.com",
    "bio": "This is a demo company. Nothing too special here."
}
```

Returns:

On success
```json
{
    "status": "success",
    "message": "new company created!",
    "id": 12342345
}
```

On failure
```json
{
    "status": "failure",
    "message": "error message"
}
```

`POST /companies/{company_id}`


## Database Design:

Company:
```yaml
- id:           integer
- name:         string
- founders:     array
- website:      string
- bio:          text
```

Founder
```yaml
- id:           integer
- company_id:   integer  # Foreign Key to Company table
- email:        string
- name:         string
- role:         string
```

Sale:
```yaml
- id:           integer
- company_id:   integer  # Foreign Key to Company table
- week:         integer
- value:        double
```

Customer:
```yaml
- id:           integer
- company_id:   integer  # Foreign Key to Company table
- week:         integer
- value:        integer
```

Web Traffic:
```yaml
- id:           integer
- company_id:   integer  # Foreign Key to Company table
- week:         integer
- value:        integer
```

Email:
```yaml
- id:           integer
- company_id:   integer  # Foreign Key to Company table
- week:         integer
- value:        integer
```
