# Frontend Installation Guide

## Quick Install

```bash
npm install
```

## If Installation Fails

### Clear Cache and Reinstall
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Use Yarn Instead
```bash
yarn install
```

### Check Node Version
```bash
node --version  # Should be 18.x or higher
npm --version   # Should be 9.x or higher
```

### Update npm
```bash
npm install -g npm@latest
```

## Running the Frontend

### Development Mode
```bash
npm run dev
```
Opens at `http://localhost:5173`

### Build for Production
```bash
npm run build
```
Output in `dist/` directory

### Preview Production Build
```bash
npm run preview
```

## Troubleshooting

### TypeScript Errors
These are normal before `npm install` runs. They will disappear after installation.

### Port 5173 in Use
```bash
# Kill the process
lsof -ti:5173 | xargs kill -9

# Or change port in vite.config.ts
```

### Module Not Found
```bash
npm install
```

### Build Errors
```bash
rm -rf node_modules package-lock.json dist
npm install
npm run build
```

## Environment Variables

Create `.env` file (optional):
```bash
cp .env.example .env
```

Edit `.env`:
```
VITE_API_URL=http://localhost:8000
```

## IDE Setup

### VS Code
Install recommended extensions:
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- TypeScript Vue Plugin (Volar)

### WebStorm
TypeScript and React support is built-in.

## Verify Installation

```bash
# Check if all dependencies installed
npm list

# Run linter
npm run lint

# Build to verify everything works
npm run build
```

## Common Issues

### "Cannot find module 'react'"
**Solution:** Run `npm install`

### "JSX element implicitly has type 'any'"
**Solution:** Run `npm install` to install @types/react

### Tailwind classes not working
**Solution:** Ensure `tailwind.config.js` and `postcss.config.js` exist

### Hot reload not working
**Solution:** Restart dev server with `npm run dev`

## Dependencies Overview

### Core
- **react**: UI library
- **react-dom**: React DOM renderer
- **react-router-dom**: Routing
- **typescript**: Type safety

### UI & Styling
- **tailwindcss**: Utility-first CSS
- **lucide-react**: Icon library
- **clsx**: Conditional classes

### Data & API
- **axios**: HTTP client
- **date-fns**: Date utilities

### Build Tools
- **vite**: Fast build tool
- **@vitejs/plugin-react**: React plugin for Vite

### Development
- **eslint**: Code linting
- **@types/react**: TypeScript types
- **autoprefixer**: CSS vendor prefixes
