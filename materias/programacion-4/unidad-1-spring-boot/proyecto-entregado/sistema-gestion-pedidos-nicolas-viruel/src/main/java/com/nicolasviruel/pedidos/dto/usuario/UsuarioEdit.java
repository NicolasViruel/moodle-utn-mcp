package com.nicolasviruel.pedidos.dto.usuario;
import com.nicolasviruel.pedidos.enums.Rol;
public record UsuarioEdit(String nombre, String apellido, String celular, Rol rol) {}
