package com.nicolasviruel.pedidos.controller;

import com.nicolasviruel.pedidos.dto.categoria.CategoriaCreate;
import com.nicolasviruel.pedidos.dto.categoria.CategoriaDto;
import com.nicolasviruel.pedidos.dto.categoria.CategoriaEdit;
import com.nicolasviruel.pedidos.service.CategoriaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/categorias")
@Tag(name = "Categorías", description = "API REST para gestión de categorías")
public class CategoriaController {

    private final CategoriaService categoriaService;

    public CategoriaController(CategoriaService categoriaService) {
        this.categoriaService = categoriaService;
    }

    @GetMapping
    @Operation(summary = "Listar todas las categorías")
    public List<CategoriaDto> listar() {
        return categoriaService.listar();
    }

    @PostMapping
    @Operation(summary = "Crear una categoría")
    public ResponseEntity<CategoriaDto> crear(@RequestBody CategoriaCreate dto) {
        CategoriaDto creada = categoriaService.crear(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(creada);
    }

    @PutMapping("/{id}")
    @Operation(summary = "Actualizar una categoría")
    public CategoriaDto actualizar(@PathVariable Long id, @RequestBody CategoriaEdit dto) {
        return categoriaService.actualizar(id, dto);
    }
}
