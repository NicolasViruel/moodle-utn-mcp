package com.nicolasviruel.pedidos.service;
import com.nicolasviruel.pedidos.dto.usuario.*;
import com.nicolasviruel.pedidos.entity.Usuario;
import com.nicolasviruel.pedidos.exception.ResourceNotFoundException;
import com.nicolasviruel.pedidos.mapper.DtoMapper;
import com.nicolasviruel.pedidos.repository.UsuarioRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class UsuarioService {
    private final UsuarioRepository repository;
    private final DtoMapper mapper;

    public UsuarioService(UsuarioRepository repository, DtoMapper mapper) {
        this.repository = repository;
        this.mapper = mapper;
    }

    @Transactional
    public UsuarioDto crear(UsuarioCreate dto) {
        Usuario entity = Usuario.builder()
                .nombre(dto.nombre())
                .apellido(dto.apellido())
                .mail(dto.mail())
                .celular(dto.celular())
                .contrasena(dto.contrasena())
                .rol(dto.rol())
                .build();
        return mapper.toDto(repository.save(entity));
    }

    @Transactional(readOnly = true)
    public List<UsuarioDto> listar() {
        return repository.findAll().stream().map(mapper::toDto).toList();
    }

    @Transactional(readOnly = true)
    public UsuarioDto obtenerPorId(Long id) {
        Usuario usuario = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Usuario no encontrado con id: " + id));
        imprimirPorConsola(usuario);
        return mapper.toDto(usuario);
    }

    @Transactional(readOnly = true)
    public UsuarioDto obtenerPorMail(String mail) {
        Usuario usuario = repository.findByMail(mail)
                .orElseThrow(() -> new ResourceNotFoundException("Usuario no encontrado con mail: " + mail));
        imprimirPorConsola(usuario);
        return mapper.toDto(usuario);
    }

    private void imprimirPorConsola(Usuario usuario) {
        System.out.println("=== Usuario encontrado ===");
        System.out.println("ID: " + usuario.getId());
        System.out.println("Nombre: " + usuario.getNombre() + " " + usuario.getApellido());
        System.out.println("Mail: " + usuario.getMail());
        System.out.println("Celular: " + usuario.getCelular());
        System.out.println("Rol: " + usuario.getRol());
        System.out.println("==========================");
    }
}
