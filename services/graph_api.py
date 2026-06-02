"""Asynchronous Microsoft Graph API client for SharePoint/OneDrive access."""

import asyncio
import json
from pathlib import Path
from typing import Any

import aiohttp
import msal

from config.settings import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID


class GraphAPIClient:
    """Simple client for Graph API using application-only authentication."""

    GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]
    GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

    def __init__(self, tenant_id: str | None = None, client_id: str | None = None, client_secret: str | None = None) -> None:
        self.tenant_id = tenant_id or AZURE_TENANT_ID
        self.client_id = client_id or AZURE_CLIENT_ID
        self.client_secret = client_secret or AZURE_CLIENT_SECRET
        self._authority = f"https://login.microsoftonline.com/{self.tenant_id}" if self.tenant_id else None
        self._app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            authority=self._authority,
            client_credential=self.client_secret,
        ) if self.client_id and self.client_secret and self._authority else None

    async def get_access_token(self) -> str:
        """Acquire a Graph access token using the Client Credentials Flow."""
        if not self._app:
            raise ValueError("MSAL application is not configured. Check Azure credentials in .env.")

        result = await asyncio.to_thread(self._app.acquire_token_for_client, scopes=self.GRAPH_SCOPE)
        if "access_token" not in result:
            raise RuntimeError(result.get("error_description", "Failed to acquire Microsoft Graph token."))
        return result["access_token"]

    async def _request(self, method: str, path: str, *, params: dict[str, Any] | None = None, json_body: dict[str, Any] | None = None) -> dict[str, Any]:
        token = await self.get_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"{self.GRAPH_BASE_URL}{path}"

        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, params=params, json=json_body) as response:
                payload = await response.text()
                if response.status >= 400:
                    raise RuntimeError(f"Graph API error {response.status}: {payload}")
                return json.loads(payload) if payload else {}

    async def list_directory(self, site_id: str, folder_path: str = "/") -> list[dict[str, Any]]:
        """List files and folders in a SharePoint site path."""
        encoded_path = folder_path.strip("/")
        path = f"/sites/{site_id}/drive/root" if not encoded_path else f"/sites/{site_id}/drive/root:/{encoded_path}:/children"
        result = await self._request("GET", path)
        return result.get("value", [])

    async def search_files(self, site_id: str, query: str, folder_path: str = "/") -> list[dict[str, Any]]:
        """Search for files by name/content within a site path."""
        path = f"/sites/{site_id}/drive/root/search(q=' {query} ')" if not folder_path or folder_path == "/" else f"/sites/{site_id}/drive/root:/{folder_path.strip('/')}:/search(q=' {query} ')"
        result = await self._request("GET", path)
        return result.get("value", [])

    async def download_file(self, file_url: str, destination: str | Path) -> Path:
        """Download a file from Graph by its content URL."""
        token = await self.get_access_token()
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(file_url, headers={"Authorization": f"Bearer {token}"}) as response:
                if response.status >= 400:
                    raise RuntimeError(f"Failed to download file: {response.status}")
                content = await response.read()

        destination.write_bytes(content)
        return destination

    async def download_by_id(self, site_id: str, file_id: str, destination: str | Path) -> Path:
        """Download a file using its Graph item identifier."""
        metadata = await self._request("GET", f"/sites/{site_id}/drive/items/{file_id}")
        download_url = metadata.get("@microsoft.graph.downloadUrl")
        if not download_url:
            raise RuntimeError("No download URL returned for the requested file.")
        return await self.download_file(download_url, destination)
