import PySimpleGUI as sg
from math import trunc
import csv

# Variable fixe
SIZE_INPUT = (10, 1)
SIZE_NOM_CV = SIZE_SUR_CV = SIZE_RDT_CV = (10, 1)
# Variable fixe
LISTE_CULTURE = ['Blé', 'Orge', 'Maïs', 'Avoine', 'Colza', 'Sarasin']
LISTE_FOURRAGE = ['Prairies permanentes', 'Prairies temporaires', 'Maïs ensilage', 'Sorgho', 'Parcs']
LISTE_ANIMAUX = []  # liste des productions animales
DIC_UNITE_ANIMAUX = {}  # liste des unités des productions animales
cle_repartition = {}  # dictionnaire contenant les références de base
cle_repartition_unite = {}  # dictionnaire contenant les références en fonction de leur unité

# Variable mobile
cv = 0  # utilisé pour ajouter des cultures
cf = 0  # utilisé pour ajouter des fourrages
prod_ani = 0  # utilisé pour ajouter des productions animales
sau_vente = 0  # utilisé pour afficher la surface culture de vente
sau_fourrage = 0  # utilisé pour afficher la surface fourragère
sau_total = 0  # utilisé pour afficher la surface total
crea_tableau = True

CS_charges = {}
CS_coefficient = {}


# Valeur constante
NOM_CS = ['Fermages et charges locatives', 'Entretien et amendements', 'Impôts fonciers', 'Foncier',
          'Loyer et charges locatives', 'Entretiens et réparations', 'Bâtiments',
          'Locations matériels et recours au tiers', 'Carburants et lubrifiants', 'Entretien, réparation petits matériels', 'Var. frais de méca', 'Mécanisation',
          'Charges salariales', 'Charges sociales exploitants', 'Main d\'oeuvre',
          'Eau, gaz, EDF', 'Autres fournitures', 'Assurances', 'Intermédiaires et honoraires', 'Transports et déplacements', 'Impôts et taxes', 'Autres charges', 'Autres charges de structure',
          'Intérêts des emprunts +1 an', 'Intérêts des emprunts -1 an', 'Autres charges financières', 'Charges financières',
          'Améliorations foncières', 'Constructions', 'Matériels et installations', 'Autres', 'Amortissements',
          'Total']

NOM_CS_CATEGORIE = ['FONC', 'BATI', 'MECA', 'MO', 'AUTRES_CS', 'CHARGES_FI', 'AMORTISSEMENTS', 'TOTAL_CS']

NOM_CS_KEY = ['FONC_LOC', 'FONC_ENTRETIEN', 'FONC_IMPOTS', 'FONC',
              'BATI_LOC', 'BATI_ENTRETIEN', 'BATI',
              'MECA_LOC', 'MECA_CARBU', 'MECA_ENTRETIEN', 'MECA_VAR', 'MECA',
              'MO_SALARIE', 'MO_EXPLOIT', 'MO',
              'AUTRES_EAU', 'AUTRES_FOURNI', 'AUTRES_ASSU', 'AUTRES_HONO', 'AUTRES_DPLTS', 'AUTRES_IMPOTS', 'AUTRES_CHARGES', 'AUTRES_CS',
              'INTERET+1', 'INTERET-1', 'AUTRES_CHARGES_FI', 'CHARGES_FI',
              'AMOR_FONCIER', 'AMOR_CONSTRUCTION', 'AMOR_MATERIELS', 'AMOR_AUTRES', 'AMORTISSEMENTS',
              'TOTAL_CS']

# TODO : création du module pour faire la répartition automatiquement
Foncier = [0.5, 0.5]
Batiment = [0.5, 0.5]
Mecanisation = [0.5, 0.5]
MO = [0.5, 0.5]
Autres_CS = [0.5, 0.5]
Frais_fi = [0.5, 0.5]
Amortissement = [0.5, 0.5]
Total = [0, 0]

repartition = [Foncier, Foncier, Foncier, Foncier, Batiment, Batiment, Batiment, Mecanisation,
               Mecanisation, Mecanisation, Mecanisation, Mecanisation, MO, MO, MO, Autres_CS, Autres_CS, Autres_CS,
               Autres_CS, Autres_CS, Autres_CS, Autres_CS, Autres_CS, Frais_fi, Frais_fi, Frais_fi, Frais_fi,
               Amortissement, Amortissement, Amortissement, Amortissement, Amortissement, Total]

# Variables non constante en exemple pour le test
# data_CS = [14497, 1922, 869, 0, 0, 2163, 0, 4465, 6778, 9365, -6289, 0, 35165, 11081, 0, 15767, 4865,
#            6407, 3797, 255, 1196, 2373, 0, 589, 197, 16, 0, 0, 1302, 15573, 0, 0, 0]

NOM_PRODUCTION = []

########################################################################################################################
                                ### FONCTIONS NECESSAIRES POUR LA PAGE DESCRIPTIF ###
########################################################################################################################
# création des fonctions nécessaires
def surface_vente(nb_culture):
    """
    mise en page automatique de l'ajout d'une culture
    :param nb_culture: indentation automatique pour actualiser les clés
    :return: format de présentation des cultures
    """
    return [[sg.Combo(LISTE_CULTURE, key=f'-CULTURE_VENTE{nb_culture}-', size=SIZE_NOM_CV, enable_events=True),
             sg.Input(size=SIZE_SUR_CV, key=f'-SURFACE_VENTE{nb_culture}-', enable_events=True), sg.Text('ha'),
             sg.Input(size=SIZE_RDT_CV, key=f'-RENDEMENT_VENTE{nb_culture}-', enable_events=True), sg.Text('T')]]


def surface_fourragere(nb_fourrage):
    """
    mise en page automatique de l'ajout d'un fourrage
    :param nb_fourrage: indentation automatique pour actualiser les clés
    :return: format de présentation des fourrages
    """
    return [[sg.Combo(LISTE_FOURRAGE, key=f'CULTURE_FOURRAGERE{nb_fourrage}', enable_events=True),
             sg.Input(size=SIZE_INPUT, key=f'SURFACE_FOURRAGERE{nb_fourrage}', enable_events=True), sg.Text('ha')]]


def ajout_prod_anx(valeur_liste, prod_ani):
    """
    mise en page automatique d'une production
    :param valeur_liste: valeur saisie dans la liste des productions
    :param prod_ani: indentation automatique pour actualiser les clés
    :return: format de présentation d'une production animale
    """
    def popup_autre():
        """
        création d'une fenêtre de saisie d'une production non existante
        :return: dictionnaire contenant le nom de la production et des valeurs d'analyse
        """
        layout1 = [[sg.Text('Nom de la production'), sg.Input(key='NOM_AUTRE')],
                   [sg.Text('Critère d\'analyse'), sg.Input(key='ANA')],
                   [sg.Button('Valider')]]

        fenetre_saisie = sg.Window('Ajout autre production', layout1, finalize=True)

        while True:
            event, values = fenetre_saisie.read()
            # condition qui permet de créer le dictionnaire prod_autre. Si faux, ferme la fenêtre
            prod_autre = {}
            if event == 'Valider':
                prod_autre[values['NOM_AUTRE']] = [values['ANA']]
                break
            elif event == sg.WIN_CLOSED:
                prod_autre = {}
                break
        fenetre_saisie.close()
        return prod_autre

    ligne = []
    if valeur_liste == 'Autre production':
        d_autre = popup_autre()
        if d_autre != {}:
            d_autre_indice = list(d_autre.keys())[0]
            DIC_UNITE_ANIMAUX.update(d_autre)
            ligne = [sg.Text(f'{d_autre_indice}', key=f'ANI_PROD{prod_ani}', size=(25, 1)),
                      sg.Text('Produit brut'), sg.Input(size=SIZE_INPUT, key=f'ANI_REP_CS{prod_ani}', enable_events=True), sg.Text('euros'),
                      sg.Input(size=SIZE_INPUT, key=f'ANI_ANA{prod_ani}', enable_events=True), sg.Text(DIC_UNITE_ANIMAUX[d_autre_indice][0])]
    elif valeur_liste in LISTE_ANIMAUX:
        ligne = [sg.Text(f'{valeur_liste}', key=f'ANI_PROD{prod_ani}', size=(25, 1)),
                  sg.Input(size=SIZE_INPUT, key=f'ANI_REP_CS{prod_ani}', enable_events=True), sg.Text(DIC_UNITE_ANIMAUX[valeur_liste][0], size=(10, 1)),
                  sg.Input(size=SIZE_INPUT, key=f'ANI_ANA{prod_ani}', enable_events=True), sg.Text(DIC_UNITE_ANIMAUX[valeur_liste][1], size=(15, 1))]
        if valeur_liste not in ('Porcs naisseur-engr.', 'Porcs PS E', 'Volailles standard'):
            ligne += [sg.Input(size=SIZE_INPUT, key=f'ANI_SURF{prod_ani}', enable_events=True), sg.Text('ha')]
        else:
            ligne += [sg.Input(0, size=SIZE_INPUT, key=f'ANI_SURF{prod_ani}', enable_events=True, visible=False)]

    return [ligne]

########################################################################################################################
                        ### FONCTIONS NECESSAIRES POUR LA PAGE CHARGES DE STRUCTURE ###
########################################################################################################################
# fonction de somme pour chaque catégories
def somme_foncier(prod):
    return CS_charges['FONC_LOC'][prod] + CS_charges['FONC_ENTRETIEN'][prod] + CS_charges['FONC_IMPOTS'][prod]
def somme_batiment(prod):
    return CS_charges['BATI_LOC'][prod] + CS_charges['BATI_ENTRETIEN'][prod]
def somme_mecanisation(prod):
    return CS_charges['MECA_LOC'][prod] + CS_charges['MECA_CARBU'][prod] + CS_charges['MECA_ENTRETIEN'][prod] + CS_charges['MECA_VAR'][prod]
def somme_mo(prod):
    return CS_charges['MO_SALARIE'][prod] + CS_charges['MO_EXPLOIT'][prod]
def somme_autres_cs(prod):
    return CS_charges['AUTRES_EAU'][prod] + CS_charges['AUTRES_FOURNI'][prod] + CS_charges['AUTRES_ASSU'][prod] + CS_charges['AUTRES_HONO'][prod] + CS_charges['AUTRES_DPLTS'][prod] + CS_charges['AUTRES_IMPOTS'][prod] + CS_charges['AUTRES_CHARGES'][prod]
def somme_charges_fi(prod):
    return CS_charges['INTERET+1'][prod] + CS_charges['INTERET-1'][prod] + CS_charges['AUTRES_CHARGES_FI'][prod]
def somme_ammortissement(prod):
    return CS_charges['AMOR_FONCIER'][prod] + CS_charges['AMOR_CONSTRUCTION'][prod] + CS_charges['AMOR_MATERIELS'][prod] + CS_charges['AMOR_AUTRES'][prod]
def somme_total(prod):
    return somme_foncier(prod) + somme_batiment(prod) + somme_mo(prod) + somme_mecanisation(prod) + somme_autres_cs(prod) + somme_charges_fi(prod) + somme_ammortissement(prod)

# fonction affichage de ligne
def ligne_cs(nom_prod, nom_cs_key):
    """
    Fonction qui permet d'afficher la répartition pour chaque production et types de charges sur une ligne
    Ajout d'une case à cocher pour
    :param nom_prod: Nom de la production
    :param nom_cs_key: Nom de clé utilisé
    :return: Renvoi la ligne contenant le couple (production, nom de la clé)
    """
    ligne = []
    for prod in nom_prod:
        if nom_cs_key in NOM_CS_CATEGORIE:
            ligne += [sg.Text('0', size=(len(prod), 1), justification='c', key=(prod, nom_cs_key), background_color='black', text_color='white')]
        else:
            ligne += [sg.Input('0', size=(len(prod), 1), justification='c', key=(prod, nom_cs_key), disabled=True, text_color='black', enable_events=True)]

    if nom_cs_key not in NOM_CS_CATEGORIE:
        ligne += [sg.Checkbox('', enable_events=True, pad=((0, 0), (0, 0)), key=('modif', nom_cs_key))]

    return ligne

# création de la colonne nom CS et saisie des CS
def ligne_nom_cs(nom_cs, nom_cs_key):
    ligne = []
    if nom_cs_key in NOM_CS_CATEGORIE:
        ligne += [sg.Text(nom_cs, size=(33, 1), justification='l', background_color='black'), sg.Text(key=nom_cs_key, size=(15, 1), background_color='black', justification='c')]
    else:
        ligne += [sg.Text(nom_cs, size=(33, 1), justification='l'), sg.Input(key=nom_cs_key, size=(15, 1), enable_events=True, justification='c')]

    ligne += [sg.Text('', size=(5, 1))]

    return ligne


# Fonction de test des valeurs
def test_valeur(valeur):
    try:
        value = int(valeur)
    except ValueError or TypeError:
       value = 0
    return value


def calcul_unite(prod, indice):
    somme = (float(cle_repartition[prod][0]) * float(cle_repartition[prod][indice])
             - float(cle_repartition[prod][2]) * float(cle_repartition['Cultures de vente'][indice])) / float(cle_repartition[prod][3])
    return round(somme, 2)

# importation du fichier de référence pour la répartion des CS
with open('Reference_repartition_CS.csv', newline='', encoding='utf8') as csvfile:
    lecture = csv.reader(csvfile)
    for row in lecture:
        cle_repartition[row[0]] = row[1:12]
        LISTE_ANIMAUX.append(row[0])
        DIC_UNITE_ANIMAUX[row[0]] = ([row[5], row[12]])
    del LISTE_ANIMAUX[0], DIC_UNITE_ANIMAUX['intitulé'], cle_repartition['intitulé']

# création du dictionnaire des références en fonction de leur unité
for cle in cle_repartition.keys():
    cle_repartition_unite[cle] = []
    for i in range(5, 11):
        if cle == 'Autre production':
            cle_repartition_unite[cle].append(cle_repartition[cle][i])
        else:
            cle_repartition_unite[cle].append(calcul_unite(cle, i))


# affichage
sg.theme('BluePurple')  # thème des fenêtres

########################################################################################################################
# page descriptif
########################################################################################################################
ajout = [[sg.Col([[sg.Button('+', key='-B1-', disabled=False), sg.Text("Ajout d'une culture de vente"), sg.Button('+', key='-B2-', disabled=False),
                   sg.Text("Ajout d'une culture fourragère")],
                  [sg.Text()],
                  [sg.Text("Ajout d'une production animal"), sg.Combo(values=LISTE_ANIMAUX[1:], size=(30, len(LISTE_ANIMAUX[1:])), key='-SELECT_PROD-', readonly=True, enable_events=True),
                   sg.Button('Ajouter', key='-AJOUTER-', disabled=False)]]),
          sg.Col([[sg.Text(f'Surface totale: {sau_total} ha', key='-SAU_TOT-', size=(40, 1), text_color='white', background_color='blue')],
                  [sg.Text(f'Surface de ventes : {sau_vente} ha', key='-SAU_VENTE-', size=(40, 1), text_color='white', background_color='blue')],
                  [sg.Text(f'Surfaces fourragères : {sau_fourrage} ha', key='-SAU_FOURRAGE-', size=(40, 1), text_color='white', background_color='blue')]],
                 background_color='blue')]]

culture = [[sg.Text()],
           [sg.Col([[sg.Text('DESCRIPTIF DES CULTURES DE VENTE', size=(50, 1))]], key='CULTURE_VENTE', vertical_alignment='top'),
            sg.VerticalSeparator(),
            sg.Col([[sg.Text('DESCRIPTIF DES SURFACES FOURRAGERES', size=(50, 1))]], key='CULTURE_FOURRAGERE', vertical_alignment='top')]]

production_animale = [[sg.Col([[sg.Text()],
                               [sg.Text('DESCRIPTIF DES PRODUCTIONS ANIMALES', size=(50, 1))],
                               [sg.Text('Nom de la production', size=(25, 1), justification='c'),
                                sg.Text('Unité répartition CS', size=(20, 1), justification='c'),
                                sg.Text('Unité d\'analyse', justification='c', size=(25, 1)),
                                sg.Text('Répartition surface fourragère')]], key='PRODUCTION_ANIMALE')]]

window_descriptif = [sg.Tab('Coût de production', [[sg.Col(ajout + culture + production_animale, key='-DESCRIPTIF-')]])]

########################################################################################################################
# page charges de structure
########################################################################################################################
col_CS = [sg.Col([[sg.Text('', size=(1, 2))]] + [ligne_nom_cs(nom_cs, cs_key) for nom_cs, cs_key in zip(NOM_CS, NOM_CS_KEY)])]
col_CS_prod = [sg.Col([[]], key='col_cs_prod')]

window_cs = [sg.Tab('Charges de structure', [[sg.Col([col_CS + col_CS_prod], scrollable=False, vertical_scroll_only=True, key='TABCS')]])]

########################################################################################################################
# affichage des différentes pages
########################################################################################################################

window = sg.Window('Principale', [[sg.TabGroup([window_descriptif + window_cs], key='TABGROUP', enable_events=crea_tableau)]], resizable=True, finalize=True)
# window['TABCS'].update(expand_y=True, expand_x=True)
# window['TABGROUP'].update(expand_y=True, expand_x=True)

while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WINDOW_CLOSED:
        break

########################################################################################################################
                                ### FONCTIONS NECESSAIRES POUR LA PAGE DESCRIPTIF ###
########################################################################################################################
    # calcul automatique de la surface de vente et mise à jour automatique
    sau_vente = 0
    for i in range(cv):
        try:
            sau_vente += float(values[f'-SURFACE_VENTE{i}-'])
        except ValueError or TypeError:
            sau_vente += 0
    window['-SAU_VENTE-'].update(f'Surface de ventes : {sau_vente} ha')

    # calcul automatique de la surface fourragère et mise à jour automatique
    sau_fourrage = 0
    for i in range(cf):
        try:
            sau_fourrage += float(values[f'SURFACE_FOURRAGERE{i}'])
        except ValueError or TypeError:
            sau_fourrage += 0
    window['-SAU_FOURRAGE-'].update(f'Surfaces fourragères : {sau_fourrage} ha')

    # calcul de la SAU total et actualisation automatique
    sau_total = sau_fourrage + sau_vente
    window['-SAU_TOT-'].update(f'Surface totale: {sau_total} ha')

    # vérification de la somme des surfaces fourragères répartis
    sau_rep_fourrage = 0
    for i in range(prod_ani):
        try:
            sau_rep_fourrage += float(values[f'ANI_SURF{i}'])
        except ValueError or TypeError:
            sau_rep_fourrage += 0

    # affichage de la vérification dans la fenêtre
    for i in range(prod_ani):
        if sau_rep_fourrage != sau_fourrage:
            window[f'ANI_SURF{i}'].update(background_color='red')
            window[f'ANI_SURF{i}'].set_tooltip('La surface ne correspond pas au total ')
        else:
            window[f'ANI_SURF{i}'].update(background_color='white')
            window[f'ANI_SURF{i}'].set_tooltip('')

    # création automatique des cultures de vente
    if event == '-B1-' and cv < 10:
        window.extend_layout(window['CULTURE_VENTE'], surface_vente(cv))
        cv += 1
    elif cv == 10:
        window['-B1-'].update(disabled=True)

    # création automatique des fourrages
    if event == '-B2-' and cf < 10:
        window.extend_layout(window['CULTURE_FOURRAGERE'], surface_fourragere(cf))
        cf += 1
    elif cf == 10:
        window['-B2-'].update(disabled=True)

    # création automatique des productions animales
    if event == '-AJOUTER-' and prod_ani < 10:
        if values['-SELECT_PROD-'] == '':
            pass
        elif values['-SELECT_PROD-'] == 'Cultures de vente':
            pass
        else:
            window.extend_layout(window['PRODUCTION_ANIMALE'], ajout_prod_anx(values['-SELECT_PROD-'], prod_ani))
            prod_ani += 1
    elif prod_ani == 10:
        window['-AJOUTER-'].update(disabled=True)

    # création du dictionnaire contenant les valeurs saisies
    saisie = {'cv': [], 'cf': [], 'animaux': [], 'sau_vente': sau_vente, 'sau_fourrage': sau_fourrage, 'sau_total': sau_total}

    if event != '-B1-':
        i = 0
        while i < cv:
            saisie['cv'].append([values[f'-CULTURE_VENTE{i}-'], values[f'-SURFACE_VENTE{i}-'], values[f'-RENDEMENT_VENTE{i}-']])
            i += 1

    if event != '-B2-':
        i = 0
        while i < cf:
            saisie['cf'].append([values[f'CULTURE_FOURRAGERE{i}'], values[f'SURFACE_FOURRAGERE{i}']])
            i += 1

    if event != '-AJOUTER-':
        i = 0
        while i < prod_ani:
            saisie['animaux'].append([window[f'ANI_PROD{i}'].get(), values[f'ANI_REP_CS{i}'], values[f'ANI_ANA{i}'], values[f'ANI_SURF{i}']])
            i += 1

########################################################################################################################
                        ### FONCTIONS NECESSAIRES POUR LA PAGE CHARGES DE STRUCTURE ###
########################################################################################################################
    # dictionnaire des valeurs saisies dans la colonne totale
    # for nom_cs in NOM_CS_KEY:
    #     if nom_cs not in NOM_CS_CATEGORIE:
    #         CS_charges[nom_cs] = [test_valeur(values[nom_cs])]

    # dictionnaire des coefficients pour la pré répartition
    # TODO a revoir en fonction de la répartition des productions
    for nom_cs, coef in zip(NOM_CS_KEY, repartition):
        if nom_cs not in NOM_CS_CATEGORIE:
            CS_coefficient[nom_cs] = coef

    # # modification de la valeur en fonction de la case coché ou non
    # # ajout dans le dictionnaire CS_charges des valeurs saisies ou des valeurs calculées en fonction du coefficient
    # for cle in NOM_CS_KEY:
    #     if cle not in NOM_CS_CATEGORIE:
    #         for prod, num_prod in zip(NOM_PRODUCTION, range(len(NOM_PRODUCTION))):
    #             if values[('modif', cle)] is True:
    #                 window[(prod, cle)].update(disabled=False)
    #                 CS_charges[cle].append(test_valeur(values[(prod, cle)]))
    #             else:
    #                 window[(prod, cle)].update(disabled=True)
    #                 CS_charges[cle].append(trunc(CS_coefficient[cle][num_prod] * CS_charges[cle][0]))
    #
    # # changement de la couleur de l'arrière plan de l'input et vérification de la somme total
    # for cat in NOM_CS_KEY:
    #     if cat not in NOM_CS_CATEGORIE and values[('modif', cat)] is True:
    #         verif = 0
    #         for prod in range(1, len(NOM_PRODUCTION) + 1):
    #             verif += CS_charges[cat][prod]
    #         for nom_prod in NOM_PRODUCTION:
    #             if verif == CS_charges[cat][0]:
    #                 window[(nom_prod, cat)].update(background_color='green', text_color='black')
    #             else:
    #                 window[(nom_prod, cat)].update(background_color='blue', text_color='black')
    #
    # # ajout des totaux dans le dictionnaire CS_charges
    # for prod in range(len(NOM_PRODUCTION)+1):
    #     if prod == 0:
    #         CS_charges['FONC'] = [somme_foncier(prod)]
    #         CS_charges['BATI'] = [somme_batiment(prod)]
    #         CS_charges['MECA'] = [somme_mecanisation(prod)]
    #         CS_charges['MO'] = [somme_mo(prod)]
    #         CS_charges['AUTRES_CS'] = [somme_autres_cs(prod)]
    #         CS_charges['CHARGES_FI'] = [somme_charges_fi(prod)]
    #         CS_charges['AMORTISSEMENTS'] = [somme_ammortissement(prod)]
    #         CS_charges['TOTAL_CS'] = [somme_total(prod)]
    #     else:
    #         CS_charges['FONC'].append(somme_foncier(prod))
    #         CS_charges['BATI'].append(somme_batiment(prod))
    #         CS_charges['MECA'].append(somme_mecanisation(prod))
    #         CS_charges['MO'].append(somme_mo(prod))
    #         CS_charges['AUTRES_CS'].append(somme_autres_cs(prod))
    #         CS_charges['CHARGES_FI'].append(somme_charges_fi(prod))
    #         CS_charges['AMORTISSEMENTS'].append(somme_ammortissement(prod))
    #         CS_charges['TOTAL_CS'].append(somme_total(prod))
    #
    # # affiche des colonnes productions dans le tableau final
    # for cat in NOM_CS_KEY:
    #     for nom_prod, prod in zip(NOM_PRODUCTION, range(1, len(NOM_PRODUCTION)+1)):
    #         if cat in NOM_CS_CATEGORIE:
    #             window[(nom_prod, cat)].update(CS_charges[cat][prod])
    #         else:
    #             if values[('modif', cat)] is False:
    #                 window[(nom_prod, cat)].update(CS_charges[cat][prod])
    #
    # # affichage de la somme par catégorie dans le tableau final
    # for cat in NOM_CS_CATEGORIE:
    #     window[cat].update(CS_charges[cat][0])

    ####################################################################################################################
                                                    # partie de test #
    ####################################################################################################################
    for i in saisie['animaux']:
        NOM_PRODUCTION.append(i[0])
    if event == 'TABGROUP':
        if NOM_PRODUCTION:
            entete = [sg.Text(nom_prod, size=(len(nom_prod), 2), justification='c') for nom_prod in NOM_PRODUCTION]
            col_CS_prod = [ligne_cs(NOM_PRODUCTION, nom_cs_key) for nom_cs_key in NOM_CS_KEY]
            window.extend_layout(window['col_cs_prod'], [entete] + col_CS_prod)
            crea_tableau == False



window.close()
