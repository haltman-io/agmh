from __future__ import annotations

from ..git_ops import with_basic_auth
from ..models import AppConfig, DestinationConfig, DestinationRepo, RepoInfo, TokenCredential
from ..ui import UI
from .base import DestinationAdapter


class GitDestination(DestinationAdapter):
    platform = "git"

    def __init__(self, dest: DestinationConfig, cfg: AppConfig, ui: UI):
        super().__init__(dest, cfg, ui)
        if not (dest.push_url_template or dest.url):
            raise ValueError("Generic Git destinations require a push_url_template or url")

    @property
    def owner(self) -> str:
        return self.dest.owner or self.dest.url or "git"

    def create_repository(self, repo: RepoInfo) -> DestinationRepo:
        return DestinationRepo(
            platform=self.platform,
            owner=self.owner,
            name=self.destination_repo_name(repo),
            web_url=self.web_url(repo),
            push_url=self.default_push_url(repo),
            created=False,
        )

    def default_push_url(self, repo: RepoInfo) -> str:
        return self._render_push_url(repo)

    def push_urls(self, repo: RepoInfo) -> list[str]:
        return self._authenticate_urls(self._render_push_url(repo), repo)

    def web_url(self, repo: RepoInfo) -> str:
        return self._render_push_url(repo).removesuffix(".git")

    def _auth_url(self, url: str, token: TokenCredential, repo: RepoInfo) -> str:
        username = token.username or self.dest.git_username or "git"
        return with_basic_auth(url, username, token.secret)

    def _render_push_url(self, repo: RepoInfo) -> str:
        destination_name = self.destination_repo_name(repo)
        template = self.dest.push_url_template or self.dest.url
        return template.format(
            owner=repo.owner,
            source_owner=repo.owner,
            destination_owner=self.dest.owner or "",
            repo=destination_name,
            name=destination_name,
            full_name=repo.full_name,
            source_platform=repo.source_platform,
            platform=self.platform,
        )
