# Meza

[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/freephile/meza/dev)](https://github.com/freephile/meza/commits/dev/)
[![GitHub Tag](https://img.shields.io/github/v/tag/freephile/meza?label=last%20tag)](https://github.com/freephile/meza/tags)
[![Lint YAML Files](https://github.com/freephile/meza/actions/workflows/yamllint.yml/badge.svg?branch=dev)](https://github.com/freephile/meza/actions/workflows/yamllint.yml)
[![Advanced Release Management](https://github.com/freephile/meza/actions/workflows/advanced-release-management.yml/badge.svg?branch=dev)](https://github.com/freephile/meza/actions/workflows/advanced-release-management.yml)
[![Generate Release Notes and Update Changelog](https://github.com/freephile/meza/actions/workflows/release-notes.yml/badge.svg?event=push&branch=dev)](https://github.com/freephile/meza/actions/workflows/release-notes.yml)
[![GitHub Discussions](https://img.shields.io/github/discussions/freephile/meza)](https://github.com/freephile/meza/discussions)
[![GitHub issues](https://img.shields.io/github/issues/freephile/meza.svg)](https://github.com/freephile/meza/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/freephile/meza.svg)](https://github.com/freephile/meza/issues/?q=is%3Aissue+is%3Aclosed)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/freephile/meza/total)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)



<img src="https://raw.githubusercontent.com/enterprisemediawiki/meza/master/manual/commands.gif">

![Meza Component Logos](assets/meza_component_logos.png)

Setup an enterprise MediaWiki server with **simple commands**. Put all components on a single monolithic server or split them out over many. Run a solitary master database or have replicas. Deploy to multiple environments. Run backups. Do it all using the `meza` command. Run `meza --help` for more info.

## Why Meza?

Standard MediaWiki is easy to install, but increasingly its newer and better features are contained within extensions that are more complicated. Additionally, they may be particularly difficult to install on Enterprise Linux derivatives. This project aims to make these features (VisualEditor, CirrusSearch, etc) easy to *install, backup, reconfigure, and maintain* in a robust and well-tested way.

## Requirements

1. Rocky Linux 8 or RHEL 8 (for now, with Debian support in the works)
2. Minimal install: Attempting to install it on a server with many other things already installed may not work properly due to conflicts.

## Install and usage

See all the Meza documentation at https://www.mediawiki.org/wiki/Meza

## Contributing

If you'd like to contribute to this project, please see [this guide on how to help](CONTRIBUTING.md).
