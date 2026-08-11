package com.nicolasviruel.pedidos.dto.pedido;
import com.nicolasviruel.pedidos.enums.Estado;
import com.nicolasviruel.pedidos.enums.FormaPago;
public record PedidoEdit(Estado estado, FormaPago formaPago) {}
