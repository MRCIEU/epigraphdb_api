from app.resources.dependent_files import dependent_files
from epigraphdb_common_utils import (
    api_docs_env_configs,
    api_env_configs,
    docker_api_env_configs,
)


def check_dependent_files() -> None:
    print("\n# Check dependent files")
    for name, path in dependent_files.items():
        exist = path.exists()
        exist_str = "existed" if exist else "NOT exist!"
        print(f"Dependent file {name}\t {path}\t {exist_str}")


def check_env_configs() -> None:
    print("\n# Check environment configs")
    print("\n## Check environment configs for API server")
    print(api_env_configs.__doc__)
    print(api_env_configs.env_configs)
    print("\n## Check environment configs for API documentation")
    print(api_docs_env_configs.__doc__)
    print(api_docs_env_configs.env_configs)
    print("\n## Check environment configs for private API container")
    print(docker_api_env_configs.__doc__)
    print(docker_api_env_configs.env_configs)


if __name__ == "__main__":
    check_dependent_files()
    check_env_configs()
