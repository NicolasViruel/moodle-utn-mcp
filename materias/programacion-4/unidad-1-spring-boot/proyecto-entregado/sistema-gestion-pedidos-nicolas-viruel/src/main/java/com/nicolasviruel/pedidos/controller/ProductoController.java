package com.nicolasviruel.pedidos.controller;

import com.nicolasviruel.pedidos.dto.producto.ProductoCreate;
import com.nicolasviruel.pedidos.dto.producto.ProductoDto;
import com.nicolasviruel.pedidos.dto.producto.ProductoEdit;
import com.nicolasviruel.pedidos.dto.producto.ProductoPatch;
import com.nicolasviruel.pedidos.service.ProductoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/productos")
@Tag(name = "Productos", description = "API REST para gestión de productos")
public class ProductoController {

    private final ProductoService productoService;

    public ProductoController(ProductoService productoService) {
        this.productoService = productoService;
    }

    @GetMapping
    @Operation(summary = "Listar todos los productos")
    public List<ProductoDto> listar() {
        return productoService.listar();
    }

    @GetMapping("/disponibles")
    @Operation(summary = "Listar productos disponibles")
    public List<ProductoDto> listarDisponibles() {
        return productoService.listarDisponibles();
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obtener un producto por ID")
    public ProductoDto obtenerPorId(@PathVariable Long id) {
        return productoService.obtenerPorId(id);
    }

    @PostMapping
    @Operation(summary = "Crear un producto")
    public ResponseEntity<ProductoDto> crear(@Valid @RequestBody ProductoCreate dto) {
        ProductoDto creado = productoService.crear(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(creado);
    }

    @PutMapping("/{id}")
    @Operation(summary = "Actualizar un producto completo")
    public ProductoDto actualizar(@PathVariable Long id, @Valid @RequestBody ProductoEdit dto) {
        return productoService.actualizar(id, dto);
    }

    @PatchMapping("/{id}")
    @Operation(summary = "Actualizar parcialmente un producto")
    public ProductoDto actualizarParcial(@PathVariable Long id, @Valid @RequestBody ProductoPatch dto) {
        return productoService.actualizarParcial(id, dto);
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Eliminar un producto")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        productoService.eliminar(id);
        return ResponseEntity.noContent().build();
    }
}
