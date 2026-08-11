package com.nicolasviruel.pedidos.service;
import com.nicolasviruel.pedidos.dto.usuario.*;
import com.nicolasviruel.pedidos.entity.Usuario;
import com.nicolasviruel.pedidos.mapper.DtoMapper;
import com.nicolasviruel.pedidos.repository.UsuarioRepository;
import org.springframework.stereotype.Service;
import java.util.List;
@Service
public class UsuarioService {
    private final UsuarioRepository repository;
    private final DtoMapper mapper;
    public UsuarioService(UsuarioRepository repository, DtoMapper mapper) { this.repository = repository; this.mapper = mapper; }
    public UsuarioDto crear(UsuarioCreate dto) {
        Usuario entity = Usuario.builder().nombre(dto.nombre()).apellido(dto.apellido()).mail(dto.mail())
                .celular(dto.celular()).contrasena(dto.contrasena()).rol(dto.rol()).build();
        return mapper.toDto(repository.save(entity));
    }
    public List<UsuarioDto> listar() { return repository.findAll().stream().map(mapper::toDto).toList(); }
}
