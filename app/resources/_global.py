"""
Global resource config
"""
import datetime
from subprocess import check_output
from typing import Dict

from app import settings

today = datetime.date.today().isoformat()

unittest_headers = {"client-type": "pytest"}


def get_service_builds() -> Dict:
    """Return build versions of related components."""
    builds = {
        "epigraphdb": {
            "overall": settings.epigraphdb_version,
            "database": settings.epigraphdb.version,
            "api": settings.api_version,
            "web_app": None,
        },
        "pqtl": settings.pqtl.version,
    }
    return builds


def get_git_info() -> Dict:
    """Return information relating to git."""
    current_branch = (
        check_output("git branch | grep \\* | cut -d ' ' -f2", shell=True)
        .decode()
        .replace("\n", "")
    )
    current_commit = (
        check_output("git rev-parse --verify --short HEAD", shell=True)
        .decode()
        .replace("\n", "")
    )
    commit_date = (
        check_output(
            f"""git show -s \\
            --format=%cd --date=format:'%Y-%m-%d' \\
            {current_commit}
            """,
            shell=True,
        )
        .decode()
        .replace("\n", "")
    )

    info = {
        "current_branch": current_branch,
        "current_commit": current_commit,
        "current_date": commit_date,
    }
    return info
