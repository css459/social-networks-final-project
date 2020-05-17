# A Social Network Analysis of Venture Capital

Social Networks Final Project

## Introduction

This repository contains the source code for the paper
described in `doc/`. The purpose of this program is to
provide a simple way to traverse CrunchBase's data on
(Corporate) Venture Capitialists. We provide an automatic
parser and an extensible `Parser` Base Class, allowing the
end-user to **define their own custom network** from
CrunchBase's data.

Moreover, we provide a utility, `crawler.py` to perform
walks over the created network, and draw various statistics
from it.

## Resources

The `doc/` folder can be referenced for the supporing Article
of this work, as well as a presentation which gives an overview
of this work.

To seed our network for downloading, we have a pre-defined
(and greatly reduced) selection of Organization UUIDs available
in `uuids.txt`

