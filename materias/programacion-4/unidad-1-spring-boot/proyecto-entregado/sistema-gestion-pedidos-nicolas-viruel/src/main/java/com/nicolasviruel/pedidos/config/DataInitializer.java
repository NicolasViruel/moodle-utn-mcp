package com.nicolasviruel.pedidos.config;

import com.nicolasviruel.pedidos.dto.categoria.CategoriaCreate;
import com.nicolasviruel.pedidos.dto.detallePedido.DetallePedidoCreate;
import com.nicolasviruel.pedidos.dto.pedido.PedidoCreate;
import com.nicolasviruel.pedidos.dto.producto.ProductoCreate;
import com.nicolasviruel.pedidos.dto.usuario.UsuarioCreate;
import com.nicolasviruel.pedidos.enums.FormaPago;
import com.nicolasviruel.pedidos.enums.Rol;
import com.nicolasviruel.pedidos.service.*;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import java.util.List;

@Configuration
public class DataInitializer {
    @Bean
    @Profile("dev")
    CommandLineRunner cargarDatos(CategoriaService categoriaService, ProductoService productoService,
                                   UsuarioService usuarioService, PedidoService pedidoService) {
        return args -> {
            var tecnologia = categoriaService.crear(new CategoriaCreate("Tecnología", "Productos tecnológicos"));
            var hogar = categoriaService.crear(new CategoriaCreate("Hogar", "Artículos para el hogar"));
            var libreria = categoriaService.crear(new CategoriaCreate("Librería", "Artículos de estudio y oficina"));

            var p1 = productoService.crear(new ProductoCreate("Teclado", 25000.0, "Teclado mecánico", 20, "teclado.jpg", true, tecnologia.id()));
            var p2 = productoService.crear(new ProductoCreate("Mouse", 15000.0, "Mouse óptico", 30, "mouse.jpg", true, tecnologia.id()));
            var p3 = productoService.crear(new ProductoCreate("Monitor", 180000.0, "Monitor 24 pulgadas", 10, "monitor.jpg", true, tecnologia.id()));
            var p4 = productoService.crear(new ProductoCreate("Auriculares", 45000.0, "Auriculares con micrófono", 15, "auriculares.jpg", true, tecnologia.id()));
            var p5 = productoService.crear(new ProductoCreate("Lámpara", 22000.0, "Lámpara de escritorio", 25, "lampara.jpg", true, hogar.id()));
            var p6 = productoService.crear(new ProductoCreate("Taza", 7000.0, "Taza de cerámica", 40, "taza.jpg", true, hogar.id()));
            var p7 = productoService.crear(new ProductoCreate("Organizador", 12000.0, "Organizador de escritorio", 18, "organizador.jpg", true, hogar.id()));
            var p8 = productoService.crear(new ProductoCreate("Cuaderno", 5500.0, "Cuaderno universitario", 50, "cuaderno.jpg", true, libreria.id()));
            var p9 = productoService.crear(new ProductoCreate("Lapicera", 1800.0, "Lapicera tinta azul", 100, "lapicera.jpg", true, libreria.id()));
            var p10 = productoService.crear(new ProductoCreate("Resaltador", 2500.0, "Resaltador fluorescente", 70, "resaltador.jpg", true, libreria.id()));

            var u1 = usuarioService.crear(new UsuarioCreate("Nicolas", "Viruel", "nicolas.viruel@correo.com", "1111111111", "clave123", Rol.ADMIN));
            var u2 = usuarioService.crear(new UsuarioCreate("Ana", "Pérez", "ana.perez@correo.com", "2222222222", "clave456", Rol.USUARIO));

            pedidoService.crear(new PedidoCreate(u1.id(), FormaPago.TARJETA, List.of(new DetallePedidoCreate(1, p1.id()), new DetallePedidoCreate(2, p2.id()))));
            pedidoService.crear(new PedidoCreate(u1.id(), FormaPago.TRANSFERENCIA, List.of(new DetallePedidoCreate(1, p3.id()), new DetallePedidoCreate(1, p4.id()))));
            pedidoService.crear(new PedidoCreate(u2.id(), FormaPago.EFECTIVO, List.of(new DetallePedidoCreate(2, p8.id()), new DetallePedidoCreate(3, p9.id()), new DetallePedidoCreate(1, p10.id()))));
        };
    }
}
