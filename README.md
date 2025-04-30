# wuwa wiki api

A [Wuthering Waves](https://wutheringwaves.kurogames.com/) API server that uses
wiki pages as its data source.

## Requirements

- Python 3.12 or higher
- uv
- Taskfile

## Quick Start

Run the following command and then open your browser to access
`http://127.0.0.1/graphql`.

```
$ task run
```

To run type checking, execute the following command.

```
$ task tyepcheck
```

To export GraphQL schema, execute the following command.

```
$ task export-graphql
```

To run tests, execute the following command.

```
$ task test
```