from sys import argv

def verif_code(ligne):
    """
    Vérifie si le code n'est pas erroné
    """
    count_crochet = 0
    count_case = 0
    for elem in ligne:
        if elem == '[':
            count_crochet += 1
        elif elem == '>':
            count_case +=1
        elif elem == ']':
            count_crochet -= 1
        elif elem == '<':
            count_case -= 1
        if count_crochet < 0:
            raise ValueError("Il y a un problème avec le nombre de" + \
                             " crochet fermant")
        elif count_case < 0:
            raise ValueError("Il y a un problème avec le nombre de" + \
                             " case")
    if count_crochet != 0:
        raise ValueError("Il y a un problème avec le nombre de" + \
                                 " crochet ouvrant")

def execution(ret, elem, n_case):
    """
    Exécute les éléments donnés
    """
    if elem == '>':
        n_case +=1
    elif elem == '<' and n_case != 0:
        n_case -= 1
    elif elem == '+':
        ret[n_case] += 1
    elif elem == '-':
        ret[n_case] -= 1
    elif elem == ',':
        ret[n_case] = int(input("Valeur de l'octet actuel"))
    elif elem == '.':
        print(chr(ret[n_case]), end='')
    return n_case, ret

def chemin_fichier(fichier):
    """
    Ouvre le fichier et mets tout sur une ligne
    """
    try:
        f = open(fichier)
    except IOError as error:
        print("Impossible d'ouvrir ce fichier")
        raise error
    ligne = " ".join(line.strip() for line in f.readlines()).replace(" ", "")
    #Vérification si le code n'est pas erroné
    verif_code(ligne)
    return ligne
    
def action_boucle(ligne, ret, elem, n_case, dans_boucle, nb_crochet, ok):
    """
    Une fois dans la boucle dû à un '[', on boucle donc et une fois qu'un
    ']' apparaît, ça marque la fin de la boucle, et donc la partie entre les
    '[]' cycle
    """
    stock = ""
    decremente = dans_boucle.count('-')
    if ligne.index(elem) == ligne.find(']') - 1 and nb_crochet == 1 or not ok:
        #on supprime le premier élement, qui est un crochet
        dans_boucle = '' + dans_boucle[1:]
        for i in range(0, ret[n_case], decremente):
            for elem in dans_boucle:
                if elem != '[':
                    n_case, ret = execution(ret, elem, n_case)
                else:
                    ok = False
                    ret, n_case = action_boucle(ligne,
                                        ret,
                                        elem,
                                        n_case,
                                        dans_boucle[dans_boucle.find('['):
                                                      dans_boucle.find(']')],
                                        nb_crochet,
                                        ok
                                    )
    return ret, n_case

def main(argv):
    if len(argv) != 2:
        raise ValueError("Vous devez rentrez (uniquement) le nom du fichier" + \
                         " que vous voulez interpreter")
    BF = argv[1]
    ligne = chemin_fichier(BF)
    nbr_case = ligne.count('>')
    ret = nbr_case*[0]
    n_case = 0
    nb_boucle = 0
    nb_crochet = 0
    dans_boucle = ""
    for elem in ligne:
        ok = True
        boucle = True if nb_boucle != 0 else False
        if elem != '[' and not boucle:
            n_case, ret = execution(ret, elem, n_case)
            save = n_case
        else:
            if elem == '[':
                nb_boucle += 1
                nb_crochet += 1
            elif elem == ']':
                nb_boucle -= 1
                nb_crochet -= 1

            if ret[save] != 0:
                dans_boucle += elem
                ret, n_case = action_boucle(
                                    ligne,
                                    ret,
                                    elem,
                                    n_case,
                                    dans_boucle,
                                    nb_crochet,
                                    ok
                                )

if "__main__" == __name__:
    main(argv)