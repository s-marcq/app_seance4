from ..app import app, db
from flask import render_template
from ..models.factbook import Country
from sqlalchemy import or_

@app.route("/pays")
def pays():
    donnees = []
    for country in Country.query.all():
        donnees.append({
            "nom": country.name,
            "capitale":"inconnu",
            "continent":"inconnu"
        })
    
    return render_template("pages/tous_pays.html", donnees=donnees, sous_titre="Tous les pays")

@app.route("/pays/<string:nom>")
def pays_specifique(nom):
    grandes_villes = []
    if nom =='France':
        grandes_villes = ['Paris', 'Lyon', 'Marseille']
    return render_template("pages/pays.html", pays=nom, grandes_villes=grandes_villes, sous_titre=nom)

@app.route("/tous_pays") # affiche tous les pays de la table Country
def tous_pays():
    donnees = Country.query.all()
    return render_template("pages/generique.html", donnees = donnees)

@app.route("/le_premier_pays") # affiche le premier pays de la table Country
def le_premier_pays():
    donnees = Country.query.first()
    return render_template("pages/generique.html", donnees = [donnees])

@app.route("/pays_differents_de_souverain") # 
def pays_differents_de_souverain():
    donnees = Country.query.filter(Country.type == 'sovereign')
    return render_template("pages/generique.html", donnees = donnees)

@app.route("/condition_or_autre_condition") #
def condition_or_autre_condition():
    donnees = Country.query.filter(or_(Country.type == 'sovereign', Country.id == 'ay'))
    return render_template("pages/generique.html", donnees = donnees)

@app.route("/ajout_pays/<string:id>/<string:name>/<string:type>/<string:rapide_description>") #
def ajout_pays(id, name, type, rapide_description):
    nouveau_pays = Country(id=id, name=name, type=type, Introduction = rapide_description)
    db.session.add(nouveau_pays)
    db.session.commit()
    return "OK"

@app.route("/get_pays/<string:id>") # renvoyer tous les pays (normalement un seul) correspondant à l'id fourni
def get_pays(id):
    nouveau_pays = Country.query.get({"id": id})
    return render_template("pages/generique.html", donnees = [nouveau_pays])

