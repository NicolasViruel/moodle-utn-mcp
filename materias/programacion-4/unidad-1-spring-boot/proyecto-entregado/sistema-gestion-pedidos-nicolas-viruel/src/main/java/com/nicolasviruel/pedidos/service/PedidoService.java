package com.nicolasviruel.pedidos.service;
import com.nicolasviruel.pedidos.dto.pedido.PedidoCreate;
import com.nicolasviruel.pedidos.dto.pedido.PedidoDto;
import com.nicolasviruel.pedidos.entity.*;
import com.nicolasviruel.pedidos.enums.Estado;
import com.nicolasviruel.pedidos.exception.ResourceNotFoundException;
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
        this.pedidoRepository = pedidoRepository;
        this.usuarioRepository = usuarioRepository;
        this.productoRepository = productoRepository;
        this.mapper = mapper;
    }

    @Transactional
    public PedidoDto crear(PedidoCreate dto) {
        Usuario usuario = usuarioRepository.findById(dto.usuarioId())
                .orElseThrow(() -> new ResourceNotFoundException("Usuario no encontrado con id: " + dto.usuarioId()));
        Pedido pedido = Pedido.builder()
                .fecha(LocalDate.now())
                .estado(Estado.PENDIENTE)
                .total(0.0)
                .formaPago(dto.formaPago())
                .usuario(usuario)
                .build();
        for (var detalleDto : dto.detalles()) {
            Producto producto = productoRepository.findById(detalleDto.productoId())
                    .orElseThrow(() -> new ResourceNotFoundException("Producto no encontrado con id: " + detalleDto.productoId()));
            pedido.addDetallePedido(detalleDto.cantidad(), producto);
        }
        return mapper.toDto(pedidoRepository.save(pedido));
    }

    @Transactional(readOnly = true)
    public List<PedidoDto> listar() {
        return pedidoRepository.findAll().stream().map(mapper::toDto).toList();
    }
}
