from enum import Enum


class ErrorCode(Enum):
    UNK = "Une erreur est survenue."
    DB_ERROR = "Erreur avec la base de donnée."
    USER_NFIND = "Utilisateur non trouvé."
    MAIL_NOK = "Addresse email non valide."
    MAIL_USED = "Addresse email déjà en utilisation"
    PRODUCT_NFIND = "Produit non trouvé"
    ID_RFID_NOK = "Id_RFID non valide."
