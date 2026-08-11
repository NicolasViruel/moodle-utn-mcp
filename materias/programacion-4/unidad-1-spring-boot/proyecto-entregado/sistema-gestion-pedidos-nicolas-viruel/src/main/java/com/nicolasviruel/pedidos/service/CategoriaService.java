package com.nicolasviruel.pedidos.service;
import com.nicolasviruel.pedidos.dto.categoria.*;
import com.nicolasviruel.pedidos.entity.Categoria;
import com.nicolasviruel.pedidos.exception.ResourceNotFoundException;
import com.nicolasviruel.pedidos.mapper.DtoMapper;
import com.nicolasviruel.pedidos.repository.CategoriaRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class CategoriaService {
    private final CategoriaRepository repository;
    private final DtoMapper mapper;

    public CategoriaService(CategoriaRepository repository, DtoMapper mapper) {
        this.repository = repository;
        this.mapper = mapper;
    }

    @Transactional
    public CategoriaDto crear(CategoriaCreate dto) {
        return mapper.toDto(repository.save(Categoria.builder()
                .nombre(dto.nombre())
                .descripcion(dto.descripcion())
                .build()));
    }

    @Transactional
    public CategoriaDto actualizar(Long id, CategoriaEdit dto) {
        Categoria categoria = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con id: " + id));
        categoria.setNombre(dto.nombre());
        categoria.setDescripcion(dto.descripcion());
        return mapper.toDto(repository.save(categoria));
    }

    @Transactional(readOnly = true)
    public List<CategoriaDto> listar() {
        return repository.findAll().stream().map(mapper::toDto).toList();
    }
}
