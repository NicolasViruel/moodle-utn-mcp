package com.nicolasviruel.pedidos.dto.producto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;

public record ProductoEdit(
        @NotBlank(message = "El nombre es obligatorio")
        String nombre,
        @NotNull(message = "El precio es obligatorio")
        @Positive(message = "El precio debe ser mayor a cero")
        Double precio,
        String descripcion,
        @PositiveOrZero(message = "El stock no puede ser negativo")
        Integer stock,
        String imagen,
        @NotNull(message = "Debe indicar si el producto está disponible")
        Boolean disponible,
        @NotNull(message = "La categoría es obligatoria")
        Long categoriaId
) {}
