"""Le funzioni che servono per fare i conti della spesa."""


def totale(prezzi):
    """La somma dei prezzi."""
    return sum(prezzi)


def prezzo_medio(prezzi):
    """Il prezzo medio, cioè il totale diviso per il numero dei prodotti."""
    return sum(prezzi) / len(prezzi)
