# **BIENVENUE SUR L'API ARLEX**

Ici vous trouverez toutes les informations concernants les commandes et les configurations du projet Arlex.


Afin d'appeler les différentes routes chaques utilisateur doit disposer d'un Token.

**Pour installer l'ensemble des dépendances:**
--------------------------

`pip3 install -r requirements.txt`


**Pour lancer l'api:**
--------------------------

`python3 main.py`


**Pour générer un token:**
--------------------------

   - il est obligatoire de disposer d'un utilisateur. Pour le créer :
        - Apppeller la route: `http://localhost:5000/api/user/`, avec comme body (example) :
            `{ "gender": 0, 
            "lastname": "Doe",
            "firstname": "John",
            "mail": "john@doe.com",
            "password": "password",
            "country": "France",
            "town": "Lille",
            "street": "rue nationale",
            "street_number": "13",
            "region": "Hauts de france",
            "postal_code": "12345"
            }`
   - Ensuite, il faut appeler la route `https://localhost:5000/api/token` avec comme body (example):
       `{
       "client_id": "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com",
       "client_secret": "test",
       "grant_type": "password",
       "app_id": "arlex-ccevqe",
       "username": "augustin.lopacinski59@gmail.com",
       "password": "password"
       }`
       
**Pour faire un push sur le git:**
--------------------------
  
  Il est obligatoire de faire une nouvelle branche pour chaque feature ou chaque coorection de bug ! 
  
  Pour créer une nouvelle branche : `git checkout -b <feature/nom_de_la_noubelle branche>`
  
  Ensuite pour commit: `git commit -am "DESCRIPTION PRECISE de votre commit"
  
  pour push : `git push origin <nom_de_votre_branche>
  
  Il faut ensuite créer une pull request. Une fois que trois review ont validé votre pull request et que travis valide les test, vous pouvez merge.
  

    
