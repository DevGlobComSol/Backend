from django.contrib import admin
from .models import AllocationBudget, Depense, DetailsDepense, DetailsRecette, Fournisseur, Budget, Recette, Produit

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('code_four', 'nom', 'telephone', 'ville', 'montant_engage')
    search_fields = ('nom', 'code_four')
    list_filter = ('ville',)

@admin.register(AllocationBudget)
class AllocationBudgetAdmin(admin.ModelAdmin):
    list_display = ('annee_ex', 'mois', 'comptes', 'budget_primitive')
    list_filter = ('annee_ex', 'mois')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    # ATTENTION : 'compte' et 'reliquat' doivent exister dans models.py
    list_display = ('annee_ex', 'compte', 'libelle_compte', 'reliquat')
    list_filter = ('annee_ex',)
    search_fields = ('compte', 'libelle_compte')

@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'annee_ex', 'comptes', 'realisation_budget')

@admin.register(DetailsDepense)
class DetailsDepenseAdmin(admin.ModelAdmin):
    list_display = ('num_depense', 'date_depense', 'montant_depense', 'budget_ligne')
    list_filter = ('annee_ex', 'budget_ligne')

@admin.register(Recette)
class RecetteAdmin(admin.ModelAdmin):
    list_display = ('num_recette', 'date_recette', 'montant_recette', 'valide')

@admin.register(DetailsRecette)
class DetailsRecetteAdmin(admin.ModelAdmin):
    list_display = ('designation', 'montant_ttc', 'budget_ligne')