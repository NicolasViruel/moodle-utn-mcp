package com.nicolasviruel.pedidos.controller;

import com.nicolasviruel.pedidos.dto.usuario.UsuarioCreate;
import com.nicolasviruel.pedidos.dto.usuario.UsuarioDto;
import com.nicolasviruel.pedidos.service.UsuarioService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/usuarios")
@Tag(name = "Usuarios", description = "API REST para gestión de usuarios")
public class UsuarioController {

    private final UsuarioService usuarioService;

    public UsuarioController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @GetMapping
    @Operation(summary = "Listar todos los usuarios")
    public List<UsuarioDto> listar() {
        return usuarioService.listar();
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obtener un usuario por ID e imprimir por consola")
    public UsuarioDto obtenerPorId(@PathVariable Long id) {
        return usuarioService.obtenerPorId(id);
    }

    @GetMapping("/mail/{mail}")
    @Operation(summary = "Obtener un usuario por mail e imprimir por consola")
    public UsuarioDto obtenerPorMail(@PathVariable String mail) {
        return usuarioService.obtenerPorMail(mail);
    }

    @PostMapping
    @Operation(summary = "Crear un usuario")
    public ResponseEntity<UsuarioDto> crear(@RequestBody UsuarioCreate dto) {
        UsuarioDto creado = usuarioService.crear(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(creado);
    }
}
