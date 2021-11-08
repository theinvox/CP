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

col_nom_cs = [[sg.Text(size=(1, 2))]]
for nom_cs, nom_cs_key in zip(NOM_CS, NOM_CS_KEY):
    if nom_cs_key in NOM_CS_CATEGORIE:
        col_nom_cs += [[sg.Text(nom_cs, size=(30, 1), justification='l', background_color='black'),
                        sg.Text(key=nom_cs_key, size=(15, 1), background_color='black', justification='c')]]
    else:
        col_nom_cs += [[sg.Text(nom_cs, size=(30, 1), justification='l'),
                        sg.Input(key=nom_cs_key, size=(17, 1), enable_events=True, justification='c')]]

col_prod = []
for prod in LISTE_PRODUCTION:
    crea_prod = [[sg.Text(prod, size=(len(prod), 2), justification='c')]]
    for nom_cs_key in NOM_CS_KEY:
        if nom_cs_key in NOM_CS_CATEGORIE:
            crea_prod += [[sg.Text('0', key=f'{prod}-{nom_cs_key}',
                                   background_color='black', size=(len(prod), 1), justification='c')]]
        else:
            crea_prod += [[sg.Input(key=f'{prod}-{nom_cs_key}', size=(len(prod) + 2, 1), justification='c')]]

    col_prod += [sg.Col(crea_prod, key=f'{prod}', visible=True)]

page = sg.Col([[sg.Col(col_nom_cs)] + [sg.Col([[sg.Text(' ', size=(2, 1))]])] + col_prod], scrollable=True, vertical_scroll_only=True)

window = sg.Window('Principale', [[page]], resizable=True, finalize=True)

while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WINDOW_CLOSED:
        break

window.close()
