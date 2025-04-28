# Flask Microservice Demo

This project is an example of using nothing but python3, flask, requests, and docker to make a complete microservice architecture implementation.  Yes, it passes JSON around in between the microservices, which is arguably not a great idea, but it's hard to argue with how easy these are to spin up.

## Architecture Diagram

Here's the architecture diagram:

_Edit: I added another GET to the backend to test the custSearch functionality and demo a JSON payload in client. Details below._

![Architecture Diagram](https://i.imgur.com/IUAfN8O.png)

For testing fun all of the microservices are exposed, but in a real application only the backend (or API) would be.

## Description of the containers

There are four different docker images that are build for this demo. Backend is the API layer and it has three GET methods as illustrated in the diagram. For order details you can specify an integer from 1 to 1000. If you specify the count parameter it will show the first # of orders up to the count you specify.

The aggregate which is exposed locally on port 5003 combines information from the orders data service and the items data service. It has a single method which will actually return exactly the same thing as the backend /detail/ method, but of course you haven't exposed the aggregate microservice in the real world, and you'd do other value-add things in the API layer like authentication.

The orders microservice is a data service, and typically you'd be going after a database of some kind. Here a faker is used to create 1000 orders and they're kept in memory for the life of the run. The /custSearch method (which isn't used by the backend currently, but demonstrates how to take a JSON payload, much like you would pass to a microservice via a gRPC request or your preferred equivalent) can be queried through postman or some other REST testing interface. You'd set the "content-type" to "application/json" and provide a JSON payload like:

```json
{
  "name": "Daniel"
}
```

Lastly the items microservice provides information about 100 randomly created items. This one is never used directly by the backend, but indirectly through the aggregate. Again, this would be a database of some sort in the real world.

## Running it

You need docker and docker-compose. Follow your OS instructions for doing that.  The docker images start with Alpine and install Python3. The only dependencies in Python are Flask, Faker, and requests.

## Testing it

With the docker-compose running and postman, try the following URLS:

### A bunch of raw orders:

http://localhost:5000/orders?count=10

```json
[
    {
        "cust": "Mr. James Edwards",
        "id": 1,
        "items": [
            88,
            2,
            38,
            59,
            52,
            95,
            32,
            68,
            17
        ]
    },
    {
        "cust": "Sarah Taylor",
        "id": 2,
        ...and so on...
    }
    ...and so on...
]
```

### An order detail

http://localhost:5000/detail/5

Notice how the "items" element has been replaced with a list of item details.

```json
{
    "cust": "John Martinez",
    "id": 6,
    "items": [
        {
            "desc": "synthesize plug-and-play interfaces",
            "id": 72
        },
        {
            "desc": "target open-source action-items",
            "id": 18
        },
        {
            "desc": "grow dynamic web services",
            "id": 86
        },
        {
            "desc": "synthesize plug-and-play interfaces",
            "id": 72
        },
        {
            "desc": "streamline synergistic e-commerce",
            "id": 37
        }
    ]
}
```

### Customer name search

http://localhost:5000/custSearch/Dan

You can now hit this URL directly with a GET to perform a search by partial customer name. A space is just '%20'. This calls the underlying custSearch endpoint for the orders microservice, but takes the name and forms a JSON payload which is possibly a more familiar way to send data to a microservice for it to operate on rather than doing it through parameters.  Again Flask makes this absurdly simple.


### Test the search in the data microservice

POST http://localhost:5001/custSearch

*Note the port of the orders microservice here! This isn't the backend!*

Make sure to use a POST and to set "Content-Type: application/json" in the "headers" and to put something like `{"name": "Daniel"}` in the "body".  You'll get a list of order where the "cust" field contains the search parameter. The customer names are randomly generated, so you might want to try something simple.

REFACTORIZACIÓN

**¿Qué camnbios se hicieron y por qué?**

# Refactorización de Rutas en la Arquitectura de Microservicios

Hemos implementado una completa estandarización de rutas en todos nuestros microservicios para establecer una API RESTful más coherente y predecible. El servicio de órdenes ahora utiliza `/orders` para la colección completa y `/orders/<id>` para recursos individuales, abandonando las antiguas rutas `/allOrders` y `/order/<id>`. Aplicamos este mismo criterio en el servicio de ítems, reemplazando `/allItems` y `/item/<id>` por `/items` y `/items/<id>`, respectivamente.

La ruta para consultar detalles agregados se reestructuró de `/detail/<id>` a `/orders/<id>/detail`, haciendo explícito que este endpoint proporciona información detallada de una orden específica, incluyendo los ítems asociados a ella.

Como parte de la limpieza de la API, eliminamos endpoints redundantes o experimentales. En particular, suprimimos la ruta `POST /custSearch` tanto en el servicio de órdenes como en el gateway, ya que duplicaba funcionalidad. En el futuro, las búsquedas por cliente se implementarán mediante parámetros de consulta (`/orders?customer=<nombre>`), siguiendo las mejores prácticas REST.

Para permitir acceso directo a la información de ítems, incorporamos en el API Gateway dos nuevos proxies: `GET /items` y `GET /items/<id>`. Esta configuración refuerza el principio de responsabilidad única en cada servicio —órdenes, ítems y agregación de datos— mientras el gateway orquesta el acceso de forma transparente.

La asignación de puertos quedó establecida de la siguiente manera: API Gateway en puerto 5000, Orders Service en 5001, Items Service en 5002 y Aggregate Service en 5003. Esta distribución facilita la identificación y el escalamiento independiente de cada componente.

Complementamos estas mejoras arquitectónicas con documentación interna exhaustiva en cada archivo de servicio, describiendo la funcionalidad de los endpoints, parámetros, flujos de llamadas entre servicios y puntos de entrada. Estos comentarios proporcionan claridad para desarrolladores actuales y futuros, facilitando la comprensión del proyecto y preparando la base para próximas ampliaciones como paginación, filtrado avanzado e implementación de capas de autenticación y manejo de errores.

Finalmente, sugerimos la utilización de Postman para poder llevar a cabo estás consultas. El código a importar es el siguiente:
{
  "info": {
    "name": "Flask Microservice Demo – Refactorización",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Backend | GET /orders?count=10",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/orders?count=10",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["orders"],
          "query": [
            { "key": "count", "value": "10" }
          ]
        }
      }
    },
    {
      "name": "Backend | GET /detail/:id",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/detail/5",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["detail", "5"]
        }
      }
    },
    {
      "name": "Backend | GET /items",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/items",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["items"]
        }
      }
    },
    {
      "name": "Backend | GET /items/:id",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/items/3",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["items", "3"]
        }
      }
    },
    {
      "name": "Orders Service | GET /orders",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5001/orders",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5001",
          "path": ["orders"]
        }
      }
    },
    {
      "name": "Orders Service | GET /orders/:id",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5001/orders/5",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5001",
          "path": ["orders", "5"]
        }
      }
    },
    {
      "name": "Items Service | GET /items",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5002/items",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5002",
          "path": ["items"]
        }
      }
    },
    {
      "name": "Items Service | GET /items/:id",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5002/items/5",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5002",
          "path": ["items", "5"]
        }
      }
    },
    {
      "name": "Aggregate Service | GET /orders/:id/detail",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5003/orders/5/detail",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5003",
          "path": ["orders", "5", "detail"]
        }
      }
    }
  ]
}


