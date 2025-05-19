# Proyecto Chatbot con RAG

Este proyecto implementa un chatbot utilizando la arquitectura RAG (Retrieval Augmented Generation). Combina la potencia de un modelo de lenguaje grande con la capacidad de recuperar información relevante de una base de conocimiento para generar respuestas más precisas y contextualizadas.

## Prerrequisitos

Antes de iniciar el proyecto, asegúrate de tener instalado lo siguiente:

* **uv**: Un administrador de paquetes de Python rápido, escrito en Rust. Lo usaremos para gestionar las dependencias del proyecto.
    * Sitio web oficial: (https://docs.astral.sh/uv/getting-started/installation/)
* **Ollama**: Una herramienta para ejecutar modelos de lenguaje grandes localmente. Necesitarás descargar e instalar Ollama para poder usar los modelos de IA.
    * Sitio web oficial: (https://ollama.com/)
* **Chocolatey** (Solo para Windows): Un administrador de paquetes para Windows. Si usas Windows, Chocolatey facilita la instalación de herramientas como `make`.
    * Sitio web oficial: (https://chocolatey.org/install)
* **make**: Una utilidad que controla la generación de ejecutables y otros archivos a partir de los archivos fuente de un programa. Lo usaremos para simplificar el proceso de inicio del proyecto.

## Instalación de Prerrequisitos

Sigue las instrucciones de instalación de los sitios web oficiales para cada herramienta según tu sistema operativo:

* **uv**: Consulta la sección de instalación en el sitio web oficial de uv.
* **Ollama**: Descarga e instala la versión adecuada para tu sistema operativo desde el sitio web oficial de Ollama.
* **Chocolatey** (Solo para Windows): Sigue las instrucciones de instalación en el sitio web oficial de Chocolatey.
* **make**:
    * En sistemas basados en Debian/Ubuntu, puedes instalarlo con `sudo apt update && sudo apt install make`.
    * En macOS, generalmente viene incluido con las herramientas de desarrollo Xcode. Si no lo tienes, puedes instalarlas ejecutando `xcode-select --install`.
    * En Windows, si instalaste Chocolatey, puedes instalar make ejecutando `choco install make`.

## Configuración de Modelos de IA con Ollama

Una vez que tengas Ollama instalado, necesitarás descargar un modelo de lenguaje grande y el modelo de embeddings `nomic-embed-text`.

1.  **Descargar un modelo de IA**: Elige un modelo de la librería de Ollama ([https://ollama.com/library](https://ollama.com/library)) y descárgalo usando el comando `ollama pull <nombre_del_modelo>`. Por ejemplo:
    ```bash
    ollama run llama3.2
    ```
    (Puedes reemplazar `llama3.2` con el nombre del modelo que prefieras).

2.  **Descargar el modelo de embeddings `nomic-embed-text`**: Este modelo es necesario para el componente de recuperación del RAG.
    ```bash
    ollama pull nomic-embed-text
    ```
    * Página del modelo `nomic-embed-text` en la librería de Ollama: [https://ollama.com/library/nomic-embed-text](https://ollama.com/library/nomic-embed-text)

## Instalación del Proyecto

1.  Clona este repositorio:
    ```bash
    git clone https://github.com/SDiaz0415/IAProyecto.git
    cd IAProyecto
    ```

## Inicio del Proyecto

Para iniciar el chatbot, ejecuta el siguiente comando en la consola dentro del directorio del proyecto:

```bash
make run