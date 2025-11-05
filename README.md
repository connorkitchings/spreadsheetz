# Vibe Coding Data Science Template

Welcome to the Vibe Coding Data Science Template! This repository provides a
production-ready, highly automated foundation for data science and machine
learning projects. It is built on the principles of the Vibe Coding System,
emphasizing observability, reproducibility, and efficient AI-assisted
collaboration.

This template is not just another collection of files; it's a **system** designed to accelerate
data science projects by solving common pain points out-of-the-box. It enforces best practices
in a lightweight, automated way so you can focus on building, not boilerplate.

For a deep dive into the methodology and guides, please see our
[full documentation site](./docs/index.md).  
If you're converting this template into a named project, start with the
[Template Kickoff Guide](./docs/template_starting_guide.md) to capture scope,
owners, and required doc/code updates.

---

## 🚀 Getting Started

If you're adopting this repository for a production project, complete the
[Template Kickoff Guide](./docs/template_starting_guide.md) to document scope,
owners, and initial decisions before running the steps below.

### Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)
- [Docker](https://www.docker.com/get-started)
- [pre-commit](https://pre-commit.com/#installation)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install dependencies:**

    ```bash
    uv sync
    ```

3.  **Install pre-commit hooks:**

    ```bash
    pre-commit install
    ```

### Running the project

1.  **Run the example flow:**

    ```bash
    prefect server start &
    python src/vibe_coding/flows/example_flow.py
    ```

2.  **Run the tests:**

    ```bash
    pytest
    ```

3.  **Build the documentation:**

    ```bash
    mkdocs serve
    ```

---

## 📂 Project Structure

```text
.vibe-coding-template/
├── .github/              # GitHub Actions workflows and templates
├── data/                 # Raw and processed data (not committed)
├── docs/                 # Project documentation
├── models/               # Trained model artifacts (not committed)
├── notebooks/            # Jupyter notebooks for exploration and analysis
├── reports/              # Generated reports and figures
├── scripts/              # Utility and automation scripts
├── session_logs/         # Chronological development session logs
├── src/                  # Project source code
│   ├── vibe_coding/      # Source code for the project
│   │   ├── flows/        # Prefect orchestration flows
│   │   └── utils/        # Shared utility modules
│   └── tests/            # Unit and integration tests
├── .dockerignore         # Files to ignore in Docker builds
├── .gitignore            # Files to ignore in Git
├── .pre-commit-config.yaml # Configuration for pre-commit hooks
├── Dockerfile            # Multi-stage Dockerfile for containerization
├── mkdocs.yml            # Configuration for MkDocs
├── prefect.yaml          # Configuration for Prefect deployments
├── pyproject.toml        # Project metadata and dependencies
└── README.md             # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
