from django.db import models

class Produit(models.Model):
    compte = models.CharField(max_length=50)
    designation = models.CharField(max_length=255)
    quantite = models.FloatField(default=0)
    unite = models.CharField(max_length=50, blank=True)
    specification = models.TextField(blank=True)
    observation = models.TextField(blank=True)

    def __str__(self):
        return self.designation

class Fournisseur(models.Model):
    code_four = models.CharField(max_length=50, unique=True, verbose_name="Code Fournisseur")
    nom = models.CharField(max_length=100, verbose_name="Nom/Raison Sociale")
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    ville = models.CharField(max_length=50, blank=True, null=True)
    nif_ou_compte = models.CharField(max_length=50, blank=True, null=True, verbose_name="N° Compte Bancaire")
    montant_engage = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.code_four} - {self.nom}"

class AllocationBudget(models.Model):
    num_compte_principal = models.CharField(max_length=50, verbose_name="N° Compte Principale")
    num_sous_compte = models.CharField(max_length=50, verbose_name="N° Sous Compte")
    nom_attache = models.CharField(max_length=100, verbose_name="Attaché")
    comptes = models.CharField(max_length=50, verbose_name="Comptes")
    annee_ex = models.CharField(max_length=50, verbose_name="Année_EX")
    budget_primitive = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    libelle_sous_compte = models.CharField(max_length=255, verbose_name="Libellé")
    budget_mensuel = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    realisation_budget = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    mois = models.CharField(max_length=50, verbose_name="Mois")
    dbm_moins = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="DBM_Moins")
    dbm_ajout = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="DBM_Ajout")

    def __str__(self):
        return f"{self.comptes} - {self.mois}"

class Budget(models.Model):
    allocation = models.ForeignKey(AllocationBudget, on_delete=models.CASCADE, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX")
    compte = models.CharField(max_length=50, verbose_name="Comptes") # Gardé 'compte' pour ton admin
    libelle_compte = models.CharField(max_length=255, verbose_name="Libellé_compte")
    
    # Montants (Noms alignés avec ton admin actuel)
    prevision = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    montant_engage = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    montant_realise = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    reliquat = models.DecimalField(max_digits=18, decimal_places=2, default=0) # Gardé 'reliquat' pour ton admin
    
    # Ajouts pour les futurs calculs (Recettes/Paiements)
    quantite_recette = models.FloatField(default=0)
    montant_paye = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return self.libelle_compte

class Depense(models.Model):
    num_compte_principal = models.CharField(max_length=50, verbose_name="N° Compte Principale")
    num_sous_compte = models.CharField(max_length=50, verbose_name="N° Sous Compte")
    nom_attache = models.CharField(max_length=100, verbose_name="Attaché")
    comptes = models.CharField(max_length=50, verbose_name="Comptes")
    annee_ex = models.CharField(max_length=50, verbose_name="Année_EX")
    budget_primitive = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    libelle_sous_compte = models.CharField(max_length=255, verbose_name="Libellé")
    budget_mensuel = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    realisation_budget = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    fournisseur_nom = models.CharField(max_length=100, verbose_name="Fournisseur") # Texte simple dans WinDev
    mois = models.CharField(max_length=50, verbose_name="Mois")
    date = models.DateField(verbose_name="Date")

    def __str__(self):
        return f"Dépense {self.id} - {self.annee_ex}"

class DetailsDepense(models.Model):
    # LIAISONS (Contraintes WinDev)
    # Chaque détail appartient à une dépense
    depense_parente = models.ForeignKey(Depense, on_delete=models.CASCADE, verbose_name="IDDépenses")
    # Chaque détail est lié à une ligne du budget
    budget_ligne = models.ForeignKey('Budget', on_delete=models.CASCADE, verbose_name="IDbudget")
    
    # Champs issus de 'DetailsDepense.JPG'
    code_four = models.CharField(max_length=50, verbose_name="Code_four")
    date_depense = models.DateField(verbose_name="Date")
    num_depense = models.CharField(max_length=50, verbose_name="Numero")
    montant_depense = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total_engagement = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    reliquat = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    compte = models.CharField(max_length=50, verbose_name="Compte")
    objet_depense = models.TextField(verbose_name="Objet")
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX")

    def __str__(self):
        return f"Détail {self.num_depense} - {self.montant_depense}"



class Recette(models.Model):
    num_recette = models.IntegerField(verbose_name="N°Recette")
    date_recette = models.DateField(verbose_name="Date")
    montant_recette = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant")
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX")
    valide = models.BooleanField(default=False, verbose_name="Validé") # Type Interrupteur dans WinDev
    nom_totalisateur = models.CharField(max_length=50, verbose_name="Totalisateur")
    nom_service = models.CharField(max_length=50, verbose_name="Service demandeur")

    def __str__(self):
        return f"Recette {self.num_recette} ({self.annee_ex})"
    
class DetailsRecette(models.Model):
    # LIAISONS (Contraintes WinDev)
    # Chaque détail appartient à une recette
    recette_parente = models.ForeignKey(Recette, on_delete=models.CASCADE, verbose_name="IDRecette")
    # Chaque détail est lié à une ligne budgétaire
    budget_ligne = models.ForeignKey('Budget', on_delete=models.CASCADE, verbose_name="IDbudget")

    # Champs issus de 'DétailsRecette.JPG'
    designation = models.CharField(max_length=50, verbose_name="Désignation")
    quantite_recette = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Quantité")
    unite = models.CharField(max_length=50, verbose_name="Unité")
    prix_unitaire_ht = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Prix Unitaire HT")
    prix_unitaire_ttc = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Prix Unitaire TTC")
    nomenclature = models.CharField(max_length=50, verbose_name="Compte")
    source = models.CharField(max_length=50, verbose_name="Source")
    montant_ttc = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant TTC")
    reference_pieces = models.CharField(max_length=50, verbose_name="Référence_pièces")
    ipm = models.CharField(max_length=50, verbose_name="IPM")
    code_recette = models.CharField(max_length=50, verbose_name="Type de recette")
    nom_ipm = models.CharField(max_length=50, verbose_name="Nom_IPM")

    def __str__(self):
        return f"Détail {self.designation} - {self.montant_ttc}"
    
