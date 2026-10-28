# 1 · Tools, credentials and local startup

[Walkthrough index](README.md) · [Next: application flow](02-project-and-application-flow.md)

## 1. A repository is the source, not the running application

The existing project is `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws`. Work in that directory. It is independent of the original Java project and the separate Python project. Git records reviewed source; containers and databases have their own runtime state.

```bash
cd /Users/robertovalencia/Documents/Business/linked-in-node-and-aws
git status --short
```

An empty status means no tracked/untracked changes to report, not that the application is healthy. If changes appear, inspect them before switching branches or reinstalling anything. Do not reset someone else's work to obtain a clean status.

## 2. Know what each tool contributes

| Tool | Job here | Read-only check |
|---|---|---|
| Git | Source history and reviewable changes | `git --version` |
| Node.js 22+ and npm | Run JavaScript/tools and install locked packages | `node --version`, `npm --version` |
| Docker Desktop/Compose v2 | Run services, PostgreSQL and Kafka locally | `docker version`, `docker compose version` |
| Terraform CLI | Learn infrastructure mechanics; prepare reviewed cloud plans | `terraform version` |
| Python 3 | Run standard-library lab/validation scripts | `python3 --version` |
| AWS CLI | Account operations in the separate deployment workflow | `aws --version` |
| GitHub CLI | Authenticated repository/workflow operations | `gh --version` |

The last two tools are unnecessary for local marketplace use. Terraform labs require `>=1.10,<2.0`; the recorded lab runs used 1.17.0. Node dependencies are declared separately at the root, backend and frontend. Check the [actual toolchain guide](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/toolchain.md) for editor recommendations and quality tooling. A recommended VS Code extension is not proof it is installed or connected to an external account.

## 3. Create local secrets once

```bash
npm run setup
```

Follow [package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/package.json) to [setup-local.sh](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/scripts/setup-local.sh). The script generates random database passwords and application keys in `.env`, with owner-only file permissions. If `.env` already exists, it keeps it. Rerunning setup is not a password-rotation procedure.

The file is ignored by Git. Check names in source and examples without printing real values. If a database volume already uses an older password, changing `.env` alone does not update that stored database account. Diagnose configuration mismatch before considering destructive reset.

## 4. Start the integrated application

```bash
npm run up
bash scripts/local.sh status
```

[local.sh](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/scripts/local.sh) runs Docker Compose, builds images and waits for declared health checks. Open `http://localhost:8180`. The Compose project is `linked-in-node-local`; it keeps this project's containers distinct from other projects. Its named data volumes survive normal shutdown.

The browser enters through the frontend/proxy. Four backend services own separate capability databases. See [compose.yaml](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/compose.yaml) and [the full setup runbook](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/local-setup.md). Container health is a startup signal; the acceptance suite checks the business flows afterward.

If Docker is unavailable, start Docker Desktop and check its engine. If startup fails, inspect `docker compose ps` and the relevant logs before retrying. A port conflict is different from invalid credentials or an unhealthy dependency.

## 5. Choose integrated mode or hot reload

Integrated mode runs the whole application in containers. Hot reload runs dependencies in Docker and application development processes on the host:

```bash
npm run down
bash scripts/local.sh deps
npm --prefix backend ci
npm --prefix frontend ci
npm run dev
```

Open `http://localhost:5183` in this mode. `npm ci` installs the lock-file versions and replaces that package's dependency installation. It is a reproducibility tool, not an update command. Switching modes prevents two copies competing for the same service ports. Root tooling uses a separate root `npm ci` when needed, such as Playwright browser checks.

## 6. Stop without deleting learning data

```bash
npm run down
```

This stops/removes the project's containers/network while retaining volumes. The script's separately guarded reset deletes local data; it is not routine cleanup. No command in this chapter provisions AWS. AWS credentials and AI API keys are not prerequisites for these local flows.

**Understanding check:** Explain the difference between Git source, an image, a container, `.env`, and a database volume. If login breaks after editing a password, which two places could disagree?
