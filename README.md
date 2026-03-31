# 👻 Taller Interactivo: Pacman y Aprendizaje por Refuerzo (Reinforcement Learning)

¡Bienvenido al código fuente de la plataforma diseñada para dar charlas interactivas de Inteligencia Artificial en colegios y universidades!

Este proyecto es una adaptación nativa para la nube (Cloud-Native) del clásico laboratorio de *Reinforcement Learning* de la Universidad de Berkeley (CS188). Se transformó la interfaz gráfica original de escritorio en una aplicación web interactiva `Flask + SocketIO` que soporta la participación de +40 estudiantes simultáneamente desde sus teléfonos celulares.

**Docente / Creador:** Data Scientist Marco Cedeño

---

## 🌟 Características Principales

1. **Juego en Tiempo Real por WebSockets**: Los alumnos no tienen que instalar nada; entran a la URL e interactúan con el algoritmo entrenando a su propio Pacman de forma remota. El backend procesa miles de partidas hiper-tunning por segundo y transmite la partida final renderizada en sus pantallas a 30 FPS.
2. **Dashboard para el Docente (`/admin`)**: 
   - Proyecta un **Código QR dinámico** en la pizarra para que los alumnos ingresen directamente.
   - Cuenta con controles de acceso estrictos: Puedes "Cerrar la Charla" cuando la clase termina o "Abrirla" nuevamente.
3. **Flujo Cero Costo Computacional Local**: Entrenar a 40 robots a la vez derrite la memoria RAM de cualquier computadora personal. Esta plataforma subcontrata TODO el cómputo a Render/Railway (servidores gratuitos), protegiendo tu laptop.
4. **Flipping "Volver a ver"**: Un ingenioso desarrollo permite mantener vivo el cerebro del Pacman tras su examen final. Puedes apretar el botón de "Volver a Ver" para presenciar exactamente las mismas estrategias aprendidas del robot, infinitas veces, sin tener que gastar recursos volviéndolo a entrenar.

---

## ⚙️ Controles en Pantalla (Panel Alumnos)

Cuando los estudiantes ingresan a la plataforma principal, tienen control sobre las hiperparametrizaciones del algoritmo de Q-Learning.

* **Aprendizaje (Alpha - $α$)**: Tasa de aprendizaje. Determina si el Pacman asimila rápido las nuevas experiencias o prefiere recordar las viejas.
* **Exploración (Epsilon - $ε$)**: Probabilidad de tomar un camino al azar. Si es muy alto, Pacman será muy "curioso", si es muy bajo, preferirá hacer solo lo que ya conoce.
* **Episodios**: Cantidad de "vidas" que tiene Pacman en el motor invisible para jugar ultra rápido al ensayo/error antes de dar su examen final.

**Nuevos Botones Inteligentes:**
- **INICIAR ENTRENAMIENTO**: Ejecuta el algoritmo desde cero, perdiendo el cerebro anterior (amnesia total).
- **VOLVER A VER (Mismo Ent.)**: Solicita al servidor jugar una partida extra de "Examen Dificultad Normal" usando los **mismos valores cerebrales** del entrenamiento recién finalizado. Perfecto para debatir con los alumnos por qué el robot tomó una decisión sin perder 2 minutos esperando que aprenda todo de nuevo.

---

## 🚀 Despliegue en Cloud (Render.com)

Esta aplicación viene "Baterías Incluídas" y su estructura está lista para ser leída por Render (utilizando Gunicorn y Eventlet pre-configurados en `Procfile` y `requirements.txt`).

**Pasos de Despliegue:**
1. Crea un repositorio en tu GitHub y sube estos archivos.
2. Ingresa a [Render.com](https://render.com) > *New Web Service*.
3. Selecciona tu repositorio de GitHub recién creado.
4. Render leerá automáticamente los requisitos e instalará todo usando **Python 3**.
5. Disfruta de la plataforma pública sin ninguna configuración adicional de puertos o redes (Ngrok ha sido completamente removido; el URL se detecta automáticamente).

---

## 💻 Panel de Control (Admin)

Una vez desplegada en Render tu URL `https://taller-pacman-reinforcement.onrender.com`. 
Solo los profesores deben entrar a **`https://taller-pacman-reinforcement.onrender.com/admin`** para proyectarlo.
- **Botón Rojo (Terminar Charla)**: Expulsa a todo el colegio y rechaza nuevos alumnos bloqueando la raíz de la web.
- **Botón Verde (Abrir Charla)**: Vuelve a habilitar el acceso. Ideal si llega alguien atrasado o decides dar dos bloques continuos del taller.
