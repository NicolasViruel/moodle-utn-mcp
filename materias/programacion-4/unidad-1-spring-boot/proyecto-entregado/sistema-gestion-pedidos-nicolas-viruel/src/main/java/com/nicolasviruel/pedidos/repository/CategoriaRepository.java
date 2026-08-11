package com.nicolasviruel.pedidos.repository;
import com.nicolasviruel.pedidos.entity.Categoria;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
@Repository
public interface CategoriaRepository extends JpaRepository<Categoria, Long> {}
