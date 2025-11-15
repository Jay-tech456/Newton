# Contributing to AutoLab Drive

Thank you for your interest in contributing to AutoLab Drive! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/Self-Envolving.git
cd Self-Envolving
```

3. Run the setup script:
```bash
./setup.sh
```

4. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Document functions with docstrings
- Maximum line length: 100 characters

```python
def analyze_event(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze an event using multi-agent system.
    
    Args:
        event_data: Event metadata dictionary
        
    Returns:
        Analysis results with lab outputs and judge decision
    """
    pass
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow React best practices
- Use functional components with hooks
- Use meaningful variable names

```typescript
interface EventTimelineProps {
  events: Event[]
  selectedEvent: Event | null
  onEventSelect: (event: Event) => void
}
```

## Project Structure

```
Self-Envolving/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── agents/   # Multi-agent system
│   │   ├── api/      # API routes
│   │   ├── models/   # Database models
│   │   └── services/ # Business logic
│   └── tests/        # Backend tests
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── types/
│   └── tests/        # Frontend tests
└── scripts/          # Utility scripts
```

## Making Changes

### Backend Changes

1. **Adding a new agent:**
   - Create file in `backend/app/agents/`
   - Implement agent interface
   - Add to research lab pipeline
   - Update tests

2. **Adding an API endpoint:**
   - Add route in `backend/app/api/routes.py`
   - Create Pydantic schema in `backend/app/schemas/`
   - Update API documentation
   - Add tests

3. **Modifying database schema:**
   - Update model in `backend/app/models/`
   - Create migration script
   - Update schemas
   - Test with existing data

### Frontend Changes

1. **Adding a new page:**
   - Create component in `frontend/src/pages/`
   - Add route in `App.tsx`
   - Update navigation in `Layout.tsx`
   - Add types if needed

2. **Adding a new component:**
   - Create in `frontend/src/components/`
   - Export from component file
   - Document props with TypeScript
   - Add to relevant pages

3. **Styling:**
   - Use TailwindCSS utility classes
   - Follow existing color scheme
   - Ensure responsive design
   - Test on mobile

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# Start backend and frontend
# Run end-to-end tests
npm run test:e2e
```

## Commit Guidelines

Use conventional commits:

```
feat: Add new genome evolution algorithm
fix: Resolve CORS issue in API
docs: Update QUICKSTART guide
style: Format code with black
refactor: Simplify event detection logic
test: Add tests for judge agent
chore: Update dependencies
```

## Pull Request Process

1. **Before submitting:**
   - Run tests and ensure they pass
   - Update documentation
   - Add/update tests for new features
   - Follow code style guidelines
   - Rebase on main branch

2. **PR Description:**
   - Describe what changes were made
   - Explain why the changes are needed
   - Link related issues
   - Add screenshots for UI changes

3. **Review Process:**
   - Address reviewer feedback
   - Keep PR focused and small
   - Update based on comments
   - Squash commits if requested

## Feature Requests

### Suggesting New Features

1. Check existing issues first
2. Create detailed issue with:
   - Clear description
   - Use cases
   - Proposed implementation
   - Potential challenges

### Priority Areas

We're especially interested in contributions for:

- **Real LLM Integration:** Replace mock LLM with actual APIs
- **Research API Connectors:** arXiv, Semantic Scholar, etc.
- **Advanced Evolution:** Genetic algorithms, multi-objective optimization
- **Visualization:** Better genome evolution visualization
- **Performance:** Caching, async processing, optimization
- **Testing:** More comprehensive test coverage
- **Documentation:** Tutorials, examples, guides

## Bug Reports

### Reporting Bugs

1. Check if bug already reported
2. Create issue with:
   - Clear title
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
   - Screenshots/logs if applicable

### Bug Fix Process

1. Create issue or comment on existing
2. Fork and create branch
3. Fix bug with tests
4. Submit PR referencing issue

## Documentation

### Updating Documentation

- Keep README.md current
- Update QUICKSTART.md for setup changes
- Expand ARCHITECTURE.md for design changes
- Add examples to docs/
- Update API documentation

### Writing Documentation

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep formatting consistent

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on what's best for the project

### Communication

- Use GitHub Issues for bugs/features
- Use Discussions for questions
- Be patient and helpful
- Share knowledge

## Development Tips

### Debugging

1. **Backend:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Frontend:**
```typescript
console.log('Debug:', data)
```

### Hot Reload

- Backend: `uvicorn app.main:app --reload`
- Frontend: `npm run dev` (automatic)

### Database Inspection

```bash
sqlite3 backend/autolab_drive.db
.tables
.schema
SELECT * FROM strategy_genomes;
```

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Build and test production builds
6. Create GitHub release
7. Deploy to production

## Questions?

- Check TROUBLESHOOTING.md
- Review ARCHITECTURE.md
- Ask in GitHub Discussions
- Open an issue for clarification

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you to all contributors who help make AutoLab Drive better!

Special thanks to our sponsors:
- Google DeepMind
- Freepik
- Forethought
