package com.nicolasviruel.pedidos;
import com.nicolasviruel.pedidos.repository.*;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import static org.assertj.core.api.Assertions.assertThat;
@SpringBootTest
@ActiveProfiles("dev")
class SistemaGestionPedidosApplicationTests {
    @Autowired UsuarioRepository usuarioRepository;
    @Autowired PedidoRepository pedidoRepository;
    @Autowired CategoriaRepository categoriaRepository;
    @Autowired ProductoRepository productoRepository;

    @Test
    void debeCargarLasCantidadesSolicitadas() {
        assertThat(usuarioRepository.count()).isEqualTo(2);
        assertThat(pedidoRepository.count()).isEqualTo(3);
        assertThat(categoriaRepository.count()).isEqualTo(3);
        assertThat(productoRepository.count()).isEqualTo(10);
        assertThat(pedidoRepository.findAll()).allSatisfy(pedido -> assertThat(pedido.getDetalles()).hasSizeGreaterThanOrEqualTo(2));
    }
}
