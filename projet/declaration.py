class Declaration:
    def __init__(self, id, quartier, arrondissement,
                 adresse, date, nomPrenom, description):
        self.id = id
        self.quartier = quartier
        self.arrondissement = arrondissement
        self.adresse = adresse
        self.date = date
        self.nomPrenom = nomPrenom
        self.description = description

    def asDictionary(self):
        return {"id": self.id,
                "quartier": self.quartier,
                "arrondissement": self.arrondissement,
                "adresse": self.adresse,
                "date": self.date,
                "nomPrenom": self.nomPrenom,
                "description": self.description
                }
