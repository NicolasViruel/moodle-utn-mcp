package com.nicolasviruel.pedidos.controller;

import com.nicolasviruel.pedidos.dto.pedido.PedidoCreate;
import com.nicolasviruel.pedidos.dto.pedido.PedidoDto;
import com.nicolasviruel.pedidos.service.PedidoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/pedidos")
@Tag(name = "Pedidos", description = "API REST para gestión de pedidos")
public class PedidoController {

    private final PedidoService pedidoService;

    public PedidoController(PedidoService pedidoService) {
        this.pedidoService = pedidoService;
    }

    @GetMapping
    @Operation(summary = "Listar todos los pedidos")
    public List<PedidoDto> listar() {
        return pedidoService.listar();
    }

    @PostMapping
    @Operation(summary = "Crear un pedido")
    public ResponseEntity<PedidoDto> crear(@RequestBody PedidoCreate dto) {
        PedidoDto creado = pedidoService.crear(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(creado);
    }
}
