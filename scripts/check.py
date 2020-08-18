from colorama import Fore, Style

from app.resources.dependent_files import dependent_files
from app.settings import epigraphdb, pqtl
from epigraphdb_common_utils import (
    api_docs_env_configs,
    api_env_configs,
    docker_api_env_configs,
)


def check_dependent_files() -> None:
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n# Check dependent files"
        + Style.RESET_ALL
    )
    for name, path in dependent_files.items():
        exist = path.exists()
        exist_str = (
            Style.BRIGHT + Fore.GREEN + "existed" + Style.RESET_ALL
            if exist
            else Style.BRIGHT + Fore.RED + "NOT exist!" + Style.RESET_ALL
        )
        print(f"Dependent file {name}\t {path}\t {exist_str}")


def check_env_configs() -> None:
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n# Check environment configs"
        + Style.RESET_ALL
    )
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n## Check environment configs for API server"
        + Style.RESET_ALL
    )
    print(Style.DIM + Fore.YELLOW + api_env_configs.__doc__ + Style.RESET_ALL)
    print(api_env_configs.env_configs)
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n## Check environment configs for API documentation"
        + Style.RESET_ALL
    )
    print(
        Style.DIM
        + Fore.YELLOW
        + api_docs_env_configs.__doc__
        + Style.RESET_ALL
    )
    print(api_docs_env_configs.env_configs)
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n## Check environment configs for private API container"
        + Style.RESET_ALL
    )
    print(
        Style.DIM
        + Fore.YELLOW
        + docker_api_env_configs.__doc__
        + Style.RESET_ALL
    )
    print(docker_api_env_configs.env_configs)


def check_db_connections() -> None:
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n# Database connections"
        + Style.RESET_ALL
    )
    for db_name, neo4j_db in [("epigraphdb", epigraphdb), ("pqtl", pqtl)]:
        name = Style.BRIGHT + Fore.YELLOW + db_name + Style.RESET_ALL
        if neo4j_db.check_connection():
            status = Style.BRIGHT + Fore.GREEN + "Connected" + Style.RESET_ALL
        else:
            status = (
                Style.BRIGHT + Fore.RED + "NOT Connected" + Style.RESET_ALL
            )
        print(f"{name}: {status}")


if __name__ == "__main__":
    check_dependent_files()
    check_env_configs()
    check_db_connections()
