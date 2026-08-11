package com.nicolasviruel.pedidos.dto.producto;
public record ProductoDto(Long id, String nombre, Double precio, String descripcion, Integer stock, String imagen, Boolean disponible, Long categoriaId, String categoriaNombre) {}
