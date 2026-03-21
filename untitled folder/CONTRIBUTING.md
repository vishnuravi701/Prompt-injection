# Contributing Guide

## Code Style

### Python (Backend)
- Follow PEP 8 standards
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Utilize type hints where possible

Example:
```python
def analyze_prompt(prompt: str) -> dict:
    """Analyze a prompt for injection patterns"""
    pass
```

### JavaScript/React (Frontend)
- Use ES6+ features
- Follow Airbnb style guide
- Use functional components
- Use React hooks

Example:
```javascript
function PromptInput({ onAnalyze, loading }) {
  const [input, setInput] = useState('');
  // ...
}
```

## Git Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "feat: add new feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Create Pull Request

## Commit Messages

Follow Conventional Commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `style:` formatting
- `refactor:` code change without feature/fix
- `chore:` dependency, maintenance
- `test:` adding tests

Example: `feat: add prompt injection detection endpoint`

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest -v
pytest --cov
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## Pull Request Checklist

- [ ] Code follows project style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tested locally
- [ ] No hardcoded secrets/API keys

## Issues & Bug Reports

When reporting issues, include:
1. Description of the bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment (OS, Python/Node version)
6. Screenshots if applicable

## Feature Requests

Include:
1. Problem statement
2. Proposed solution
3. Alternative solutions
4. Implementation complexity estimate
5. Use cases

## Development Setup

See [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md) for detailed setup guide.

## Questions

- Ask in GitHub Issues
- Check existing documentation
- Review similar implementations

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
