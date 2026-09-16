<div align="center">

<h1 style="border-bottom: none">
  <b><a href="https://tourmind.com/skills">TourMind Booking Skills</a></b><br />
  <strong>Haz que tu agente busque y reserve hoteles y vuelos en todo el mundo</strong>
</h1>

<a href="https://tourmind.com/skills">
  <img alt="TourMind Booking Skills" src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/hero/tourmind-booking-skills.png" style="width: 100%" />
</a>

<br />

<p align="center">
  Lleva a tus clientes a una nueva forma de viajar
</p>

<br />

<div align="center">
  <a href="https://tourmind.com/skills">Página del producto</a> |
  <a href="https://auth.journione.ai">Obtener un Token</a> |
  <a href="https://tourmind.com">Empresa</a>
</div>

<br />

[![ClawHub installs](https://img.shields.io/badge/ClawHub_installs-2.1k-F97316)](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
[![Release](https://img.shields.io/github/v/release/tourmind-com/Tourmind-Booking-Skills?label=release)](https://github.com/tourmind-com/Tourmind-Booking-Skills/releases/latest)
[![License](https://img.shields.io/github/license/tourmind-com/Tourmind-Booking-Skills)](LICENSE)

</div>

<br />

<div align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.es.md">Español</a>
</div>

<br />

Convierte tu agente de IA en una solución integral para reservar hoteles y buscar y reservar vuelos en todo el mundo. Sin salir de tu cliente de IA habitual, puedes buscar hoteles y vuelos globales, comparar precios en tiempo real de las principales OTA y proveedores, verificar la disponibilidad y los precios finales, y utilizar TourMind Booking Skills para completar reservas y pagos y consultar su estado.

## Demostración del Skill de hoteles

Los siguientes GIF muestran la experiencia del Skill de hoteles.

### 1. Buscar hoteles en tiempo real

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif" alt="Demostración de búsqueda de hoteles con TourMind" width="720" />
  </a>
</div>

### 2. Comparar habitaciones reales

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif" alt="Demostración de comparación de habitaciones con TourMind" width="720" />
  </a>
</div>

### 3. Verificar la tarifa final y pagar

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif" alt="Demostración de verificación y pago de hotel con TourMind" width="720" />
  </a>
</div>

## Capacidades principales

- **Hoteles:** Busca hoteles y habitaciones disponibles en todo el mundo, compara precios en tiempo real y consulta fotos, instalaciones, comidas y condiciones de cancelación. También permite volver a verificar la disponibilidad y gestionar la reserva, el pago y la cancelación.
- **Vuelos:** Busca aeropuertos y vuelos de ida, ida y vuelta o multidestino; compara horarios, clases de cabina, escalas, equipaje y precios totales; después vuelve a comprobar la tarifa elegida y permite reservar, consultar el estado de la reserva y pagar.
- **Planificación completa del viaje:** Pide al agente que prepare un itinerario y busque vuelos y hoteles de acuerdo con tus fechas, presupuesto y preferencias.
- **Transacciones más seguras:** Una búsqueda nunca crea una reserva. Antes de reservar un hotel o vuelo, cancelar una reserva de hotel que lo permita o pagar, el agente muestra la información importante y espera tu confirmación explícita.
- **Conversación natural:** Explica lo que necesitas en tu idioma preferido, sin rellenar formularios de búsqueda complicados.

## Agentes compatibles

TourMind Booking Skills funciona con ChatGPT (modo Work o Codex), Claude Code, WorkBuddy, QClaw, Marvis, OpenClaw, Kimi Work, Doubao Work Mode, Qwen Work Mode, Hermes, Cursor y otros agentes compatibles con Skills.

## Elige la integración de TourMind adecuada

Este repositorio de Skills reúne las funciones de hotel y vuelo para usuarios particulares (ToC) y empresariales (ToB). Las integraciones MCP tienen una estructura diferente, así que elige la opción que corresponda a tu caso.

| Integración | Usuarios | Funciones | Repositorio |
|---|---|---|---|
| TourMind Booking Skills | ToC y ToB | Skills de hotel y vuelo | **[Este repositorio](https://github.com/tourmind-com/Tourmind-Booking-Skills)** |
| MCP de hoteles — Particular (ToC) | ToC | Búsqueda y reserva de hoteles para usuarios particulares | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| MCP de hoteles — Empresa (ToB) | ToB | Búsqueda y reserva de hoteles para usuarios empresariales | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |
| MCP de vuelos — Particular y empresa | ToC y ToB | Un único MCP de vuelos compartido por usuarios particulares y empresariales | [Flight Booking AI MCP](https://github.com/tourmind-com/flight-booking-ai-mcp.git) |

## Instalación en 1 minuto

Elige uno de estos dos métodos.

### Pide a tu agente que lo instale

Copia y envía este mensaje a tu agente:

```text
Ayúdame a instalar TourMind Booking Skills. Repositorio del Skill: git@github.com:tourmind-com/Tourmind-Booking-Skills.git.
```

### O ejecuta un solo comando

```bash
npx skills add tourmind-com/tourmind-booking-skills
```

Puedes buscar y comparar hoteles, y consultar aeropuertos, sin Token. Se necesita un Token para buscar y verificar vuelos en tiempo real y para cualquier operación real de reserva, consulta del estado o pago.

Si ya tienes una cuenta de TourMind, puedes usar el [Skill Token](https://tourmind.com/user/skill-token) de tu cuenta. Los desarrolladores y usuarios particulares pueden obtener un Token compatible en [auth.journione.ai](https://auth.journione.ai). Envíalo únicamente a un agente de confianza y en una conversación privada:

```text
Usa el siguiente TourMind Skill Token con los Skills de IA:
<YOUR_SKILL_TOKEN>

Este Token se utiliza únicamente para autenticar los Skills de IA de TourMind. No expongas el Token completo en conversaciones públicas, repositorios de código públicos ni documentos compartidos.
```

El agente guardará y configurará el Token para los Skills instalados. No necesitas crear ni editar tú mismo ningún archivo de Token.

Después de instalarlo, solo tienes que pedir al agente que busque un hotel, encuentre un vuelo o planifique ambos juntos.

## Ejemplos de prompts

### Buscar un hotel

```text
Busca un hotel en Tokio para dos adultos del 9 al 13 de diciembre de 2026. Queremos una habitación con dos camas cerca de una estación bien comunicada, con un precio medio inferior a 18.000 JPY por noche, cancelación gratuita y desayuno si es posible. Muestra las cinco mejores opciones disponibles con fotos de la habitación, precio total de la estancia, comidas, condiciones de cancelación y las principales ventajas e inconvenientes. No reserves todavía.
```

### Buscar un vuelo

```text
Busca vuelos de ida y vuelta de Shanghái a Tokio para dos adultos, con salida el 9 de diciembre y regreso el 13 de diciembre de 2026. Clase Turista, preferiblemente sin escalas. Compara las opciones disponibles por precio total, horarios de salida y llegada, aeropuertos, escalas, duración y equipaje. Muestra la franquicia de equipaje facturado de cada opción y destaca las que incluyan al menos una pieza por persona. No reserves todavía.
```

### Planificar vuelo y hotel juntos

```text
Planifica un viaje de cinco días a Osaka para dos personas. Primero compara vuelos de ida y vuelta con horarios prácticos y después busca un hotel bien situado que se ajuste a nuestras fechas y presupuesto. Explica las mejores combinaciones de vuelo y hotel y muestra por separado los costes estimados del vuelo y del hotel. Espera a que elija antes de reservar nada.
```

### Continuar con un hotel que te gusta

```text
Me gusta el hotel cerca de la estación de Shinjuku que acabas de recomendar. Comprueba qué habitaciones con dos camas siguen disponibles, vuelve a verificar la opción con mejor relación calidad-precio y muéstrame el precio final, las comidas incluidas y las condiciones de cancelación. Dime qué información necesitas a continuación y espera mi confirmación antes de reservar.
```

### Continuar con un vuelo que te gusta

```text
El vuelo directo de la mañana que acabas de mostrarme es el que más me conviene. Vuelve a comprobar el precio total más reciente y después resume el itinerario y la franquicia de equipaje facturado. Dime qué datos de los pasajeros y de contacto necesitas, muéstrame el resumen completo y espera mi confirmación antes de reservarlo.
```

### Consultar una reserva

```text
Consulta la reserva de hotel o vuelo que acabamos de hacer y explícame su estado actual. Si todavía se puede pagar, muéstrame primero los métodos de pago disponibles y el importe final; después espera mi confirmación antes de continuar.
```

## Flujos de reserva

El agente realiza estos pasos dentro de la conversación. No necesitas llamar a las API ni gestionar archivos locales por tu cuenta.

### Búsqueda y reserva de hoteles

```text
Destino, fechas, ocupación, número de habitaciones, presupuesto y preferencias
  → Resolver la ciudad, zona, lugar u hotel concreto (search_location / búsqueda por nombre)
  → Buscar hasta 20 hoteles candidatos (search_hotels)
  → Verificar en lote habitaciones en tiempo real y totales de estancia (batch_query_room_rates; query_room_rates para un hotel)
  → Ordenar y mostrar hasta cinco hoteles verificados
  → Mostrar los detalles, imágenes y habitaciones en tiempo real del hotel elegido (get_hotel_detail + consulta de tarifas)
  → Revisar los cargos obligatorios de los detalles del hotel y volver a comprobar el precio final, la disponibilidad y las condiciones de cancelación (check_room_availability)
  → Configurar el Token cuando una operación de reserva requiera autenticación; si cambia el canal, actualizar primero las tarifas y, en todos los casos, volver a comprobar el precio final y la disponibilidad con el Token nuevo
  → Proporcionar el nombre legal completo del huésped y el correo electrónico de contacto
  → Mostrar el resumen completo de la reserva y esperar una confirmación explícita
  → Crear la reserva de hotel (create_booking)
  → Consultar la reserva cuando se solicite; iniciar el pago o cancelar una reserva de hotel que lo permita solo después de una confirmación explícita independiente (query_booking / pay_order / cancel_booking)
```

El precio candidato almacenado por `search_hotels` es solo una señal inicial. Los precios reservables que se muestran al usuario proceden de la consulta de habitaciones en tiempo real, y la reserva utiliza los últimos valores de `check_room_availability`. Elegir un hotel o una habitación no confirma la reserva. El pago y la cancelación requieren revisiones y confirmaciones independientes. Si se elige Stripe, el agente explica primero su comisión adicional del 3,5 % y que, una vez cobrada, no es reembolsable.

### Búsqueda y reserva de vuelos

```text
Ruta, fechas, tipo de viaje, cabina, preferencias y número de adultos / niños / bebés
  → Resolver aeropuertos y validar fechas y composición de pasajeros (search_airports)
  → Configurar el Token y buscar vuelos en tiempo real (search_flights)
  → Comparar hasta las 10 primeras ofertas por horarios, aeropuertos, cabina, escalas, equipaje y precio total
  → Elegir una cotización antes de que transcurran 20 minutos desde la búsqueda
  → Volver a comprobar el vuelo elegido y el total más reciente (verify_offer)
  → Proporcionar datos de pasajeros, documentos de viaje y contacto
  → Revisar el itinerario, el precio y los datos completos de los viajeros, y confirmar expresamente la reserva
  → Crear la reserva de vuelo (create_booking)
  → Consultar el pedido y continuar solo si todavía se puede pagar (query_order)
  → Elegir un método de pago, revisar el resumen completo y confirmar el pago por separado
  → Volver a consultar el pedido; solo si no ha cambiado y todavía se puede pagar, crear un único enlace de pago (create_payment)
  → Consultar el estado del pedido o del pago cuando sea necesario (query_order / query_payment)
```

Elegir un vuelo solo autoriza la nueva comprobación del precio; no confirma la reserva. Si cambian los criterios de búsqueda o han transcurrido 20 minutos desde la búsqueda, el agente solicita permiso antes de realizar una nueva búsqueda. Un enlace de pago no demuestra que el pago se haya completado ni que se haya emitido el billete. Stripe añade una comisión de procesamiento no reembolsable del 3,5 %; WeChat Pay, Alipay y Online Banking solo están disponibles para pedidos en CNY.

Actualmente, el Skill de vuelos permite consultar aeropuertos, buscar y verificar vuelos en tiempo real, reservar, consultar pedidos y crear o consultar pagos de terceros. No ejecuta cancelaciones o cambios de vuelos, solicitudes de reembolso, compra de servicios adicionales ni acciones manuales de emisión; para estas solicitudes, contacta con atención al cliente de vuelos.

## Token y seguridad

- Los Skills de hotel y vuelo utilizan el mismo TourMind Skill Token. Cada usuario solo necesita obtenerlo una vez; no hace falta solicitarlo por separado.
- Cuando cualquiera de los Skills instalados necesita autenticación, el agente guarda el mismo Token en el archivo local `skill_token.txt` de ese Skill. Todas las llamadas a la API de los Skills ToB deben usar el Token guardado en el archivo local correspondiente, y no necesitas crear ni editar los archivos por tu cuenta.
- No expongas el Token completo en prompts, registros, capturas de pantalla, URL, commits de Git ni incidencias.
- En macOS o Linux, el agente ejecuta `chmod 600 skill_token.txt` para que solo el usuario actual pueda leer o escribir el archivo del Token.
- Si una solicitud autenticada devuelve HTTP 401 o `unauthorized`, el agente elimina el Token local no válido y detiene la operación autenticada. Una respuesta independiente que indique que un permiso no está habilitado no se considera un Token no válido.
- Las páginas de resultados de hoteles devueltas son de solo lectura y pueden volver a abrirse hasta que caduquen.
- Crear una reserva de hotel o vuelo, cancelar una reserva de hotel que lo permita o iniciar un pago requiere la confirmación explícita del usuario en una conversación de IA autenticada.

## FAQ

[Preguntas frecuentes sobre el uso de TourMind Skill](https://github.com/tourmind-com/Tourmind-Booking-Skills/issues/23#issue-5276313315)

## Ayuda y soporte

- Página del producto: [tourmind.com/skills](https://tourmind.com/skills)
- Token para desarrolladores y usuarios particulares: [auth.journione.ai](https://auth.journione.ai)
- Soporte en GitHub: [abrir una incidencia](https://github.com/tourmind-com/Tourmind-Booking-Skills/issues)
- Soporte de hoteles: [hotel@tourmind.com](mailto:hotel@tourmind.com)
- Atención al cliente de vuelos (24/7): [flightcs1@tourmind.com](mailto:flightcs1@tourmind.com)
- Colaboración comercial: [bp@tourmind.com](mailto:bp@tourmind.com)
- Colaboración en productos de IA: [ai@tourmind.com](mailto:ai@tourmind.com)

## Licencia

[MIT](LICENSE) © 2026 TourMind
