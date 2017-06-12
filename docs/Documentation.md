# Union Board Documentation

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
 POST | `/companies` | Create a new company | success/error message and company object | OAuth
 POST | `/companies/{company_id}` | Add KPI metrics to a company | success/error message and the metrics recently added | OAuth
 PUT | `/companies/{company_id}` | Update a company's information including name, bio, website, and KPI metrics | success/error message and data recently updated | OAuth

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
- id:       integer  # Foreign Key to Company table
- email:    string
- name:     string
- role:     string
```

Sale:
```yaml
- id:       integer  # Foreign Key to Company table
- week:     integer
- sales:    double
```

Customer:
```yaml
- id:           integer  # Foreign Key to Company table
- week:         integer
- customers:    integers
```

Web Traffic:
```yaml
- id:       integer  # Foreign Key to Company table
- week:     integer
- sales:    double
```

Email:
```yaml
- id:       integer  # Foreign Key to Company table
- week:     integer
- emails:   integer
```