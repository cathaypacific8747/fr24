# Library
Most code is developed in asynchronous mode: if you are not familiar with that programming style, wrap your code in an `async` function called `async_main`, and

- run `asyncio.run(main())` in a Python script;
- run `await main()` in a Jupyter notebook.

You can find usage examples in under [`scripts/`](https://github.com/cathaypacific8747/fr24/tree/master/scripts).

!!! note
    Pyarrow do not come with stubs: generate them with
    ```sh
    stubgen -p pyarrow -o $PATH_TO_SITE_PACKAGES
    ```

Intersphinx could be found [here](https://cathaypacific8747.github.io/fr24/objects.inv).

<!-- TODO: add scripts here and show corresponding output. -->