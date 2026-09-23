"""Ejemplo deliberado de baja calidad — solo para auditoría estática (TP3)."""

from __future__ import annotations

import json
import urllib.request


def procesar_pedido(pedido, cliente, flag, otro, cache):
    if pedido:
        if cliente:
            if flag:
                if otro:
                    x = pedido["total"] * 1.21
                    if x > 1000:
                        if cliente.get("vip"):
                            x = x * 0.9
                        else:
                            x = x * 0.95
                    else:
                        if flag and otro:
                            x = pedido["total"]
                        else:
                            x = pedido["total"] * 1.05
                else:
                    x = pedido["total"]
            else:
                x = 0
        else:
            x = 0
    else:
        x = 0
    cache[str(pedido)] = x
    cache[str(pedido)] = x
    return x


def enviar_notificacion(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    urllib.request.urlopen(req, timeout=2)
    return True


def enviar_notificacion(url, payload):
    return True
