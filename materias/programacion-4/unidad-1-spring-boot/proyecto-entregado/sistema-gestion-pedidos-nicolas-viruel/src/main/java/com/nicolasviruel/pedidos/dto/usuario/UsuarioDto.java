package com.nicolasviruel.pedidos.dto.usuario;
import com.nicolasviruel.pedidos.enums.Rol;
public record UsuarioDto(Long id, String nombre, String apellido, String mail, String celular, Rol rol) {}
