# Lucenette AI

<img src="./avatar.jpg" width="300" />

> **Design philosophy**: *She listens like snow. She connects like a net.*

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE) ![Status](https://img.shields.io/badge/Status-design%20phase-orange)

> ⚠️ **Current status**: This project is in the **design phase**. The architecture is fully documented, but **no module has been implemented yet**. The primary documentation is written in Chinese — see [README.md](./README.md) or [docs/](./docs/).

## What is this

Lucenette is a general-purpose **agent operating system** built around a large language model as its core brain, a distributed scheduling network as its nervous system, plug-and-play device abstractions as its senses and limbs, and a management-plane service as its operations hub. The goal is not another chatbot, but a digital-life system with proactive thinking, multimodal interaction, environment sensing, device control, and self-monitoring.

## Key ideas

- **Dual-core architecture**: the conscious mind (main LLM core, event-driven) plus the subconscious mind (thinking subsystem, 24/7 background thinking);
- **Words and deeds align**: a single inference emits both dialogue text and control tags;
- **Everything is a plugin**: all capabilities (built-in functions, physical devices, MCP plugins) are registered and can be toggled at runtime;
- **Thin center, autonomous edge**: the middle scheduler only routes; end schedulers execute autonomously;
- **Non-intrusive management**: the management plane pulls metrics one-way and never touches the realtime path.

## Implementation status

All modules: **not implemented** (design docs only). See the status matrix in [README.md](./README.md) or [docs/index.md](./docs/index.md).

## Documentation

The design documentation is written in Chinese and organized as follows:

| Path | Content |
|------|---------|
| [docs/00-global/](docs/00-global/) | Glossary, design principles, architecture overview, tech stack, ADRs |
| [docs/01-contracts/](docs/01-contracts/) | Cross-module contracts (standard command, message envelope, management API, metrics, tool registry, device descriptor) |
| [docs/02-modules/](docs/02-modules/) | Module specs M01–M09 (one work package each) |
| [docs/03-standards/](docs/03-standards/) | Coding style, module doc template, testing & acceptance |
| [docs/04-delivery/work-packages.md](docs/04-delivery/work-packages.md) | Work-package board |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) (Chinese). RFC proposals live in [docs/rfcs/](docs/rfcs/). Please follow our [Code of Conduct](./CODE_OF_CONDUCT.md).

## License

MIT — see [LICENSE](./LICENSE).

**Disclaimer**: This is an academic research tool. Generated content does not represent the views of the maintainers. Users are fully responsible for the content they generate.

