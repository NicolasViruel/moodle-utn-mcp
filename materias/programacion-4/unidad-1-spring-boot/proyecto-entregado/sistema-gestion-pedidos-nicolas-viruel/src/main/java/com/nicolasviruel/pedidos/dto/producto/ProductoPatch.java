package com.nicolasviruel.pedidos.dto.producto;

import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;

public record ProductoPatch(
        String nombre,
        @Positive(message = "El precio debe ser mayor a cero")
        Double precio,
        String descripcion,
        @PositiveOrZero(message = "El stock no puede ser negativo")
        Integer stock,
        String imagen,
        Boolean disponible,
        Long categoriaId
) {}
