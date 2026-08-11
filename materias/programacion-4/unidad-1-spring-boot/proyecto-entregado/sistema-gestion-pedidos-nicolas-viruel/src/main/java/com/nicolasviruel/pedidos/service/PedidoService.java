package com.nicolasviruel.pedidos.service;
import com.nicolasviruel.pedidos.dto.detallePedido.DetallePedidoCreate;
import com.nicolasviruel.pedidos.dto.pedido.PedidoDto;
import com.nicolasviruel.pedidos.entity.*;
import com.nicolasviruel.pedidos.enums.Estado;
import com.nicolasviruel.pedidos.enums.FormaPago;
import com.nicolasviruel.pedidos.mapper.DtoMapper;
import com.nicolasviruel.pedidos.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDate;
import java.util.List;
@Service
public class PedidoService {
    private final PedidoRepository pedidoRepository;
    private final UsuarioRepository usuarioRepository;
    private final ProductoRepository productoRepository;
    private final DtoMapper mapper;
    public PedidoService(PedidoRepository pedidoRepository, UsuarioRepository usuarioRepository,
                         ProductoRepository productoRepository, DtoMapper mapper) {
        this.pedidoRepository = pedidoRepository; this.usuarioRepository = usuarioRepository;
        this.productoRepository = productoRepository; this.mapper = mapper;
    }
    @Transactional
    public PedidoDto crear(Long usuarioId, FormaPago formaPago, List<DetallePedidoCreate> detallesDto) {
        Usuario usuario = usuarioRepository.findById(usuarioId).orElseThrow(() -> new IllegalArgumentException("Usuario inexistente"));
        Pedido pedido = Pedido.builder().fecha(LocalDate.now()).estado(Estado.PENDIENTE).total(0.0).formaPago(formaPago).usuario(usuario).build();
        for (DetallePedidoCreate dto : detallesDto) {
            Producto producto = productoRepository.findById(dto.productoId()).orElseThrow(() -> new IllegalArgumentException("Producto inexistente"));
            DetallePedido detalle = DetallePedido.builder().cantidad(dto.cantidad()).subtotal(producto.getPrecio() * dto.cantidad()).producto(producto).build();
            pedido.addDetallePedido(detalle);
        }
        return mapper.toDto(pedidoRepository.save(pedido));
    }
    @Transactional(readOnly = true)
    public List<PedidoDto> listar() { return pedidoRepository.findAll().stream().map(mapper::toDto).toList(); }
}
