package com.nicolasviruel.pedidos.dto.pedido;
import com.nicolasviruel.pedidos.dto.detallePedido.DetallePedidoDto;
import com.nicolasviruel.pedidos.enums.Estado;
import com.nicolasviruel.pedidos.enums.FormaPago;
import java.time.LocalDate;
import java.util.List;
public record PedidoDto(Long id, LocalDate fecha, Estado estado, Double total, FormaPago formaPago, Long usuarioId, List<DetallePedidoDto> detalles) {}
