from enum import Enum


class SuccessCode(Enum):
    UNK = "Succès."
    USER_CREATED = "Utilisateur créé avec succès"
    USER_UPDATED = "Utilisateur modifié avec succès."
    USER_DELETED = "Utilisateur supprimé avec succès."
    PRODUCT_CREATED = "Produit ajouté avec succès"
    PRODUCT_DELETED = "Produit supprimé avec succès"

