package com.nicolasviruel.pedidos.service;

import com.nicolasviruel.pedidos.dto.producto.*;
import com.nicolasviruel.pedidos.entity.Categoria;
import com.nicolasviruel.pedidos.entity.Producto;
import com.nicolasviruel.pedidos.exception.ResourceNotFoundException;
import com.nicolasviruel.pedidos.mapper.DtoMapper;
import com.nicolasviruel.pedidos.repository.CategoriaRepository;
import com.nicolasviruel.pedidos.repository.ProductoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class ProductoService {
    private final ProductoRepository repository;
    private final CategoriaRepository categoriaRepository;
    private final DtoMapper mapper;

    public ProductoService(ProductoRepository repository, CategoriaRepository categoriaRepository, DtoMapper mapper) {
        this.repository = repository;
        this.categoriaRepository = categoriaRepository;
        this.mapper = mapper;
    }

    @Transactional
    public ProductoDto crear(ProductoCreate dto) {
        Categoria categoria = obtenerCategoria(dto.categoriaId());
        Producto entity = Producto.builder()
                .nombre(dto.nombre())
                .precio(dto.precio())
                .descripcion(dto.descripcion())
                .stock(dto.stock())
                .imagen(dto.imagen())
                .disponible(dto.disponible())
                .categoria(categoria)
                .build();
        return mapper.toDto(repository.save(entity));
    }

    @Transactional(readOnly = true)
    public List<ProductoDto> listar() {
        return repository.findAll().stream().map(mapper::toDto).toList();
    }

    @Transactional(readOnly = true)
    public List<ProductoDto> listarDisponibles() {
        return repository.findByDisponibleTrue().stream().map(mapper::toDto).toList();
    }

    @Transactional(readOnly = true)
    public ProductoDto obtenerPorId(Long id) {
        return mapper.toDto(obtenerEntidad(id));
    }

    @Transactional
    public ProductoDto actualizar(Long id, ProductoEdit dto) {
        Producto producto = obtenerEntidad(id);
        Categoria categoria = obtenerCategoria(dto.categoriaId());
        producto.setNombre(dto.nombre());
        producto.setPrecio(dto.precio());
        producto.setDescripcion(dto.descripcion());
        producto.setStock(dto.stock());
        producto.setImagen(dto.imagen());
        producto.setDisponible(dto.disponible());
        producto.setCategoria(categoria);
        return mapper.toDto(repository.save(producto));
    }

    @Transactional
    public ProductoDto actualizarParcial(Long id, ProductoPatch dto) {
        Producto producto = obtenerEntidad(id);
        if (dto.nombre() != null) {
            producto.setNombre(dto.nombre());
        }
        if (dto.precio() != null) {
            producto.setPrecio(dto.precio());
        }
        if (dto.descripcion() != null) {
            producto.setDescripcion(dto.descripcion());
        }
        if (dto.stock() != null) {
            producto.setStock(dto.stock());
        }
        if (dto.imagen() != null) {
            producto.setImagen(dto.imagen());
        }
        if (dto.disponible() != null) {
            producto.setDisponible(dto.disponible());
        }
        if (dto.categoriaId() != null) {
            producto.setCategoria(obtenerCategoria(dto.categoriaId()));
        }
        return mapper.toDto(repository.save(producto));
    }

    @Transactional
    public void eliminar(Long id) {
        Producto producto = obtenerEntidad(id);
        repository.delete(producto);
    }

    private Producto obtenerEntidad(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Producto no encontrado con id: " + id));
    }

    private Categoria obtenerCategoria(Long id) {
        return categoriaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con id: " + id));
    }
}
