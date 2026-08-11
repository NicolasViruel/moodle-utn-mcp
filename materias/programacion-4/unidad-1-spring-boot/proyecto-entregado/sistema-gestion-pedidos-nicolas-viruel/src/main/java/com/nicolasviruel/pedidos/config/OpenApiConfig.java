package com.nicolasviruel.pedidos.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI productosOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("API REST - Gestión de Productos")
                        .description("Sistema de e-commerce básico - Programación IV UTN TUP")
                        .version("2.0"));
    }
}
