package com.nicolasviruel.pedidos.dto.detallePedido;
public record DetallePedidoDto(Long id, Integer cantidad, Double subtotal, Long productoId, String productoNombre) {}
