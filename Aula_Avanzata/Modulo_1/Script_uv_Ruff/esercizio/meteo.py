"""Le funzioni che servono per il riepilogo delle temperature della settimana."""
import math


def massima(temperature):
    """La temperatura più alta della lista."""
    return max(temperature)
def minima(temperature):
    """La temperatura più bassa della lista."""
    giorni=len(temperature)
    return min(temperature)
def media(temperature):
    """La media delle temperature, cioè la loro somma divisa per il numero dei valori."""
    return sum( temperature )/len(temperature)
