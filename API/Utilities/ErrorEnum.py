from enum import Enum


class ErrorCode(Enum):
    UNK = "Une erreur est survenue."
    DB_ERROR = "Erreur avec la base de donnée."
    USER_NFIND = "Utilisateur non trouvé."
    USER_NOT_FOUND = "user_not_found"
    MAIL_NOK = "Addresse email non valide."
    MAIL_USED = "Addresse email déjà en utilisation."
    PRODUCT_NFIND = "Produit non trouvé"
    BAD_TOKEN = "Le token envoyé est incorrecte"
    GENDER_NOK = "Genre non valide."
    NAME_NOK = "Nom et/ou prénom non valide."
    POSTAL_NOK = "Code postal non valide."
    COUNTRY_NOK = "Pays non valide."
    STREET_NOK = "Rue non valide."
    CITY_NOK = "Ville non valide."
    REGION_NOK = "Région non valide."
    ID_RFID_NOK = "Id_RFID non valide."
    NO_REF = "Le produit n'est pas référencé."
