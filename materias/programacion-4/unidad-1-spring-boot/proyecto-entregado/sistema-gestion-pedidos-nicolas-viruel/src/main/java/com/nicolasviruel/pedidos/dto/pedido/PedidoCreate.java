package com.nicolasviruel.pedidos.dto.pedido;

import com.nicolasviruel.pedidos.dto.detallePedido.DetallePedidoCreate;
import com.nicolasviruel.pedidos.enums.FormaPago;

import java.util.List;

public record PedidoCreate(Long usuarioId, FormaPago formaPago, List<DetallePedidoCreate> detalles) {}
