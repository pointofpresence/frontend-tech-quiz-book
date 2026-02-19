# Может ли @RestController возвращать XML, а не JSON?

**Может ли @RestController возвращать XML, а не JSON?**

- @RestController — Spring MVC контроллер для REST API  
- По умолчанию возвращает JSON через MessageConverter (MappingJackson2HttpMessageConverter)  
- Для XML нужна поддержка Jackson XML или JAXB через другой HttpMessageConverter  
- Контент-тип меняется на "application/xml" (через headers или @Produces)  
- Конфигурируется через зависимости и настройку конвертеров в Spring  
- Можно вернуть XML, если настройка и модели поддерживают сериализацию XML  
- Практический кейс: интеграция с системами, требующими XML (SOAP, legacy сервисы)

# Подробный ответ
## Основной ответ
Да, аннотация **@RestController** в Spring Boot может возвращать ответ в формате **XML** вместо JSON. По умолчанию Spring Boot использует Jackson для сериализации объектов в JSON, но если в проект добавить соответствующий **message converter** для XML, например Jackson XML или JAXB, и правильно настроить content negotiation, контроллер без проблем сможет выдавать данные в формате XML.

## Ключевые моменты
- **Content negotiation (согласование формата)** — Spring определяет формат ответа по заголовку `Accept` HTTP-запроса или через URL-параметры. Если клиент отправляет `Accept: application/xml`, а в приложении присутствует XML-конвертер, то ответ будет в XML.
- Для поддержки XML нужно добавить зависимость, например `com.fasterxml.jackson.dataformat:jackson-dataformat-xml` или включить JAXB, и зарегистрировать соответствующий HttpMessageConverter.
- В `@RestController` возвращаемый объект сериализуется автоматически, формат зависит от настроек и доступных конвертеров. JSON и XML — просто разные представления одного и того же объекта.

## Практический контекст
В приложениях на Spring Boot 2.5+ обычно JSON — стандарт, но при взаимодействии с внешними системами, которые требуют XML (например SOAP-подобные сервисы или старые API), добавляют Jackson XML. Для этого достаточно добавить зависимость и, при необходимости, переопределить `WebMvcConfigurer` для регистрации `MappingJackson2XmlHttpMessageConverter`. Затем клиенты могут запрашивать XML, и контроллеры с `@RestController` автоматически его возвращают, что обеспечивает гибкость API.
