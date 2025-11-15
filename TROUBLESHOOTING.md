# Troubleshooting Guide

## Common Issues and Solutions

### Frontend Issues

#### TypeScript Errors: "Cannot find module 'react'"

**Cause:** Node modules not installed

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### Port 5173 already in use

**Solution:**
```bash
# Kill the process using the port
lsof -ti:5173 | xargs kill -9

# Or change the port in vite.config.ts
```

#### API connection errors (CORS)

**Cause:** Backend not running or CORS misconfiguration

**Solution:**
1. Ensure backend is running on port 8000
2. Check backend logs for CORS errors
3. Verify `CORS_ORIGINS` in `backend/app/config.py`

#### Build fails with "out of memory"

**Solution:**
```bash
# Increase Node memory
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

### Backend Issues

#### ModuleNotFoundError

**Cause:** Virtual environment not activated or dependencies not installed

**Solution:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Database errors: "no such table"

**Cause:** Database not initialized

**Solution:**
```bash
cd backend
python -m app.db.init_db
```

#### Port 8000 already in use

**Solution:**
```bash
# Kill the process
lsof -ti:8000 | xargs kill -9

# Or change port in .env or when running
uvicorn app.main:app --port 8001
```

#### SQLAlchemy errors: "from_attributes"

**Cause:** Pydantic v1 vs v2 compatibility

**Solution:** Already fixed in schemas. If you see this:
```bash
pip install --upgrade pydantic
```

#### File upload fails: "Invalid ZIP"

**Cause:** ZIP structure doesn't match expected format

**Solution:** Ensure ZIP contains:
```
dataset.zip
├── frames/
│   ├── frame_000001.jpg
│   └── ...
└── telemetry.csv
```

#### CSV validation error: "Missing required columns"

**Cause:** telemetry.csv missing required fields

**Solution:** Ensure CSV has these columns:
- frame_id
- timestamp
- ego_speed_mps
- ego_yaw
- road_type
- weather
- lead_distance_m
- cut_in_flag
- pedestrian_flag

### Database Issues

#### SQLite locked

**Cause:** Multiple processes accessing database

**Solution:**
```bash
# Stop all backend processes
pkill -f "uvicorn app.main:app"

# Delete lock file if exists
rm backend/autolab_drive.db-journal

# Restart backend
cd backend && python run.py
```

#### Database corruption

**Solution:**
```bash
# Backup current database
cp backend/autolab_drive.db backend/autolab_drive.db.backup

# Reinitialize
rm backend/autolab_drive.db
python -m app.db.init_db
```

### Setup Issues

#### Virtual environment creation fails

**Solution:**
```bash
# Install venv if not available
sudo apt-get install python3-venv  # Ubuntu/Debian
brew install python3  # macOS

# Or use virtualenv
pip install virtualenv
virtualenv venv
```

#### pip install fails with SSL errors

**Solution:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### npm install fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Use different registry
npm install --registry=https://registry.npmjs.org/

# Or use yarn
yarn install
```

### Runtime Issues

#### Analysis takes too long

**Cause:** Mock LLM has delays or large dataset

**Solution:**
- Check backend logs for errors
- Reduce number of papers in retriever
- Optimize agent pipeline

#### No events detected

**Cause:** Telemetry data doesn't trigger detection rules

**Solution:**
- Check event detection thresholds in `event_detector.py`
- Verify telemetry data has variation
- Add debug logging to see detection logic

#### Genome not updating

**Cause:** Judge decision is "Tie" or changes too small

**Solution:**
- Check judge decision reasoning
- Adjust Meta-Learner thresholds
- Review genome update logic in `meta_learner.py`

### Development Issues

#### Hot reload not working (backend)

**Solution:**
```bash
# Ensure --reload flag is set
uvicorn app.main:app --reload --port 8000
```

#### Hot reload not working (frontend)

**Solution:**
```bash
# Check vite.config.ts
# Restart dev server
npm run dev
```

#### Changes not reflected

**Solution:**
```bash
# Clear browser cache
# Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

# Backend: restart server
# Frontend: restart dev server
```

## Debugging Tips

### Backend Debugging

1. **Enable debug logging:**
```python
# In app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Use breakpoints:**
```python
import pdb; pdb.set_trace()
```

3. **Check API docs:**
Visit `http://localhost:8000/docs` for interactive API documentation

### Frontend Debugging

1. **Open browser console:**
- Chrome/Edge: F12 or Cmd+Option+I (Mac)
- Firefox: F12 or Cmd+Option+K (Mac)

2. **Check network tab:**
- View API requests/responses
- Check for CORS errors
- Verify request payloads

3. **React DevTools:**
Install React Developer Tools browser extension

### Database Debugging

1. **Inspect database:**
```bash
sqlite3 backend/autolab_drive.db
.tables
.schema datasets
SELECT * FROM datasets;
```

2. **Check relationships:**
```sql
SELECT d.name, COUNT(e.id) as event_count 
FROM datasets d 
LEFT JOIN events e ON d.id = e.dataset_id 
GROUP BY d.id;
```

## Performance Optimization

### Backend

1. **Use PostgreSQL instead of SQLite:**
```bash
# Install PostgreSQL
pip install psycopg2-binary

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:pass@localhost/autolab_drive
```

2. **Add caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function():
    pass
```

3. **Async processing:**
```bash
pip install celery redis
# Configure Celery for background tasks
```

### Frontend

1. **Optimize bundle size:**
```bash
npm run build
npm run preview
```

2. **Lazy load components:**
```typescript
const StrategiesPage = lazy(() => import('./pages/StrategiesPage'))
```

3. **Memoize expensive computations:**
```typescript
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b])
```

## Getting Help

### Check Logs

**Backend logs:**
```bash
cd backend
python run.py 2>&1 | tee backend.log
```

**Frontend logs:**
Check browser console

### Verify Installation

```bash
# Backend
cd backend
source venv/bin/activate
python -c "import fastapi; print(fastapi.__version__)"

# Frontend
cd frontend
npm list react
```

### Clean Install

If all else fails, start fresh:

```bash
# Backend
cd backend
rm -rf venv
rm autolab_drive.db
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Still Having Issues?

1. Check the GitHub Issues page
2. Review ARCHITECTURE.md for system design
3. Read QUICKSTART.md for setup steps
4. Check API documentation at `/docs`
5. Enable debug logging and inspect output

## Common Error Messages

### "No module named 'app'"

**Solution:** Run from backend directory or set PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### "UNIQUE constraint failed"

**Solution:** Trying to create duplicate record. Check database state.

### "404 Not Found" on API calls

**Solution:** 
- Verify backend is running
- Check API endpoint URL
- Review FastAPI routes in `app/api/routes.py`

### "Failed to fetch"

**Solution:**
- Backend not running
- CORS issue
- Network connectivity problem
- Check browser console for details
