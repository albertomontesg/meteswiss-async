import asyncio

from meteoswiss_async import MeteoSwissClient


async def main():
    client = await MeteoSwissClient.with_session()

    resp = await client.get_weather(postal_code="8152")
    print(resp)
    print(resp.graph.weather_condition_3h)
    print(resp.graph.wind_cardinal_direction_3h)

    resp = await client.get_station_information(station_code="KLO")
    print(resp)

    resp = await client.get_full_overview(
        postal_code=["8152", "8001"], station_code=["KLO"]
    )
    print(resp)

    stations = await client.get_stations()
    print(stations)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
