# Union Board Documentation

## Table of contents:
* [Requests](#requests)
* [API Endpoints](#api-endpoints)
* [Sample Data Format](#sample-data-format)
* [Database Design](#database-design)

## Requests:

Verb | Description
---------|----------
 GET | Used for retrieving resources.
 POST | Used for creating resources
 PUT | Used for changing/replacing resources
 DELETE | Used for deleting resources

## API Endpoints:

Done | Method | Endpoint | Usage | Returns | Authentication
---------|---------|----------|--------- | ---------- | ---------
 [x] | GET | `/companies` | Get all companies' information | Arrays of companies | OAuth
 [x] | GET | `/companies/{company_id}` | Get a company information | Object including name, founders' email and bio | OAuth
 [x] | GET | `/companies/{company_id}?fields={name,emails,website,bio}` | Get a company information based on particular parameters | Object including fields specified in the request parameter | OAuth
 [x] | GET | `/companies/{company_id}/sales` | Get a company's weekly sales information | Company's name and sales | OAuth
 [x] | GET | `/companies/{company_id}/traffic` | Get a company's weekly traffic information | Company's name and web traffic | OAuth
 [x] | GET | `/companies/{company_id}/customers` | Get a company's weekly customers information | Company's name and customers | OAuth
 [x] | GET | `/companies/{company_id}/emails` | Get a company's weekly emails information | Company's name and emails | OAuth
 [x] | POST | `/companies` | Create a new company | success/error message and company object | OAuth
 [x] | POST | `/companies/{company_id}` | Add KPI metrics to a company | success/error message and the metrics recently added | OAuth
 [ ] | PUT | `/companies/{company_id}/update` | Update a company's information including name, bio, website, and KPI metrics | success/error message and data recently updated | OAuth

## Sample Data Format:

### `GET /companies`

Return format:
```json
{
    "total": 2,
    "companies": [
        {
            "id": 145,
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
        },
        {
            "id": 2030,
            "name": "Boocoo",
            "founders": [
                {
                    "name": "Jane Jacob",
                    "email": "jane@boocoo.club",
                    "role": "CEO"
                }
            ],
            "website": "http://boocoo.club",
            "bio": "Boocoo is a AI startup specializing in random stuff."
        }
    ]
}
```

### `POST /companies`

Request body:
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

Return format:

On success:
```json
{
    "status": "success",
    "message": "new company created!",
    "id": 12342345
}
```

On failure:
```json
{
    "status": "failure",
    "message": "error message"
}
```

### `POST /companies/{company_id}`

Request body:
```json
{
    "sales": 123.7,
    "customers": 23,
    "traffic": 950,
    "emails": 500
}
```
**Note**: Any fields can be omitted but **cannot** be empty

Return format:

On success:
```json
{
    "status": "success",
    "message": "metrics added",
    "metrics_added": {
        "sales": 123.7,
        "customers": 23,
        "traffic": 950,
        "emails": 500
    }
}
```

On failure:
```json
{
    "status": "failure",
    "message": "one of the metrics is empty"
}
```


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
