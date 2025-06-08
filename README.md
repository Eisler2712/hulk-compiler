# Compilador para el Lenguaje HULK

## Descripción General

Compilador diseñado para el lenguaje de programación HULK. Este proyecto implementa el análisis léxico, sintáctico y semántico para la traducción de código fuente `.hulk` a un lenguaje intermedio o código objeto.

## Autores y Colaboradores

El desarrollo de este compilador ha sido realizado por:

- **Rafael Acosta Márquez** ([GIT](https://github.com/theGitNoob)), C411
- **Eisler Francisco Valles Rodríguez** ([GIT](https://github.com/Eisler2712)), C411

## Guía de Compilación y Uso

Para compilar y ejecutar un programa utilizando el compilador HULK, siga los pasos que se detallan a continuación.

### 1. Construcción del Compilador

Inicialice el entorno de compilación ejecutando el siguiente comando en el directorio raíz del proyecto. Este paso genera el analizador léxico (Lexer) y el autómata del analizador sintáctico (Parser):

```bash
make build
```

### 2. Creación del Archivo Fuente

Cree un archivo `main.hulk` en el directorio raíz del proyecto. Este archivo contendrá el código fuente que desea compilar.

### 3. Proceso de Compilación Completo

Para analizar el código fuente en `main.hulk` y generar el ejecutable final, utilice el comando `make`. Este comando automatiza todo el proceso de compilación:

```bash
make
```

### Comandos Adicionales

-   **Compilación del Código Intermedio:** Si desea compilar únicamente el archivo C generado a partir del código HULK, ejecute:

    ```bash
    make compile
    ```

-   **Ejecución de Pruebas:** Para verificar la integridad y el correcto funcionamiento del compilador, puede ejecutar la suite de pruebas automatizadas con el siguiente comando:

    ```bash
    make test
    ```
