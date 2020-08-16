from epigraphdb_common_utils import (
    api_docs_env_configs,
    api_env_configs,
    docker_api_private_env_configs,
    docker_api_public_env_configs,
)


def check() -> None:
    print("\n# Check environment configs for API server")
    print(api_env_configs.__doc__)
    print(api_env_configs.configs)
    print("\n# Check environment configs for API documentation")
    print(api_docs_env_configs.__doc__)
    print(api_docs_env_configs.configs)
    print("\n# Check environment configs for private API container")
    print(docker_api_private_env_configs.__doc__)
    print(docker_api_private_env_configs.configs)
    print("\n# Check environment configs for public API container")
    print(docker_api_public_env_configs.__doc__)
    print(docker_api_public_env_configs.configs)


if __name__ == "__main__":
    check()
