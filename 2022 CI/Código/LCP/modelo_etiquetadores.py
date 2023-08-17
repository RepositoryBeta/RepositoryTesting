class modelo_etiquetadores:
    def definicionTipo(tipo):
        PROPN="PROPN"
        AUX="AUX"
        VERB="VERB"
        ADP="ADP"
        NOUN="NOUN"
        NN="NN"
        SYM="SYM"
        NUM="NUM"
        if tipo==VERB:
            return 0
        elif tipo==NOUN:
            return 1
        elif tipo==PROPN:
            return 2
        elif tipo==ADP:
            return 3
        elif tipo==AUX:
            return 4
        elif tipo==NN:
            return 5
        elif tipo==SYM:
            return 6
        elif tipo==NUM:
            return 7
        else:
            return 8
       
        
