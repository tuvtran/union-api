import random

data1 = {
    'name': 'Demo',
    'founders': [
        {
            'name': 'Tu Tran',
            'email': 'tu@demo.com',
            'role': 'CTO'
        },
        {
            'name': 'John Average',
            'email': 'john@demo.com',
            'role': 'CEO'
        }
    ],
    'website': 'http://www.demo.com',
    'bio': 'This is a demo company. Nothing too special here.',
}

data2 = {
    'name': 'Boocoo',
    'founders': [
        {
            'name': 'Jane Jacob',
            'email': 'jane@boocoo.club',
            'role': 'CEO'
        },
        {
            'name': 'Tu Tran',
            'email': 'tu@boocoo.club',
            'role': 'CTO'
        },
        {
            'name': 'Sed Heath',
            'email': 'sed@boocoo.club',
            'role': 'COO'
        },
    ],
    'website': 'http://boocoo.club',
    'bio': "Boocoo is a AI startup specializing in random stuff."
}

data3 = {
    'name': 'Axxos',
    'founders': [
        {
            'name': 'David Facktard',
            'email': 'david@axxos.io',
            'role': 'CEO'
        },
        {
            'name': 'Nick Carraway',
            'email': 'nick@axxos.io',
            'role': 'CTO'
        },
        {
            'name': 'Sed Minker',
            'email': 'sed@axxos.io',
            'role': 'COO'
        },
    ],
    'website': 'http://axxios.io',
    'bio': "We specialize in making humans less stupid."
}

kpi_list = [
    'sales', 'traffic', 'subscribers',
    'active_users', 'paying_users', 'engagement',
    'mrr', 'cpa', 'pilots', 'product_releases', 'preorders',
    'automation_percents', 'conversion_rate', 'marketing_spent',
    'other_1', 'other_2']

kpis = {}
for metric in kpi_list:
    kpis[metric] = [random.randint(10, 50) for _ in range(10)]
