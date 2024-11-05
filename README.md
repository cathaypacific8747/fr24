# fr24

fr24 is a library for downloading data from [Flightradar24](https://flightradar24.com) using [gRPC](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md) and JSON.

It supports querying live feed snapshots/playback, trajectory history and other miscellaneous metadata.

Please see the [documentation](https://cathaypacific8747.github.io/fr24/) for detailed usage guides. 

## Installation

For the latest stable version:

```sh
pip install fr24
```

For a development version, clone the repository and run in the directory:

```sh
uv sync
```

## License

> [!IMPORTANT]  
> Code has been developed for educational purposes ONLY. Do not abuse it.

```json
{
  "copyright": "Copyright (c) 2014-2023 Flightradar24 AB. All rights reserved.",
  "legalNotice": "The contents of this file and all derived data are the property of Flightradar24 AB for use exclusively by its products and applications. Using, modifying or redistributing the data without the prior written permission of Flightradar24 AB is not allowed and may result in prosecutions."
}
```