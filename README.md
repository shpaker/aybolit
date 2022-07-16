# aybolit


## installation

```
pip install aybolit
```

## usage

```python
from dataclasses import asdict
from json import dumps

from aybolit import Aybolit

aybolit = Aybolit()


@aybolit('mongodb')
def mongodb_is_available():
  return 'available'


@aybolit()
def healthcheck_with_error():
  return 42 / 0


@aybolit()
def healthcheck_with_fail():
  assert 1 == 2


def redis_is_available():
  return 'available'


if __name__ == '__main__':
  aybolit.add(redis_is_available, 'redis')
  results = aybolit.check()
  print(
    dumps(asdict(results), indent=2, default=str),
  )
```

output:

```json
{
  "started_at": "2022-07-16 21:46:13.740670",
  "finished_at": "2022-07-16 21:46:13.740729",
  "checks": [
    {
      "started_at": "2022-07-16 21:46:13.740698",
      "finished_at": "2022-07-16 21:46:13.740699",
      "title": "mongodb",
      "state": "pass",
      "message": "available"
    },
    {
      "started_at": "2022-07-16 21:46:13.740705",
      "finished_at": "2022-07-16 21:46:13.740715",
      "title": "healthcheck_with_error",
      "state": "error",
      "message": "ZeroDivisionError: division by zero"
    },
    {
      "started_at": "2022-07-16 21:46:13.740719",
      "finished_at": "2022-07-16 21:46:13.740722",
      "title": "healthcheck_with_fail",
      "state": "fail",
      "message": null
    },
    {
      "started_at": "2022-07-16 21:46:13.740725",
      "finished_at": "2022-07-16 21:46:13.740726",
      "title": "redis",
      "state": "pass",
      "message": "available"
    }
  ]
}
```
