package com.nicolasviruel.pedidos.mapper;

import com.nicolasviruel.pedidos.dto.categoria.*;
import com.nicolasviruel.pedidos.dto.detallePedido.DetallePedidoDto;
import com.nicolasviruel.pedidos.dto.pedido.PedidoDto;
import com.nicolasviruel.pedidos.dto.producto.ProductoDto;
import com.nicolasviruel.pedidos.dto.usuario.UsuarioDto;
import com.nicolasviruel.pedidos.entity.*;
import org.springframework.stereotype.Component;

@Component
public class DtoMapper {
    public CategoriaDto toDto(Categoria entity) {
        return new CategoriaDto(entity.getId(), entity.getNombre(), entity.getDescripcion());
    }
    public ProductoDto toDto(Producto entity) {
        return new ProductoDto(entity.getId(), entity.getNombre(), entity.getPrecio(), entity.getDescripcion(),
                entity.getStock(), entity.getImagen(), entity.getDisponible(), entity.getCategoria().getId(),
                entity.getCategoria().getNombre());
    }
    public UsuarioDto toDto(Usuario entity) {
        return new UsuarioDto(entity.getId(), entity.getNombre(), entity.getApellido(), entity.getMail(), entity.getCelular(), entity.getRol());
    }
    public DetallePedidoDto toDto(DetallePedido entity) {
        return new DetallePedidoDto(entity.getId(), entity.getCantidad(), entity.getSubtotal(),
                entity.getProducto().getId(), entity.getProducto().getNombre());
    }
    public PedidoDto toDto(Pedido entity) {
        return new PedidoDto(entity.getId(), entity.getFecha(), entity.getEstado(), entity.getTotal(),
                entity.getFormaPago(), entity.getUsuario().getId(), entity.getDetalles().stream().map(this::toDto).toList());
    }
}
