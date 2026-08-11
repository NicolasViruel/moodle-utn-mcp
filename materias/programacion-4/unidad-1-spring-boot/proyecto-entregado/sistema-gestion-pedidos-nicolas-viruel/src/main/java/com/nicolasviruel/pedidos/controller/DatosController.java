package com.nicolasviruel.pedidos.controller;

import com.nicolasviruel.pedidos.dto.categoria.CategoriaDto;
import com.nicolasviruel.pedidos.dto.pedido.PedidoDto;
import com.nicolasviruel.pedidos.dto.usuario.UsuarioDto;
import com.nicolasviruel.pedidos.service.CategoriaService;
import com.nicolasviruel.pedidos.service.PedidoService;
import com.nicolasviruel.pedidos.service.UsuarioService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api")
public class DatosController {
    private final CategoriaService categoriaService;
    private final UsuarioService usuarioService;
    private final PedidoService pedidoService;

    public DatosController(CategoriaService categoriaService, UsuarioService usuarioService,
                           PedidoService pedidoService) {
        this.categoriaService = categoriaService;
        this.usuarioService = usuarioService;
        this.pedidoService = pedidoService;
    }

    @GetMapping("/categorias")
    public List<CategoriaDto> categorias() {
        return categoriaService.listar();
    }

    @GetMapping("/usuarios")
    public List<UsuarioDto> usuarios() {
        return usuarioService.listar();
    }

    @GetMapping("/pedidos")
    public List<PedidoDto> pedidos() {
        return pedidoService.listar();
    }
}
