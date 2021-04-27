# Linkauto
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
[![GitHub stars](https://img.shields.io/github/stars/stanvanrooy/linkauto)](https://github.com/stanvanrooy/linkauto/stargazers)
[![PyPI license](https://img.shields.io/pypi/l/linkauto)](https://pypi.python.org/project/linkauto/)
[![Downloads](https://pepy.tech/badge/linkauto/week)](https://pepy.tech/project/linkauto)

Linkauto is a Python package for automating various parts of LinkedIn, making use of the private LinkedIn API.

For feature requests, ideas, comments, etc., please open an issue.

## Installation
The package can be installed with the following pip command:
```pip install linkauto```

## Usage
Here is a retrieves a profile and sends an invite.

```python
from linkauto.api.client import ApiClient
from linkauto.api.constants import Linkedin_41588_146600, GooglePixelUS
import orjson, asyncio

async def main():
  client = ApiClient('username', 'password', Linkedin_41588_146600, GooglePixelUS)
  await client.init()
  await client.login()
  response = await client.profile_get(profile_url='/in/stan-van-rooy')
  profile = orjson.loads(await response.read())
  invite = await client.relationship_invitation_create(profile_url='stan-van-rooy')

if __name__ == '__main__':
  asyncio.run(main())
```

Other examples of how to use the package, can be found in the [examples directory](https://github.com/stanvanrooy/linkauto/tree/main/examples).

## Support
This is a hobby project, which means sometimes other things take priority. I will review issues and work on issues when I have the time. Spamming new issues, asking for a ton of updates, or things like that, will not speed up the process. It will probably even give me less motivation to work on it :)

If you're looking for paid support, please reach out to me at [stan@rooy.dev](mailto:stan@rooy.dev).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
