package com.nicolasviruel.pedidos.repository;
import com.nicolasviruel.pedidos.entity.DetallePedido;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
@Repository
public interface DetallePedidoRepository extends JpaRepository<DetallePedido, Long> {}
