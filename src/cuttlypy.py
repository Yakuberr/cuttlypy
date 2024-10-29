import httpx
import time

class BotItem:
    def __init__(self, d: dict) -> None:
        self.raw = d

    @property
    def name(self):
        return self.raw['name']

    @property
    def clicks(self):
        return self.raw['clicks']


class RefItem:
    def __init__(self, d: dict) -> None:
        self.raw = d

    @property
    def link(self):
        return self.raw['link']

    @property
    def clicks(self):
        return self.raw['clicks']


class StandardDeviceItem:
    def __init__(self, d: dict) -> None:
        self.raw = d

    @property
    def tag(self):
        return self.raw['tag']

    @property
    def clicks(self):
        return self.raw['clicks']


class BrandDeviceItem:
    """Klasa dla danych z obiektu `Linkstats().devices.brand``"""

    def __init__(self, d: dict) -> None:
        self.raw = d

    @property
    def family(self):
        return self.raw['family']

    @property
    def tag(self):
        return self.raw['tag']

    @property
    def clicks(self):
        return self.raw['clicks']


class Devices:
    def __init__(self, d: dict) -> None:
        self.raw = d

    @property
    def geo(self):
        return {k: StandardDeviceItem(v) for k, v in self.raw['geo'].items()}

    @property
    def dev(self):
        return {k: StandardDeviceItem(v) for k, v in self.raw['dev'].items()}

    @property
    def sys(self):
        return {k: StandardDeviceItem(v) for k, v in self.raw['sys'].items()}

    @property
    def bro(self):
        return {k: StandardDeviceItem(v) for k, v in self.raw['bro'].items()}

    @property
    def brand(self) -> dict[str, BrandDeviceItem]:
        return {k: BrandDeviceItem(v) for k, v in self.raw['brand'].items()}

    @property
    def lang(self):
        return {k: StandardDeviceItem(v) for k, v in self.raw['lang'].items()}


class LinkStats:
    def __init__(self, d: dict) -> None:
        self.raw = d

    @property
    def status(self):
        return self.raw['stats']['status']

    @property
    def clicks(self):
        return self.raw['stats']['clicks']

    @property
    def date(self):
        return self.raw['stats']['date']

    @property
    def title(self):
        return self.raw['stats']['date']

    @property
    def fullLink(self):
        return self.raw['stats']['fullLink']

    @property
    def shortLink(self):
        return self.raw['stats']['shortLink']

    @property
    def facebook(self):
        return self.raw['stats']['facebook']

    @property
    def twitter(self):
        return self.raw['stats']['twitter']

    @property
    def pinterest(self):
        return self.raw['stats']['pinterest']

    @property
    def instagram(self):
        return self.raw['stats']['instagram']

    @property
    def googlePlus(self):
        return self.raw['stats']['googlePlus']

    @property
    def linkedin(self):
        return self.raw['stats']['linkedin']

    @property
    def rest(self):
        return self.raw['stats']['rest']

    @property
    def devices(self):
        return Devices(self.raw['stats']['devices'])

    @property
    def refs(self):
        self.raw['stats']['refs']['ref']
        return {k: RefItem(v) for k, v in self.raw['stats']['refs']['ref'].items()}

    @property
    def bots(self):
        return {k: BotItem(v) for k, v in self.raw['stats']['bots']['bots'].items()}


class GeneralLinkStats:
    def __init__(self, d: dict) -> None:
        self.raw = d
        self.raw['stats'].pop('devices')
        self.raw['stats'].pop('refs')
        self.raw['stats'].pop('bots')

    @property
    def status(self):
        return self.raw['stats']['status']

    @property
    def clicks(self):
        return self.raw['stats']['clicks']

    @property
    def date(self):
        return self.raw['stats']['date']

    @property
    def title(self):
        return self.raw['stats']['date']

    @property
    def fullLink(self):
        return self.raw['stats']['fullLink']

    @property
    def shortLink(self):
        return self.raw['stats']['shortLink']

    @property
    def facebook(self):
        return self.raw['stats']['facebook']

    @property
    def twitter(self):
        return self.raw['stats']['twitter']

    @property
    def pinterest(self):
        return self.raw['stats']['pinterest']

    @property
    def instagram(self):
        return self.raw['stats']['instagram']

    @property
    def googlePlus(self):
        return self.raw['stats']['googlePlus']

    @property
    def linkedin(self):
        return self.raw['stats']['linkedin']

    @property
    def rest(self):
        return self.raw['stats']['rest']


def get_link_analytics(session:httpx.Client, api_key:str, cuttly_url: str, general=False, sleep=False):
    res = session.get(f'http://cutt.ly/api/api.php?key={api_key}&stats={cuttly_url}',
                    follow_redirects=True)  # Bez opcji follow_redirects odpowiedź zwraca kod przekierowania bez zwracania danych
    if res.headers['x-ratelimit-remaining'] == '0' and sleep:
        time.sleep(60)
        return get_link_analytics(session=session, api_key=api_key, cuttly_url=cuttly_url, general=general, sleep=sleep)
    res.raise_for_status()
    if general:
        return GeneralLinkStats(res.json())
    return LinkStats(res.json())

async def async_get_link_analytics(session:httpx.AsyncClient, api_key:str, cuttly_url: str, general=False, sleep=False):
    res = await session.get(f'http://cutt.ly/api/api.php?key={api_key}&stats={cuttly_url}',
                    follow_redirects=True)  # Bez opcji follow_redirects odpowiedź zwraca kod przekierowania bez zwracania danych
    if res.headers['x-ratelimit-remaining'] == '0' and sleep:
        time.sleep(60)
        return await async_get_link_analytics(session=session, api_key=api_key, cuttly_url=cuttly_url, general=general, sleep=sleep)
    res.raise_for_status()
    if general:
        return GeneralLinkStats(res.json())
    return LinkStats(res.json())

__all__ = ["BotItem", "RefItem", "StandardDeviceItem", "BrandDeviceItem", "Devices", "LinkStats", "GeneralLinkStats",
           "get_link_analytics", "async_get_link_analytics"]