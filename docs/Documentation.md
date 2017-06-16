# Union Board Documentation

## Table of contents:
* [Requests](#requests)
* [Progress](#progress)
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

## Progress:
- [x] `GET /companies`
- [x] `GET /companies/{company_id}`
- [ ] `GET /companies/{company_id}?fields={name,emails,website,bio}`
- [x] `GET /companies/{company_id}/{metric}`
- [x] `POST /companies`
- [x] `POST /companies/{company_id}`
- [ ] `PUT /companies/{company_id}/update`
- [ ] `POST /auth/login`
- [ ] `POST /auth/change`
- [ ] `GET /auth/status`
- [ ] `POST /auth/logout`


## API Endpoints:

### Startup-related API:

 Method | Endpoint | Usage | Returns | Authentication
---------|----------|--------- | ---------- | ---------
 GET | `/companies` | Get all companies' information | Arrays of companies | OAuth
 GET | `/companies/{company_id}` | Get a company information | Object including name, founders' email and bio | OAuth
 GET | `/companies/{company_id}?fields={name,emails,website,bio}` | Get a company information based on particular parameters | Object including fields specified in the request parameter | OAuth
 GET | `/companies/{company_id}/{metric}` | Get a company's weekly metric information | Company's name and sales | OAuth
 POST | `/companies` | Create a new company | success/error message and company object | OAuth
 POST | `/companies/{company_id}` | Add KPI metrics to a company | success/error message and the metrics recently added | OAuth
 PUT | `/companies/{company_id}/update` | Update a company's metric (value and updated_at field) | success/error message and data recently updated | OAuth

### Authentication API:

 Method | Endpoint | Usage | Returns | Authentication
---------|----------|--------- | ---------- | ---------
 POST | `/auth/login` | Log in | status and authentication token | None
 POST | `/auth/change` | Change a user's password | status and message | OAuth
 GET | `/auth/status` | Check the current status of the user, whether Brandery staff or startup founders | object with user information | OAuth
 POST | `/auth/logout` | Log out | status and message | OAuth

## Sample Data Format:

### `GET /companies`

#### Return format:
```json
{
    "total": 2,
    "companies": {
        "Demo": {
            "id": 145,
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
        "Boocoo": {
            "id": 2030,
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
    }
}
```

### `GET /companies/{company_id}`

#### Return format:
```json
{
    "id": 145,
    "name": "Demo",
    "website": "http://demo.com",
    "founders" : [
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
    "bio": "This is a demo company. Nothing too special here"
}
```

### `GET /companies/{company_id}/{metric}`

#### Return format:
```json
{
    "weeks": 4,
    // "%a, %d %b %Y %H:%M:%S GMT"
    "last_updated": "Fri, 16 Jun 2017 15:57:23 GMT",
    "data": [12, 34, 56, 23]
}
```

### `POST /companies`

#### Request body:
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

#### Return format:
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

#### Request body:
```json
{
    "sales": 123.7,
    "customers": 23,
    "traffic": 950,
    "emails": 500
}
```
**Note**: Any fields can be omitted but **cannot** be empty

#### Return format:
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

### `POST /auth/login`

#### Request Body:
```json
{
    "email": "john.doe@companyx.com",
    "password": "123456"
}
```

#### Return format:
On success:
```json
{
    "status": "success",
    "message": "logged in",
    "auth_token": "AaDEW143G@d"
}
```

On failure:
```json
{
    "status": "failure",
    "message": "wrong password or user does not exist"
}
```

### `POST /auth/change`

TODO

### `GET /auth/status`

TODO

### `POST /auth/logout`

TODO

## Database Design:

### Company:
```yaml
- id:           integer
- name:         string
- founders:     array
- website:      string
- bio:          text
```

### Founder
```yaml
- id:           integer
- company_id:   integer  # Foreign Key to Company table
- email:        string
- name:         string
- role:         string
```

### User
```yaml
- id:           integer
- founder_id:   integer # Foreign Key to Founder table
- email:        integer
- password:     string
- created_at:   datetime
- staff:        boolean
```

### Metric (Sale, Customer, Traffic, Email):
```yaml
- id:           integer
- company_id:   integer  # Foreign Key to Company table
- week:         integer
- updated_at:   datetime
- value:        double
```
