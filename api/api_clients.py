from aiohttp import ClientSession


class EuropeanCentralBankClient:
    host: str = "https://sdw-wsrest.ecb.europa.eu"

    async def _fetch(self, endpoint: str):
        async with ClientSession(base_url=self.host) as client:
            async with client.get(endpoint) as response:
                response.raise_for_status()
                return await response.text()

    async def fetch_exchange_rate(self, source: str, target: str,) -> str:
        return await self._fetch(f"/service/data/EXR/M.{source}.{target}.SP00.A?detail=dataonly")

    async def fetch_raw_data(self, identifier: str):
        return await self._fetch(f"/service/data/BP6/{identifier}?detail=dataonly")
