## Hello AOSP

### module partition

> libhelloaosp -> odm
>
> libhelloaosp.v1 -> vendor
>
> hello1_aosp -> odm
>
> libhelloaosp.v2 -> system
>
> hello2_aosp -> system


### Dir Structure

```

.
├── bin
├── hello
│   ├── hello1
│   ├── hello2
│   │   └── lib_api -> ../lib_api
│   ├── lib
│   ├── lib64
│   └── lib_api
└── libhelloaosp
    └── include


```
