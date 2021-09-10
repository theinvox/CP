import PySimpleGUI as sg
liste = ['a', 'b']
nb_col = 0
ajout_ligne = None

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

LISTE_PRODUCTION = ['Vaches laitières', 'Porcs N-E', 'Vaches allaitantes', 'Poules pondeuses']


# def ligne_cs(nom_cs, nom_cs_key, nom_prod):
#     """
#     Fonction qui permet d'afficher la répartition pour chaque production et types de charges sur une ligne
#     Ajout d'une case à cocher pour
#     :param nom_prod: Nom de la production
#     :param nom_cs_key: Nom de clé utilisé
#     :return: Renvoi la ligne contenant le couple (production, nom de la clé)
#     """
#     ligne = []
#     if nom_cs_key in NOM_CS_CATEGORIE:
#         ligne += [sg.Text(nom_cs, size=(33, 1), justification='l', background_color='black'),
#                   sg.Text(key=nom_cs_key, size=(15, 1), background_color='black', justification='c')]
#     else:
#         ligne += [sg.Text(nom_cs, size=(33, 1), justification='l'),
#                   sg.Input(key=nom_cs_key, size=(17, 1), enable_events=True, justification='c')]
    #
    # ligne += [sg.VerticalSeparator()]

#     for prod in nom_prod:
#         if nom_cs_key in NOM_CS_CATEGORIE:
#             ligne += [sg.Text('0', size=(len(prod), 1), justification='c', key=(prod, nom_cs_key),
#                               background_color='black', text_color='white')]
#         else:
#             ligne += [
#                 sg.Input('0', size=(len(prod)+2, 1), justification='c', key=(prod, nom_cs_key), disabled=True,
#                          text_color='black', enable_events=True)]
#
#     if nom_cs_key not in NOM_CS_CATEGORIE:
#         ligne += [sg.Checkbox('', enable_events=True, pad=((0, 0), (0, 0)), key=('modif', nom_cs_key))]
#
    # return ligne

col_nom_cs = []
for nom_cs, nom_cs_key in zip(NOM_CS, NOM_CS_KEY):
    if nom_cs_key in NOM_CS_CATEGORIE:
        col_nom_cs += [[sg.Text(nom_cs, size=(33, 1), justification='l', background_color='black'),
                   sg.Text(key=nom_cs_key, size=(15, 1), background_color='black', justification='c')]]
    else:
        col_nom_cs += [[sg.Text(nom_cs, size=(33, 1), justification='l'),
                   sg.Input(key=nom_cs_key, size=(17, 1), enable_events=True, justification='c')]]


page = sg.Col([[sg.Col(col_nom_cs)] + [sg.Col([[sg.Text(' '*5)] for i in range(32)])]],

              scrollable=True, vertical_scroll_only=True)

window = sg.Window('Principale', [[page]], resizable=True, finalize=True)

while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WINDOW_CLOSED:
        break

window.close()
