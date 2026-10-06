
class ComparacaoAgent:

    CAMPOS = {
        "seguradora": "Seguradora",
        "vigencia": "Vigência",
        "limite_agregado": "Limite agregado",
        "franquia": "Franquia",
        "abrangencia_territorial": "Abrangência territorial",
        "base_contratacao": "Base de contratação",
        "sublimites": "Sublimites",
        "exclusoes": "Exclusões",
        "prazo_adicional_notificacao": "Prazo adicional de notificação",
        "retroatividade": "Data de retroatividade",
    }

    def comparar(self, apolice_a, apolice_b):
        resultado = []

        for campo, nome in self.CAMPOS.items():
            valor_a = apolice_a.get(campo)
            valor_b = apolice_b.get(campo)

            resultado.append({
                "campo": nome,
                "apolice_a": self._formatar(valor_a),
                "apolice_b": self._formatar(valor_b),
                "diferente": valor_a != valor_b,
            })

        return resultado

    def _formatar(self, valor):
        if valor is None:
            return "Não identificado"

        if isinstance(valor, (dict, list)):
            if isinstance(valor, dict):
                return "; ".join(
                    f"{chave}: {item}"
                    for chave, item in valor.items()
                )

            return "; ".join(str(item) for item in valor)

        return str(valor)