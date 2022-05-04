## Shopcarts Service
Version: 1.0

[![Build Status](https://github.com/2022-Spring-NYU-DevOps-Shopcarts/shopcarts/actions/workflows/tdd.yml/badge.svg)](https://github.com/2022-Spring-NYU-DevOps-Shopcarts/shopcarts/actions)
[![Build Status](https://github.com/2022-Spring-NYU-DevOps-Shopcarts/shopcarts/actions/workflows/bdd.yml/badge.svg)](https://github.com/2022-Spring-NYU-DevOps-Shopcarts/shopcarts/actions)
[![codecov](https://codecov.io/gh/2022-Spring-NYU-DevOps-Shopcarts/shopcarts/branch/main/graph/badge.svg?token=YU8G34H0HW)](https://codecov.io/gh/2022-Spring-NYU-DevOps-Shopcarts/shopcarts)

Resource URLs: ```/shopcarts```, ```/shopcarts/<user-id>```, ```/shopcarts/<user-id>/items```, ```/shopcarts/<user-id>/items/<item-id>```

Allows different users to store items in their shopcarts.
Run locally via ```honcho start```.
Test via ```nosetests``` and (after starting local server) ```behave```.

Deployed to: [prod](http://nyu-shopcart-service-sp2203.us-south.cf.appdomain.cloud) and [dev](http://nyu-shopcart-service-sp2203-dev.us-south.cf.appdomain.cloud).


### Usage: 
See [apidocs](http://nyu-shopcart-service-sp2203.us-south.cf.appdomain.cloud/apidocs).
