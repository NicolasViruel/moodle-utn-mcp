package com.nicolasviruel.pedidos.entity;

import jakarta.persistence.*;
import lombok.*;
import java.util.HashSet;
import java.util.Set;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "categorias")
public class Categoria extends Base {
    @Column(nullable = false, unique = true)
    private String nombre;
    private String descripcion;

    @OneToMany(mappedBy = "categoria")
    @Builder.Default
    private Set<Producto> productos = new HashSet<>();
}
