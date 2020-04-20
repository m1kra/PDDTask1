#!/bin/bash

rm -rf provision/ssh/*
ssh-keygen -q -t rsa -N '' -f provision/ssh/id_rsa