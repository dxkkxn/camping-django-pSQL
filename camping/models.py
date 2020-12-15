from django.db import models
from .scripts import date_18_years_before
# Create your models here.
birthday_min = date_18_years_before()

class TypeEmplacement(models.Model):
    type_emplacement = models.CharField(max_length = 30, primary_key = True)
    nb_personnes_max = models.IntegerField()
    prix_journee     = models.DecimalField(max_digits = 10, decimal_places = 2)
    class Meta:
        db_table = "type_emplacement"

class Emplacement(models.Model):
    num_emplacement  = models.AutoField(primary_key = True)
    type_emplacement = models.ForeignKey(TypeEmplacement,
                                    db_column = "type_emplacement",
                                    on_delete = models.CASCADE)
    class Meta:
        db_table = "emplacement"

class Profil(models.Model):
    id_profil         = models.AutoField(primary_key = True)
    nom_client        = models.CharField(max_length = 30)
    prenom_client     = models.CharField(max_length = 30)
    adresse           = models.CharField(max_length = 50)
    telephone         = models.IntegerField()
    date_de_naissance = models.DateField()#
    #Num_carte = models.AutoField()
    email             = models.EmailField()
    password          = models.CharField(max_length= 30)

    class Meta:
        db_table = "profil"
        constraints = [
            models.CheckConstraint(check=(models.Q(telephone__gte = 100000000,
                                                    telephone__lt = 1000000000)),
            name='tel_digits'),

            models.CheckConstraint(check=(models.Q(date_de_naissance__lte = birthday_min)),
            name='age18ans'),
            models.UniqueConstraint(name = "email unique"  , fields = ["email"])
        ]

class OptionLocation(models.Model):
    option_location = models.CharField(max_length = 30, primary_key = True)
    remise_option   = models.IntegerField()
    class Meta:
        db_table    = "option_location"

class ServicesProposes(models.Model):
    nom_service       = models.CharField(max_length = 30, primary_key = True)
    description       = models.CharField(max_length = 500)
    prix_suplement    = models.IntegerField()

    class Meta:
        db_table = "services_proposes"

class Saison(models.Model):
    code_saison     = models.AutoField(primary_key = True)
    libelle_saison  = models.CharField(max_length = 30)
    date_com        = models.DateField()
    date_fin        = models.DateField()
    coef_majoration = models.IntegerField()
    class Meta:
        db_table = "saison"


class Reservation(models.Model):
    num_reservation  = models.AutoField(primary_key = True)
    nb_personnes     = models.IntegerField()
    acompte          = models.IntegerField()
    reglement        = models.DecimalField(max_digits = 10, decimal_places = 2)
    reglement_bool   = models.BooleanField(default = False)
    date_reservation = models.DateField()
    debut_sejour     = models.DateField()
    fin_sejour       = models.DateField()
    annulation       = models.BooleanField(default = False)
    presence         = models.BooleanField(default = False)
    option_location  = models.ForeignKey(OptionLocation,
                                        db_column = "option_location",
                                        on_delete = models.CASCADE)
    type_emplacement = models.ForeignKey(TypeEmplacement,
                                        db_column = "type_emplacement",
                                         on_delete = models.CASCADE)
    code_saison     = models.ForeignKey(Saison, db_column = "code_saison",
                                        on_delete = models.CASCADE)
    class Meta:
        db_table = "reservation"

class Client(models.Model):
    num_client        = models.AutoField(primary_key = True)
    nom_client        = models.CharField(max_length = 30)
    prenom_client     = models.CharField(max_length = 30)
    adresse           = models.CharField(max_length = 50)
    telephone         = models.IntegerField()
    date_de_naissance = models.DateField()#
    #Num_carte = models.AutoField()
    num_emplacement   = models.ForeignKey(Emplacement,
                                            db_column = "num_emplacement",
                                            on_delete = models.CASCADE)
    num_reservation   = models.ForeignKey(Reservation,
                                        db_column = "num_reservation",
                                         on_delete = models.CASCADE)
    class Meta:
        db_table = "client"

class Fidelite(models.Model):
    point_fidelite = models.IntegerField(primary_key = True)
    reduc_fidelite = models.IntegerField()
    class Meta:
        db_table = "fidelite"

class Responsable(models.Model):
    email           = models.EmailField(primary_key = True)
    password        = models.CharField(max_length= 30)
    num_client      = models.ForeignKey(Client, db_column = "num_client",
                                                on_delete = models.CASCADE)
    points_fidelite = models.ForeignKey(Fidelite, db_column = "points_fidelite",
                                        on_delete = models.CASCADE)
    num_reservation = models.ForeignKey(Reservation,
                                        db_column = "num_reservation",
                                        on_delete = models.CASCADE)
    id_profil       = models.ForeignKey(Profil, db_column = "id_profil",
                                        on_delete = models.CASCADE)
    class Meta:
        db_table = "responsable"

class ReservationServices(models.Model):
    num_reservation = models.ForeignKey(Reservation,
                                        db_column = "num_reservation",
                                        on_delete = models.CASCADE)
    nom_service = models.ForeignKey(ServicesProposes,
                                         db_column = "nom_service",
                                         on_delete = models.CASCADE)
    class Meta:
        db_table = "reservation_services"
        unique_together = (("num_reservation", "nom_service"),)



class Employe(models.Model):
    id_employe      = models.AutoField(primary_key = True)
    nom_employe     = models.CharField(max_length = 30)
    prenom_employe  = models.CharField(max_length = 30)
    activite        = models.CharField(max_length = 30)
    adresse_employe = models.CharField(max_length = 30)
    telephone       = models.IntegerField()
    email           = models.EmailField()
    password        = models.CharField(max_length = 30)
    salaire         = models.DecimalField(max_digits = 4,decimal_places = 2)
    class Meta:
        db_table = "employe"

class Facture(models.Model):
    num_facture     = models.AutoField(primary_key = True)
    date_emission   = models.DateField()
    num_reservation = models.ForeignKey(Reservation,
                                        db_column = "num_reservation",
                                        on_delete = models.CASCADE)
    id_employe      = models.ForeignKey(Employe,
                                        db_column = "id_employe",
                                        on_delete = models.CASCADE)
    class Meta:
        db_table = "facture"

class Sport(models.Model):
    nom_sport   = models.CharField(primary_key = True, max_length = 30)
    tarif_unite = models.DecimalField(max_digits = 10, decimal_places = 2)
    class Meta:
        db_table = "sport"

class ClientSport(models.Model):
    nom_sport  = models.ForeignKey(Sport, db_column = "nom_sport",
                                    on_delete = models.CASCADE)
    num_client = models.ForeignKey(Client, db_column = "num_client",
                                    on_delete = models.CASCADE)
    unite_location = models.IntegerField()
    class Meta:
        db_table = "client_sport"
        unique_together = (("nom_sport", "num_client"),)

class Materiel(models.Model):
    nom_materiel = models.CharField(max_length = 30, primary_key = True)
    qte_materiel = models.IntegerField()
    class Meta:
        db_table = "materiel"

class Intervenant(models.Model):
    id_intervenant     = models.AutoField(primary_key = True)
    nom_intervenant    = models.CharField(max_length = 30)
    prenom_intervenant = models.CharField(max_length = 30)
    salaire            = models.DecimalField(max_digits = 4,decimal_places = 2)
    class Meta:
        db_table = "intervenant"

class SportIntervenant(models.Model):
    nom_sport      = models.ForeignKey(Sport, db_column = "nom_sport",
                                        on_delete = models.CASCADE)
    id_intervenant = models.ForeignKey(Intervenant,
                                        db_column = "id_intervenant",
                                        on_delete = models.CASCADE)
    class Meta:
        db_table = "sport_intervenant"
        unique_together = (("nom_sport", "id_intervenant"),)

class SportMateriel(models.Model):
    nom_materiel = models.ForeignKey(Materiel, db_column = "nom_materiel",
                                     on_delete = models.CASCADE)
    nom_sport    = models.ForeignKey(Sport, db_column = "nom_sport",
                                     on_delete = models.CASCADE)
    class Meta:
        db_table = "sport_materiel"
        unique_together = (("nom_materiel", "nom_sport"),)

class SalleDesJeux(models.Model):
    ref_jeu  = models.AutoField(primary_key = True)
    nom_jeu  = models.CharField(max_length = 30)
    prix_jeu = models.DecimalField(max_digits = 3, decimal_places = 2)
    class Meta:
        db_table = "salle_des_jeux"

class ClientSalleDesJeux(models.Model):
    num_client = models.ForeignKey(Client, db_column = "num_client",
                                    on_delete = models.CASCADE)
    ref_jeu    = models.ForeignKey(SalleDesJeux, db_column = "ref_jeu",
                                    on_delete = models.CASCADE)
    qte        = models.IntegerField()
    class Meta:
        db_table = "client_salle_des_jeux"
        unique_together = (("num_client", "ref_jeu"),)

class ProduitSuperette(models.Model):
    ref_produit  = models.AutoField(primary_key = True)
    nom_produit  = models.CharField(max_length = 30)
    prix_produit = models.DecimalField(max_digits = 3, decimal_places = 2)
    class Meta:
        db_table = "produit_superette"

class ClientProduitSuperette(models.Model):
    num_client   = models.ForeignKey(Client, db_column = "num_client",
                                    on_delete = models.CASCADE)
    ref_produit  = models.ForeignKey(ProduitSuperette,
                                     db_column = "ref_produit",
                                     on_delete = models.CASCADE)
    qte          = models.IntegerField()
    class Meta:
        db_table = "client_produit_superette"
        unique_together = (("num_client", "ref_produit"),)

class Karaoke(models.Model):
    ref_salle     = models.AutoField(primary_key = True)
    date          = models.DateTimeField()
    tarif_karaoke = models.DecimalField(max_digits = 3, decimal_places = 2)
    class Meta:
        db_table = "karaoke"

class ClientKaraoke(models.Model):
    num_client = models.ForeignKey(Client, db_column = "num_client",
                                   on_delete = models.CASCADE)
    ref_salle    = models.ForeignKey(Karaoke, db_column = "ref_salle",
                                     on_delete = models.CASCADE)
    nbr_heures  = models.IntegerField()
    class Meta:
        db_table = "client_karaoke"
        unique_together = (("num_client", "ref_salle"),)

class CafeBar(models.Model):
    ref_conso  = models.AutoField(primary_key = True)
    nom_conso  = models.CharField(max_length = 30)
    prix_conso = models.DecimalField(max_digits = 3, decimal_places = 2)
    class Meta:
        db_table = "cafe_bar"

class ClientCafeBar(models.Model):
    num_client = models.ForeignKey(Client, db_column = "num_client",
                                   on_delete = models.CASCADE)
    ref_conso    = models.ForeignKey(CafeBar, db_column = "ref_conso",
                                     on_delete = models.CASCADE)
    qte_conso    = models.IntegerField()
    class Meta:
        db_table = "client_cafe_bar"
        unique_together = (("num_client", "ref_conso"),)
