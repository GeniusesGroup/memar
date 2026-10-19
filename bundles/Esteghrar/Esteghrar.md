# Esteghrar - Golang version   
[![GoDoc](https://pkg.go.dev/badge/github.com/GeniusesGroup/esteghrar)](https://pkg.go.dev/github.com/GeniusesGroup/esteghrar)
[![Go Report](https://goreportcard.com/badge/github.com/GeniusesGroup/esteghrar)](https://goreportcard.com/report/github.com/GeniusesGroup/esteghrar)

Esteghrar is a software orchestrator based on [Memar](https://github.com/GeniusesGroup/memar) framework. Because we chose Unikernels(Exokernels) instead of Containers style, It will be a VM Orchestration not precisely like other tools (e.g. K8s, ...). Unlike other tools that need to operate and maintain separately from organization software(External observer), Esteghrar makes the organization software self-awareness(Internal observer). This will add more intelligence to any software that uses(embeds) Estghrar modules, without the need to use any AI models.

Modules need to deploy a distributed software base on memar framework

In one word Esteghrar want to add the ability to **reproduction** to any software, that It is most important factor of what we call **life**.

## Architecture

- [Esteghrar inside architecture]()
- [System architecture diagram that Esteghrar made it](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#R5VpRc5s4EP41nt49NAPIYHiM7aSXmfYuc57OXR9lo2AajBghYru%2F%2Fla2ZMAC4ybGkN5LRlokBX27%2B0n74QGarDafGE6WX6hPooFl%2BJsBmg4sy3UN%2BCsM273BNp29IWChvzeZuWEW%2FiDSKOcFWeiTtDSQUxrxMCkbFzSOyYKXbJgxui4Pe6JR%2Bb8mOCCaYbbAkW79J%2FT5Um7LGuX2P0gYLNV%2FNh1v%2F2SF1WC5k3SJfboumNDdAE0YpXzfWm0mJBLYKVz28%2B5rnh5ejJGYnzPhC5r95c0mmRO7H%2FFXRPH9%2FPGjKffxgqNM7li%2BLd8qCAJGs0QOI4yTTRXweK6GG%2FqLmYftQpgQuiKcbWGIXGgoZ8gIsUz5Cusc76EKh2UBa6QmYunj4LB0DgM0JBI%2FgwpqRgWWgRiEzhgcmwjjIqIZrDpeL0NOZgleCOMasgJsS76CN5ia0KxFsojYCWfpOHYIlK0B9YDxTGyG0RfIXAZNU8MOds7LoOAoDGKBISAAk9BY4BNCGt7KB6vQ98X0MSNp%2BENGmwH9hIYx3%2B3LHg%2FsqVgr4zTdE4lYOuWMPpMJjSisO41pLFZ5CqPoyHR5v6hlrHKAO1p4m0aV11pzmnuNnH8VUkdUYI5cHSvX1LEyjVFbYDVjBVDFPvFluLWX%2Fe5p7MokOqwAriLIXNQSbpaG213KSbBkWFACXBOyCI71eiiNZiiLOTyw0NMTcRYLLeHhiT%2Fy5obRKvjluEV6ileB77SV4frxdZskEdApD2kMD%2F6EW9r%2FgphrvFbMCuua1DvUHDPO0jAmadpSUvg2cf1hVVK41hw5TrtJ0ZgVo2tmhaWjLy8rt48Pp2Bvl9YbjkRUBnGon4heVQRbbZ2HFTdhHyom2aWML2lAYxzd5dZxOYLzMZ8pTSSA3wnnW1n%2BCZ4ow0s2If9XTL%2BxZe%2BbXEy0p5tiZ6s6Mey3MEl0v6n1RCeftuupeSnHjN%2BK0nF3p8dpGi6U%2BT6Myh4Xe6%2F1t%2BJXmrEFOYWpKmwxC8jJWKkOFUYiYPaX8otc3vNnXIVUKYQXXPDMRbLmdPF4oBB1uVakUyyKrsoyTh3LJOClJ8pWv%2F1NggzalP0%2BsJxIHLhzuBQ5Ad9Bcmz5HD6Lw5ry5a6aUqsAYU30wQ9cvJ84Tb5nqWjjnRTBngmHieAGMcmomedTksYfRIuuxTUBxwLolDDwUHqj532rFfBpt6MjWjQr3G5WEaPZWi2sJKFumNEs8uKNZZ9LjcgscqNx4zaw4673SFgIoIn7YEeUqc7yRsrcp2NXnGnZ3Z6Wo9cdl3Y5Jjy7ISjO9H9l7FzyHH0fMXEV%2BaVBcj2SpKyhrZ%2Ba15USLa8Zlg40V6u5hLwyUOrkO6m56tj9YqV9nV96qrmiMy7PLWmuTUj1T3NVxWsPRFd0mkd7JroiXfh716prE%2Fo9U111falSdv3lubnBbXYFGV9VhUX6V8v3LMM2Zkm%2FZFhUK5B0KcM2nZI9k2FRp2JDQWD4qcLyIC68K61BObHndSVyuw0JzylJUKPTQQGdY8%2FmgVIOkwupDxeMCFVONEYEemtE7KbC3vC2MEAe8fnKj8JQOGCPxVHPLUZX43hkeEfRuH%2BDPDYPW3nDp1Cj23B9FYFZPf%2BShLxzA9PqlKrO0Hqu%2FynJdsrlnKMupV19ShrqP9Do7IvCuR8U%2Bk7d52rEb06QVzH30D66ZspaqY65tfHum5gbuvnvkffD8x91o7v%2FAA%3D%3D).

## Why new orchestraor

- [Plug and Play](https://en.wikipedia.org/wiki/Plug_and_play) to any software without nedd to do anything to make it, a distributed software! e.g. without need to config first, ...
- As [nanos kernel](https://github.com/nanovms/nanos) said, all kernels (e.g. Linux, ...) and orchestration(e.g. k8s, nomad, ...) develepe to run and orchestrate multiple applications, but like nanos, Esteghrar also develope to handle just one apllication.
- Add full system observability (insight) without need to do anything by any one(NoOps).

## Some resources

- https://kubernetes.io/docs/reference/kubernetes-api/ - https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#node-v1-core
- https://mesosphere.github.io/marathon/api-console/index.html
- https://github.com/Yelp/paasta/blob/master/comparison.md
- https://docs.digitalocean.com/reference/api/api-reference/#tag/Images
- https://github.com/erikh/spin
