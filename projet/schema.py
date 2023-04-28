declaration_insertion_schema = {
    'type': 'object',
    'required': ['quartier', 'arrondissement', 'adresse',
                 'date', 'nomPrenom', 'description'],
    'properties': {
             'quartier': {
                    'type': 'string'
                 },
             'arrondissement': {
                     'type': 'string'
                 },
             'adresse': {
                    'type': 'string'
                 },
             'date': {
                    'type': 'string'
                 },
             'nomPrenom': {
                     'type': 'string'
                 },
             'description': {
                    'type': 'string'
                 }
    },
    'additionalProperties': False
}

profil_schema = {
    'type': 'object',
    'required': ['nom', 'courriel', 'liste', 'motPass'],
    'properties': {
                'nom': {
                    'type': 'string'
                 },
                'courriel': {
                     'type': 'string',
                     'pattern': '^\\S+@\\S+\\.\\S+$',
                     'format': 'email'
                 },
                'liste': {
                    'type': 'string'
                },
                'motPass': {
                    'type': 'string'
                 }
    },
    'additionalProperties': False
}
