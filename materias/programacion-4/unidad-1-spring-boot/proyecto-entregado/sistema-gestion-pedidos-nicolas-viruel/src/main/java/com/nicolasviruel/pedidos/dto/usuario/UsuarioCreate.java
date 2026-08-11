package com.nicolasviruel.pedidos.dto.usuario;
import com.nicolasviruel.pedidos.enums.Rol;
public record UsuarioCreate(String nombre, String apellido, String mail, String celular, String contrasena, Rol rol) {}
