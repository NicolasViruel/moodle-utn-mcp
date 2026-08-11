package com.nicolasviruel.pedidos.entity;

import jakarta.persistence.*;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "productos")
public class Producto extends Base {
    @Column(nullable = false)
    private String nombre;
    @Column(nullable = false)
    private Double precio;
    private String descripcion;
    private Integer stock;
    private String imagen;
    @Column(nullable = false)
    private Boolean disponible;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "categoria_id", nullable = false)
    private Categoria categoria;
}
