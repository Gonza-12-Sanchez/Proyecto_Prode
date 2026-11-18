# Prode MVP Frontend

## Descripción
Frontend modular del MVP de Prode — Torneos de Pronósticos. Se conecta al backend FastAPI en `http://localhost:8002`.

## Estructura
```
frontend/
├── index.html          # Esqueleto HTML sin CSS/JS inline
├── css/
│   └── style.css       # Todos los estilos (dark theme)
├── js/
│   ├── app.js          # Clase App principal, navegación de tabs
│   ├── api.js          # Funciones fetch wrapper, gestión de JWT
│   ├── auth.js         # Registro, login, perfil
│   ├── leagues.js      # Carga y visualización de ligas
│   ├── tournaments.js  # Crear torneo, unirse, ver detalle
│   ├── predictions.js  # Formularios de predicción
│   ├── leaderboard.js  # Tabla de rankings
│   └── utils.js        # Funciones utilitarias (formatDate, showAlert, showTable)
└── README.md
```

## Cómo correr
1. Asegúrate de que el backend FastAPI está corriendo en `http://localhost:8002`
2. Abre el navegador en `http://localhost:8002`
3. El backend monta `/static` desde `frontend/` y sirve `index.html` en `/`

## Autenticación
- JWT guardado en `localStorage` con clave `'prode_token'`
- Todos los fetch usan `Authorization: Bearer <token>`

## Módulos JS
Todos los archivos JS usan ES6 modules (`export`/`import`):
- `api.js` — funciones de red (`setToken`, `getToken`, `apiPost`, `apiGet`, `authHeaders`)
- `utils.js` — utilidades (`formatDate`, `showAlert`, `showTable`, `escapeHtml`)
- `auth.js` — autenticación (`register`, `login`, `loadProfile`)
- `leagues.js` — ligas (`load`)
- `tournaments.js` — torneos (`create`, `join`, `load`, `viewDetail`, `populateSelects`)
- `predictions.js` — predicciones (`loadMatches`, `makePrediction`)
- `leaderboard.js` — leaderboard (`load`)
- `app.js` — orquestador principal (`App.showTab`, `App.init`, `App.updateAuthUI`)
