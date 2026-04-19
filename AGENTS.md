# Repository Guidelines

## Project Structure & Module Organization

SpamShield is a small Python chat application with spam filtering.

- `Chat_Server.py`: threaded TCP chat server on port `5002`; loads `spam_model.pkl`, extracts message features, and blocks spam.
- `Client.py`: command-line TCP client for local chat testing.
- `app.py`: Flask-SocketIO web bridge on port `5000`; connects browser sessions to `Chat_Server.py`.
- `templates/index.html`: web UI template served by Flask.
- `Train_spam_model.py`: trains the scikit-learn `RandomForestClassifier` from `spam_dataset.csv`.
- `spam_dataset.csv` and `spam_model.pkl`: training data and serialized model artifact.
- `GEMINI.md`: project overview and operational notes.

## Build, Test, and Development Commands

Use the local virtual environment when available:

```bash
./venv/bin/python Train_spam_model.py
```

Retrains the spam model and rewrites `spam_model.pkl`.

```bash
./venv/bin/python Chat_Server.py
```

Starts the TCP chat server required by both clients.

```bash
./venv/bin/python Client.py
```

Starts the terminal chat client.

```bash
./venv/bin/python app.py
```

Starts the Flask-SocketIO web app at `http://localhost:5000`. Run `Chat_Server.py` first.

## Coding Style & Naming Conventions

Write Python 3 code with 4-space indentation. Prefer clear function names in `snake_case`, constants in `UPPER_SNAKE_CASE`, and short module-level scripts consistent with the current files. Keep socket setup, feature extraction, model loading, and request handlers separated into functions where practical. Avoid broad `except:` blocks in new code; catch `Exception as e` when the error is intentionally surfaced or logged.

## Testing Guidelines

No automated tests are currently present. For changes to spam detection, retrain with `Train_spam_model.py`, then manually verify both allowed and blocked messages through `Client.py` or the web UI. Suggested smoke test:

1. Start `Chat_Server.py`.
2. Connect two clients.
3. Send a normal message and confirm it broadcasts.
4. Send an obvious spam phrase such as `FREE cash prize at http://example.com` and confirm `[SPAM BLOCKED]`.

If adding tests, place them under `tests/` and use `test_*.py` naming.

## Commit & Pull Request Guidelines

Recent commits use short conventional-style messages, for example `fix: organize-code` and `fix: code-fix`. Continue using `<type>: <summary>` such as `feat: add web spam status` or `fix: handle client disconnect`.

Pull requests should include a concise description, manual test steps, and any model or dataset changes. Include screenshots when changing `templates/index.html` or web UI behavior. Mention whether `spam_model.pkl` was regenerated.

## Security & Configuration Tips

Do not commit secrets. `app.py` currently uses a development `SECRET_KEY`; replace it with environment-based configuration before deployment. Treat `spam_model.pkl` as a generated artifact tied to `spam_dataset.csv` and the feature columns in `Chat_Server.py`.
