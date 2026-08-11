package com.nicolasviruel.pedidos.entity;

import com.nicolasviruel.pedidos.enums.Estado;
import com.nicolasviruel.pedidos.enums.FormaPago;
import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDate;
import java.util.HashSet;
import java.util.Set;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "pedidos")
public class Pedido extends Base implements Calculable {
    @Column(nullable = false)
    private LocalDate fecha;
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Estado estado;
    @Column(nullable = false)
    private Double total;
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private FormaPago formaPago;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "usuario_id", nullable = false)
    private Usuario usuario;

    @OneToMany(mappedBy = "pedido", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<DetallePedido> detalles = new HashSet<>();

    public void addDetallePedido(int cantidad, Producto producto) {
        DetallePedido detalle = DetallePedido.builder()
                .cantidad(cantidad)
                .subtotal(producto.getPrecio() * cantidad)
                .producto(producto)
                .build();
        detalles.add(detalle);
        detalle.setPedido(this);
        calcularTotal();
    }

    public void deleteDetallePedidoByProducto(Producto producto) {
        detalles.removeIf(detalle -> detalle.getProducto().getId().equals(producto.getId()));
        calcularTotal();
    }

    public DetallePedido findDetallePedidoByProducto(Producto producto) {
        return detalles.stream()
                .filter(detalle -> detalle.getProducto().getId().equals(producto.getId()))
                .findFirst()
                .orElse(null);
    }

    @Override
    public void calcularTotal() {
        this.total = detalles.stream().mapToDouble(DetallePedido::getSubtotal).sum();
    }
}
