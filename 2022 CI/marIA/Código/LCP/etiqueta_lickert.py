class etiqueta_lickert:
    def scalaLickert(valor):
        if valor >= 0 and valor < 0.25:
            return "Very Easy"
        elif valor >= 0.25 and valor< 0.5:
            return  "Easy"
        elif valor >= 0.5 and valor < 0.6:
            return "Neutral"
        elif valor >= 0.6 and valor <= 0.75:
            return "Difficult"
        elif valor > 0.75:
            return "Very Difficult"

