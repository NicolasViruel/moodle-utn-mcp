package com.nicolasviruel.pedidos.service;
import com.nicolasviruel.pedidos.dto.categoria.*;
import com.nicolasviruel.pedidos.entity.Categoria;
import com.nicolasviruel.pedidos.mapper.DtoMapper;
import com.nicolasviruel.pedidos.repository.CategoriaRepository;
import org.springframework.stereotype.Service;
import java.util.List;
@Service
public class CategoriaService {
    private final CategoriaRepository repository;
    private final DtoMapper mapper;
    public CategoriaService(CategoriaRepository repository, DtoMapper mapper) { this.repository = repository; this.mapper = mapper; }
    public CategoriaDto crear(CategoriaCreate dto) { return mapper.toDto(repository.save(Categoria.builder().nombre(dto.nombre()).descripcion(dto.descripcion()).build())); }
    public List<CategoriaDto> listar() { return repository.findAll().stream().map(mapper::toDto).toList(); }
}
